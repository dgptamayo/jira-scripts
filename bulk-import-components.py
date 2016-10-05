#!/usr/bin/python
'''
SYNOPSIS
    bulk-import-components.py [-u, --username] [-k, --key] [csv file]

DESCRIPTION
    Reads a csv list of components and imports them to a JIRA Project 
    based on the passed project key. 
    Uses JIRA REST API (tested using API v6.3.4)
'''
import sys, argparse, getpass, json, requests, csv
from requests.auth import HTTPDigestAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from requests import Session, exceptions

# DEFINE JIRA URL
jiraurl = ''

# main module - define what the script needs to do
def main(args, password):
    # get the JIRA project data
    try:
        jiraResponse = s.get(jiraurl + '/rest/api/2/project/' + args.key, auth = (args.username, password), verify=False)
        jiraResponse.raise_for_status()
    except requests.exceptions.HTTPError as err:
        # display error and exit
        print err
        sys.exit(1)

    headers = {'Content-Type': 'application/json'}
    
    # open the csv file
    with open(args.csv, 'rb') as f:
        reader = csv.reader(f)
        try:
            # iterate thru each record
            for row in reader:
                print "Adding " + row[0]
                try:
                    data = {'name': row[0], 'project': args.key}
                    r = s.post(jiraurl + '/rest/api/2/component', data = json.dumps(data), headers = headers, auth = (args.username, password), verify = False)
                    r.raise_for_status()
                except requests.exceptions.HTTPError as err:
                    # display error and exit
                    print err
                    sys.exit(1)
                            
        except csv.Error as e:
            sys.exit('File %s, line %d: %s' % (args.csv, reader.line_num, e))
        finally:
            # close the file
            f.close()


# Define script entry-point and parameters
if __name__ == "__main__":
    # check if JIRA instance URL was defined
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
    parser.add_argument(
            "csv", help = "CSV file"
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

