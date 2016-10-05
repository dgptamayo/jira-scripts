#!/usr/bin/python
'''
SYNOPSIS
    bulk-delete-components.py [-u, --username] [-k, --key]

DESCRIPTION
    Removes all Components of a JIRA Project based on the passed project key. 
    Uses JIRA REST API (tested using API v6.3.4)
'''
import sys, argparse, getpass, json, requests
from requests.auth import HTTPDigestAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from requests import Session, exceptions

# DEFINE JIRA URL
jiraurl = ''

# main module - define what the script needs to do
def main(args, password):

    # get the JIRA project data, check if key is valid
    try:
        jiraResponse = s.get(jiraurl + '/rest/api/2/project/' + args.key, auth = (args.username, password), verify = False)
        jiraResponse.raise_for_status()
    except requests.exceptions.HTTPError as err:
        # display error and exit
        print err
        sys.exit(1)
    
    # process project data
    projectData = json.loads(jiraResponse.content)

    # extract the project components
    projectComponents = projectData['components']
    print "Deleting " + str(len(projectComponents)) + " components"

    # iterate thru each component, get the id and delete it
    for component in projectComponents:
        print "Deleting " + component['id'] + " " + component['name']
        try:
            r = s.delete(jiraurl + '/rest/api/2/component/' + component['id'], auth = (args.username, password), verify = False)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            # display error and exit - most likely authorization problem
            print err
            sys.exit(1)
            
    # inform completion
    print "Bulk component removal complete"

# Define script entry-point and parameters
if __name__ == "__main__":
    # check if JIRA instance URL is defined
    if not jiraurl:
        print "JIRA URL not defined. Edit this script and enter the details"
        sys.exit(1)

    # define required paramaters
    parser = argparse.ArgumentParser(
            description = "Bulk deletion of components in a JIRA project"
            )
    parser.add_argument(
            "-u", "--username", help = "JIRA username", required = True
            )
    parser.add_argument(
            "-k", "--key", help = "JIRA Project Key", required = True
            )
    args = parser.parse_args()
    
    # Password
    password = getpass.getpass()

    # disable SSL verication warnings
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    # define HTTP session retries
    s = Session()
    s.mount('https://', HTTPAdapter(max_retries=Retry(total=5)))
        
    main(args, password)

