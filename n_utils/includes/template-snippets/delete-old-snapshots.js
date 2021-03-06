exports.handler = function(event, context) {
  var CF_paramEBSTag="confluence-data";
  var CF_AWS__AccountId="832585949989";
  AWS = require('aws-sdk');
  ec2 = new AWS.EC2();
  var KEEP_AT_LEAST = 5;

  var params = {
      DryRun: false,
      Filters: [
          {
              Name: 'tag:' + CF_paramEBSTag,
              Values: [ CF_paramEBSTag ]
          }
      ],
      OwnerIds: [ CF_AWS__AccountId ]
  };

  deleted_snapshots = {DeletedSnaphots: []};

  ec2.describeSnapshots(params, function(err, data) {
      if (err) {
        console.log(err, err.stack);
        context.fail(err);
        return;
      } else {
        data.Snapshots.sort(dateComparator);
        if (data.Snapshots.length > KEEP_AT_LEAST) {
          delete_snapshots(context, data.Snapshots.slice(KEEP_AT_LEAST, data.Snapshots.length));
        } else {
          context.succeed(deleted_snapshots);
        }
      }
  });
};

function delete_snapshots(context, snapshots) {
  var signals = {expected: 0, received: 0};

  for (i = 0; i < snapshots.length; i++) {
    (function(i) {
        var snapshotTime = new Date(snapshots[i].StartTime);
        var monthAgo = new Date(new Date().getTime() - 2592000000);
        var iCopy = (function(iCopy){return iCopy;})(i);
        if (snapshotTime < monthAgo) {
          var callback = delete_callback(deleted_snapshots, snapshots[iCopy]);
          signals.expected++;
          var timer = setTimeout(function() {
            timer = null;
            signals.received++;
            callback({error:'Call timed out'});
            console.log("timed out");
          }, 5000);
          ec2.deleteSnapshot({SnapshotId: snapshots[i].SnapshotId}, function(err, data) {
            if (timer) {
              signals.received++;
              clearTimeout(timer);
              callback(err, data);
            }
          });
        }
    })(i);
  }
  var signalChecker = function() {
    if (signals.received < signals.expected) {
      setTimeout(signalChecker, 1000);
      return;
    }
    context.succeed(deleted_snapshots);
  };
  signalChecker();
}

function delete_callback (deleted_snapshots, snapshot) {
  return function(err, data) {
    if (err) {
      console.log(err, err.stack);
    } else {
      console.log("Deleted snapshot " + snapshot.SnapshotId);
      deleted_snapshots.DeletedSnaphots.push(snapshot);
    }
  };
}

function dateComparator (a, b) {
  if( new Date(a.StartTime).getTime() > new Date(b.StartTime).getTime() ){
    return 1;
  } else if( new Date(a.StartTime).getTime() < new Date(b.StartTime).getTime() ){
    return -1;
  }
  return 0;
}
