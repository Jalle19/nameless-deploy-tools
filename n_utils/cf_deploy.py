#!/usr/bin/env python

# Copyright 2016 Nitor Creations Oy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import codecs
import collections
import ctypes
import inspect
import locale
from operator import itemgetter
import os
import re
import sys
import time
import threading
from threading import Thread
import boto3
from botocore.exceptions import ClientError
from awslogs.core import AWSLogs
from . import aws_infra_util

def update_stack(stack_name, template, params):
    clf = boto3.client('cloudformation')
    chset_name = stack_name + "-" + time.strftime("%Y%m%d%H%M%S", time.gmtime())
    chset_id = clf.create_change_set(StackName=stack_name, TemplateBody=template,
                                     Parameters=params,
                                     Capabilities=["CAPABILITY_IAM"],
                                     ChangeSetName=chset_name)['Id']
    chset_data = clf.describe_change_set(ChangeSetName=chset_id)
    chset_data['CreationTime'] = time.strftime("%a, %d %b %Y %H:%M:%S +0000",
                                               chset_data['CreationTime'].timetuple())
    print "** Changeset:"
    print aws_infra_util.json_save(chset_data)
    status = chset_data['Status']
    while "_COMPLETE" not in status and "FAILED" != status:
        time.sleep(5)
        chset_data = clf.describe_change_set(ChangeSetName=chset_id)
        status = chset_data['Status']
    if status == "FAILED":
        clf.delete_change_set(ChangeSetName=chset_id)
        raise Exception("Creating changeset failed")
    else:
        clf.execute_change_set(ChangeSetName=chset_id)
    return

def create_stack(stack_name, template, params):
    clf = boto3.client('cloudformation')
    clf.create_stack(StackName=stack_name, TemplateBody=template,
                     Parameters=params, Capabilities=["CAPABILITY_IAM"])
    return

def delete(stack_name, region):
    if sys.version_info < (3, 0):
        sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

    os.environ['AWS_DEFAULT_REGION'] = region
    print "\n\n**** Deleting stack '" + stack_name
    clf = boto3.client('cloudformation')
    clf.delete_stack(StackName=stack_name)
    while True:
        try:
            stack_info = clf.describe_stacks(StackName=stack_name)
            status = stack_info['Stacks'][0]['StackStatus']
            if not status.endswith("_IN_PROGRESS") and not status.endswith("_COMPLETE"):
                 raise Exception("Delete stack failed: end state " + status)
            print "Status: \033[32;1m"+ status + "\033[m"
            time.sleep(5)
        except ClientError as err:
            if err.response['Error']['Code'] == 'ValidationError' and \
               err.response['Error']['Message'].endswith('does not exist'):
                print "Status: \033[32;1mDELETE_COMPLETE\033[m"
                break
            else:
                raise

def deploy(stack_name, yaml_template, region):
    if sys.version_info < (3, 0):
        sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

    os.environ['AWS_DEFAULT_REGION'] = region
    # Disable buffering, from http://stackoverflow.com/questions/107705/disable-output-buffering
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    ami_id = ""
    ami_name = ""
    ami_created = ""
    if 'AMI_ID' in os.environ and os.environ['AMI_ID']:
        ami_id = os.environ['AMI_ID']

    template_doc = aws_infra_util.yaml_to_dict(yaml_template)
    if not ami_id and 'Parameters' in template_doc and \
      'paramAmi'in template_doc['Parameters'] and \
      'IMAGE_JOB' in os.environ:
        image_job = re.sub(r'\W', '_', os.environ['IMAGE_JOB'].lower())
        print "Looking for ami with name prefix " + image_job
        ec2 = boto3.client('ec2')
        ami_data = ec2.describe_images(Filters=[{'Name': 'name',
                                                 'Values': [image_job + "_*"]}])
        if len(ami_data['Images']) > 0:
            sorted_images = sorted(ami_data['Images'],
                                   key=itemgetter('CreationDate'), reverse=True)
            for image in sorted_images:
                if re.match('^' + image_job + '_\\d{4,14}', image['Name']):
                    print "Result: " + aws_infra_util.json_save(image)
                    ami_id = image['ImageId']
                    ami_name = image['Name']
                    ami_created = image['CreationDate']
                    break
    elif ami_id and 'Parameters' in template_doc and \
        'paramAmi'in template_doc['Parameters']:
        print "Looking for ami metadata with id " + ami_id
        ec2 = boto3.client('ec2')
        ami_meta = ec2.describe_images(ImageIds=[ami_id])
        print "Result: " + aws_infra_util.json_save(ami_meta)
        image = ami_meta['Images'][0]
        ami_name = image['Name']
        ami_created = image['CreationDate']

    print "\n\n**** Deploying stack '" + stack_name + "' with template '" + \
          yaml_template + "' and ami_id '" + str(ami_id) + "'"

    if "Parameters" not in template_doc:
        template_doc['Parameters'] = []

    template_parameters = template_doc['Parameters']

    if ami_id:
        os.environ["paramAmi"] = ami_id
        os.environ["paramAmiName"] = ami_name
        os.environ["paramAmiCreated"] = ami_created
        if not "paramAmiName" in template_parameters:
            template_parameters['paramAmiName'] = \
                collections.OrderedDict([("Description", "AMI Name"),
                                         ("Type", "String"), ("Default", "")])
        if not "paramAmiCreated" in template_parameters:
            template_parameters['paramAmiCreated'] = \
                collections.OrderedDict([("Description", "AMI Creation Date"),
                                         ("Type", "String"), ("Default", "")])

    json_template = aws_infra_util.json_save(template_doc)
    json_small = aws_infra_util.json_save_small(template_doc)

    print "** Final template:"
    print json_template
    print ""

    # Load previous stack information to see if it has been deployed before
    stack_data = None
    clf = boto3.client('cloudformation')
    stack_oper = "create_stack"
    try:
        stack_data = clf.describe_stacks(StackName=stack_name)
        # Dump original status, for the record
        status = stack_data['Stacks'][0]['StackStatus']
        print "Status: \033[32;1m" + status + "\033[m"
        stack_oper = "update_stack"
    except ClientError as err:
        if err.response['Error']['Code'] == 'ValidationError' and \
           err.response['Error']['Message'].endswith('does not exist'):
            print "Status: \033[32;1mNEW_STACK\033[m"
        else:
            raise

    # Create/update stack
    params_doc = []
    for key in template_parameters.keys():
        if key in os.environ:
            val = os.environ[key]
            print "Parameter " + key + ": using \033[32;1mCUSTOM value " + \
                  val + "\033[m"
            params_doc.append({'ParameterKey': key, 'ParameterValue': val})
        else:
            val = template_parameters[key]['Default']
            print "Parameter " + key + ": using default value " + str(val)

    stack_func = globals()[stack_oper]
    stack_func(stack_name, json_small, params_doc)
    logs = AWSLogs(log_group_name='instanceDeployment',
                   log_stream_name=stack_name + "/*",
                   start='1m ago')
    print "Waiting for " + stack_oper + " to complete:"
    log_threads = {}
    while True:
        stack_info = clf.describe_stacks(StackName=stack_name)
        status = stack_info['Stacks'][0]['StackStatus']
        if "ROLLBACK" in status:
            color = "\033[31;1m"
        else:
            color = "\033[32;1m"
        print color + "Status: " + status + "\033[m"
        if not status.endswith("_IN_PROGRESS"):
            for stream_name, thread in log_threads.iteritems():
                thread.raise_exception()
                while thread.isAlive():
                    time.sleep(0.01)
                    thread.raiseException()
            break
        try:
            streams = logs.get_streams()
            for stream_name in streams:
                if stream_name not in log_threads:
                    thread = LoggingThread(stream_name)
                    thread.start()
                    log_threads[stream_name] = thread
        except ClientError:
            pass
        time.sleep(5)

    if (stack_oper == "create_stack" and status != "CREATE_COMPLETE") or \
       (stack_oper == "update_stack" and status != "UPDATE_COMPLETE"):
        sys.exit(stack_oper + " failed: end state " + status)

    print "Done!"

def _async_raise(tid, exctype):
    '''Raises an exception in the threads with id tid'''
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid,
                                                     ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # "if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")

class LoggingThread(Thread):
    '''A thread class that supports raising exception in the thread from
       another thread.
    '''
    def __init__(self, stream_name):
        Thread.__init__(self)
        self._thread_id = None
        self._stream_name = stream_name

    def _get_my_tid(self):
        if not self.isAlive():
            raise threading.ThreadError("the thread is not active")
        if hasattr(self, "_thread_id"):
            return self._thread_id
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid

    def run(self):
        logs = AWSLogs(log_group_name='instanceDeployment',
                       log_stream_name=self._stream_name,
                       start='1m ago', output_timestamp_enabled=True,
                       output_stream_enabled=True, color_enabled=True,
                       watch=True)
        logs.list_logs()
        return

    def raise_exception(self):
        _async_raise(self._get_my_tid(), KeyboardInterrupt)
