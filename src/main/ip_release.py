import json
import boto3
import os
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from main.log import Logger

#from main.util import validate_json_with_schema, allow_ip_on_waf
ip_sets = os.getenv('ip_sets', 'waf.json')

LOGGER = Logger()
schema = {
    "type": "object",
    "required": ["action", "location", "ip"],
    "properties" : {
        "action" : {"type" : "string"},
        "location" : {"type" : "string"},
        "ip" : {"type" : "string"},
    }
}

def ip_release_handler(event):

    if validate_json_with_schema(event):
        changed_wafs = allow_ip_on_waf(event)    
        return changed_wafs
    else:
        return {'action': 'waf', 'message': 'Error with JSON'}

def validate_json_with_schema(json_input):
    try:
        validate(instance=json_input,schema=schema)
        LOGGER.info('JSON Input is valid')
        return True
    except ValidationError as exception:
        LOGGER.error(exception)
        return False

def allow_ip_on_waf(event):
    with open(ip_sets) as f:
        ip_sets_json = json.load(f)
        LOGGER.info('%s will perform changes on Global WAF', event['location'])
        waf_global = boto3.client('waf')
        global_token = waf_global.get_change_token()
        waf_global.update_ip_set(
            IPSetId=ip_sets_json[event['location']]['GlobalId'],
            ChangeToken=global_token['ChangeToken'],
            Updates=[
                {
                    'Action': 'INSERT',
                    'IPSetDescriptor': {
                        'Type': 'IPV4',
                        'Value': event['ip']
                    }
                }
            ]
            )

        if 'RegionalId' in ip_sets_json[event['location']]:
            LOGGER.info('%s will perform changes on Regional WAF', event['location'])
            waf_regional = boto3.client('waf-regional')
            regional_token = waf_regional.get_change_token()
            waf_regional.update_ip_set(
                IPSetId=ip_sets_json[event['location']]['RegionalId'],
                ChangeToken=regional_token['ChangeToken'],
                Updates=[
                    {
                        'Action': 'INSERT',
                        'IPSetDescriptor': {
                            'Type': 'IPV4',
                            'Value': event['ip']
                        }
                    }
                ]
                )
        return {'action': 'waf', 'message': 'IP {} allowed on WAF'.format(event['ip'])}