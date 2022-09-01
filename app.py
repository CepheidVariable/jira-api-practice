import json
import logging
import os

import requests
from requests.auth import HTTPBasicAuth

import JIRA_CREDS

# logger setup
logging.basicConfig(
    level= logging.INFO,
    format='%(levelname)s: %(asctime)s: [%(filename)s:%(lineno)s - %(funcName)s()]: %(message)s'
)

URL = 'https://cepheidvariable.atlassian.net/rest/api/latest'
AUTH = HTTPBasicAuth(JIRA_CREDS.ATLASSIAN_USER, JIRA_CREDS.ATLASSIAN_TOKEN)
PATH = os.path.dirname(__file__)

def get_issue(issue_key: str) -> None:
    '''Makes a GET request to the Jira Cloud API to retrieve issue using 'issue_key' passed in as String. Logs response to stdout.'''

    headers = {
        "Accept": "application/json"
    }

    res = requests.get(f'{URL}/issue/{issue_key}', headers=headers, auth=AUTH)

    if res.status_code == 200:
        data = json.loads(res.text)
        logging.info(json.dumps({
            "code": res.status_code,
            "success": True,
            "message": data['self']
        }))
    else:
        msg = {
            "code": res.status_code,
            "success": False
        }
        
        data = json.loads(res.text)

        for key in data:
            msg.update({key: data[key]})

        logging.warning(json.dumps(msg))
    
    return

def add_attachments(issue_key: str) -> None:
    '''Makes a POST request to the Jira Cloud API to add attachments to 'issue_key' passed in as String. Logs response to stdout.'''
    headers = {
        "Accept": "application/json",
        "X-Atlassian-Token": "no-check"
    }

    files = (
        ("file", ("text.txt", open(PATH + "/uploads/text.txt","rb"), "application-type")),
        ("file", ("payload.json", open(PATH + "/uploads/payload.json","rb"), "application-type")),
    )

    res = requests.post(f'{URL}/issue/{issue_key}/attachments', headers=headers, auth=AUTH, files=files)
    
    if res.status_code == 200 or res.status_code == 204:
        attachments = []
        
        data = json.loads(res.text)
        
        for item in data:
            attachments.append(item['self'])

        logging.info(json.dumps({
            "code": res.status_code,
            "success": True,
            "attachments": attachments
        }))
    else:
        msg = {
            "code": res.status_code,
            "success": False
        }
        
        data = json.loads(res.text)

        for key in data:
            msg.update({key: data[key]})

        logging.warning(json.dumps(msg))

    return

def main():
    get_issue('DOP-10')
    add_attachments('DOP-a11')

    return

if __name__ == '__main__':
    main()
    logging.info('Exiting script.')