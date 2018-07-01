from n_utils.cf_utils import InstanceInfo, get_images, INSTANCE_IDENTITY_URL
from dateutil.parser import parse

class IdentityResp:
    def __init__(self):
        return

    text = """
{
  "privateIp" : "192.168.208.238",
  "devpayProductCodes" : null,
  "marketplaceProductCodes" : [ "aw0evgkw8e5c1q413zgy5pjce" ],
  "version" : "2017-09-30",
  "instanceId" : "i-021614c41980832b8",
  "billingProducts" : null,
  "instanceType" : "m3.large",
  "availabilityZone" : "eu-west-1a",
  "accountId" : "832585949989",
  "kernelId" : null,
  "ramdiskId" : null,
  "architecture" : "x86_64",
  "imageId" : "ami-f8252c12",
  "pendingTime" : "2018-06-26T12:24:28Z",
  "region" : "eu-west-1"
}
"""
class ClientResp:
    def __init__(self):
        return
    def describe_tags(self, Filters=None):
        assert Filters[0]['Name'] == 'resource-id'
        assert Filters[0]['Values'] == ['i-021614c41980832b8']
        return {"Tags": [
                    {
                        "Key": 'Name',
                        "Value": "test-instance"
                    },
                    {
                        "Key": 'aws:cloudformation:stack-name',
                        "Value": "test-stack"
                    },
                    {
                        "Key": 'aws:cloudformation:stack-id',
                        "Value": "test-stack-id"
                    },
                    {
                        "Key": 'aws:cloudformation:logical-id',
                        "Value": "test-logical-id"
                    }]
                }
    def describe_stacks(self, StackName=None):
        assert StackName == "test-stack"
        return {
    "Stacks": [
        {
            "StackId": "arn:aws:cloudformation:eu-west-1:832585949989:stack/infra-network/809d77a0-afab-11e5-92de-50faeb52a4d2", 
            "Description": "Nitor infra network stack", 
            "Tags": [], 
            "Outputs": [
                {
                    "Description": "subnet id", 
                    "OutputKey": "subnetInfraA", 
                    "OutputValue": "subnet-abe2edce"
                }, 
                {
                    "Description": "subnet id", 
                    "OutputKey": "subnetInfraB", 
                    "OutputValue": "subnet-70112607"
                }],
            "EnableTerminationProtection": False, 
            "CreationTime": parse("2015-12-31T10:44:43.689Z"), 
            "StackName": "infra-network", 
            "NotificationARNs": [], 
            "StackStatus": "UPDATE_ROLLBACK_COMPLETE", 
            "LastUpdatedTime": parse("2015-12-31T13:39:48.260Z"), 
            "DisableRollback": False, 
            "RollbackConfiguration": {}
        }
    ]
}
    def describe_stack_resources(self, StackName=None):
        assert StackName == "test-stack"
        return {
    "StackResources": [
        {
            "StackId": "arn:aws:cloudformation:eu-west-1:832585949989:stack/infra-network/809d77a0-afab-11e5-92de-50faeb52a4d2", 
            "ResourceStatus": "CREATE_COMPLETE", 
            "ResourceType": "AWS::EC2::NetworkAcl", 
            "Timestamp": "2015-12-31T10:45:24.071Z", 
            "StackName": "infra-network", 
            "PhysicalResourceId": "acl-f94c779c", 
            "LogicalResourceId": "aclNitorInfra"
        }, 
        {
            "StackId": "arn:aws:cloudformation:eu-west-1:832585949989:stack/infra-network/809d77a0-afab-11e5-92de-50faeb52a4d2", 
            "ResourceStatus": "CREATE_COMPLETE", 
            "ResourceType": "AWS::EC2::NetworkAclEntry", 
            "Timestamp": "2015-12-31T10:45:45.723Z", 
            "StackName": "infra-network", 
            "PhysicalResourceId": "infra-aclen-4YIM1ZP45OYX", 
            "LogicalResourceId": "aclentryAllowAllEgress"
        }
    ]
}
    def describe_images(self, Filters=None):
        assert Filters[0]['Name'] == 'tag-value'
        assert Filters[0]['Values'] == ['awsdev_centos_jenkins_bake_*']
        return {
    "Images": [
        {
            "ProductCodes": [
                {
                    "ProductCodeId": "aw0evgkw8e5c1q413zgy5pjce", 
                    "ProductCodeType": "marketplace"
                }
            ], 
            "Description": "", 
            "Tags": [
                {
                    "Value": "awsdev_centos_jenkins_bake_0001", 
                    "Key": "Name"
                }, 
                {
                    "Value": "20180410161338", 
                    "Key": "Tstamp"
                }, 
                {
                    "Value": "awstest_centos_jenkins_promote_0001", 
                    "Key": "awstest_centos_jenkins_promote"
                }
            ], 
            "VirtualizationType": "hvm", 
            "Hypervisor": "xen", 
            "EnaSupport": True, 
            "SriovNetSupport": "simple", 
            "ImageId": "ami-03045e7a", 
            "State": "available", 
            "BlockDeviceMappings": [
                {
                    "DeviceName": "/dev/sda1", 
                    "Ebs": {
                        "Encrypted": False, 
                        "DeleteOnTermination": True, 
                        "VolumeType": "gp2", 
                        "VolumeSize": 8, 
                        "SnapshotId": "snap-0a112c2708d4a1d16"
                    }
                }
            ], 
            "Architecture": "x86_64", 
            "ImageLocation": "832585949989/awsdev_centos_jenkins_bake_0001", 
            "RootDeviceType": "ebs", 
            "OwnerId": "832585949989", 
            "RootDeviceName": "/dev/sda1", 
            "CreationDate": "2018-04-10T13:22:11.000Z", 
            "Public": False, 
            "ImageType": "machine", 
            "Name": "awsdev_centos_jenkins_bake_0001"
        }, 
        {
            "ProductCodes": [
                {
                    "ProductCodeId": "aw0evgkw8e5c1q413zgy5pjce", 
                    "ProductCodeType": "marketplace"
                }
            ], 
            "Description": "", 
            "Tags": [
                {
                    "Value": "aws_centos_jenkins_promote_0001", 
                    "Key": "aws_centos_jenkins_promote"
                }, 
                {
                    "Value": "awsdev_centos_jenkins_bake_0031", 
                    "Key": "Name"
                }, 
                {
                    "Value": "20180510103015", 
                    "Key": "Tstamp"
                }
            ], 
            "VirtualizationType": "hvm", 
            "Hypervisor": "xen", 
            "EnaSupport": True, 
            "SriovNetSupport": "simple", 
            "ImageId": "ami-3fdfe846", 
            "State": "available", 
            "BlockDeviceMappings": [
                {
                    "DeviceName": "/dev/sda1", 
                    "Ebs": {
                        "Encrypted": False, 
                        "DeleteOnTermination": True, 
                        "VolumeType": "gp2", 
                        "VolumeSize": 8, 
                        "SnapshotId": "snap-037ed955e6363bab7"
                    }
                }
            ], 
            "Architecture": "x86_64", 
            "ImageLocation": "832585949989/awsdev_centos_jenkins_bake_0031", 
            "RootDeviceType": "ebs", 
            "OwnerId": "832585949989", 
            "RootDeviceName": "/dev/sda1", 
            "CreationDate": "2018-05-10T07:41:11.000Z", 
            "Public": False, 
            "ImageType": "machine", 
            "Name": "awsdev_centos_jenkins_bake_0031"
        }, 
        {
            "ProductCodes": [
                {
                    "ProductCodeId": "aw0evgkw8e5c1q413zgy5pjce", 
                    "ProductCodeType": "marketplace"
                }
            ], 
            "Description": "", 
            "Tags": [
                {
                    "Value": "awsdev_centos_jenkins_bake_0032", 
                    "Key": "Name"
                }, 
                {
                    "Value": "20180623181343", 
                    "Key": "Tstamp"
                }
            ], 
            "VirtualizationType": "hvm", 
            "Hypervisor": "xen", 
            "EnaSupport": True, 
            "SriovNetSupport": "simple", 
            "ImageId": "ami-4dddd2a7", 
            "State": "available", 
            "BlockDeviceMappings": [
                {
                    "DeviceName": "/dev/sda1", 
                    "Ebs": {
                        "Encrypted": False, 
                        "DeleteOnTermination": True, 
                        "VolumeType": "gp2", 
                        "VolumeSize": 8, 
                        "SnapshotId": "snap-06a4decdcb0904550"
                    }
                }
            ], 
            "Architecture": "x86_64", 
            "ImageLocation": "832585949989/awsdev_centos_jenkins_bake_0032", 
            "RootDeviceType": "ebs", 
            "OwnerId": "832585949989", 
            "RootDeviceName": "/dev/sda1", 
            "CreationDate": "2018-06-23T15:23:51.000Z", 
            "Public": False, 
            "ImageType": "machine", 
            "Name": "awsdev_centos_jenkins_bake_0032"
        }]} 



def test_instance_info(mocker):
    boto3 = mocker.patch('n_utils.cf_utils.boto3')
    boto3.client.return_value = ClientResp() 
    retry = mocker.patch('n_utils.cf_utils.get_retry')
    retry.return_value = IdentityResp() 
    is_ec2 = mocker.patch('n_utils.cf_utils.is_ec2')
    is_ec2.return_value = True
    wait_net_service = mocker.patch('n_utils.cf_utils.wait_net_service')
    wait_net_service.return_value = True
    info = InstanceInfo()
    assert info.instance_id() == "i-021614c41980832b8"
    assert info.region() == "eu-west-1"
    assert info.stack_name() == "test-stack"
    assert info.stack_id() == "test-stack-id"
    assert info.logical_id() == "test-logical-id"
    assert info.initial_status() == "UPDATE_ROLLBACK_COMPLETE"
    assert info.availability_zone() == "eu-west-1a"
    assert info.private_ip() == "192.168.208.238"
    assert info.tag("Name") == "test-instance"
    retry.assert_called_with(INSTANCE_IDENTITY_URL)
    wait_net_service.assert_called_with("169.254.169.254", 80, 120)

def test_get_images(mocker):
    boto3 = mocker.patch('n_utils.cf_utils.boto3')
    boto3.client.return_value = ClientResp()
    images = get_images("awsdev_centos_jenkins_bake")
    assert images[0]["Name"] == "awsdev_centos_jenkins_bake_0032"
    assert images[2]["Name"] == "awsdev_centos_jenkins_bake_0001"

