import datetime
import json

def dthandler(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    return None

def json_dumps(data):
    return json.dumps(data, default=dthandler)
