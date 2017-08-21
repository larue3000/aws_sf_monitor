import boto3
from datetime import date, datetime

client = boto3.client('stepfunctions')

# https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable
def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def get_executions(stateMachineArn, maxResults=1):
    results = {}
    for state in ['RUNNING', 'SUCCEEDED', 'FAILED', 'TIMED_OUT', 'ABORTED']:
        results.update({
            state: client.list_executions(
                stateMachineArn=stateMachineArn,
                statusFilter=state,
                maxResults=maxResults
            )
        })
    return results

def get_timestamp(results, status):
    ts = datetime(2017, 1, 1, 0, 0, 0)
    if len(results[status]["executions"]) > 0:
        try:
            ts = results[status]["executions"][0]['stopDate']
        except Exception as e:
            ts = datetime.now()
    return ts.isoformat()

def get_status(stateMachineArn):
    results = get_executions(stateMachineArn)
    statuses = {
        'RUNNING': get_timestamp(results, 'RUNNING'),
        'SUCCEEDED': get_timestamp(results, 'SUCCEEDED'),
        'FAILED': get_timestamp(results, 'FAILED'),
        'TIMED_OUT': get_timestamp(results, 'TIMED_OUT'),
        'ABORTED': get_timestamp(results, 'ABORTED')
    }
    return {
        'stateMachineArn': stateMachineArn,
        'status': max(statuses, key=statuses.get)
    }


