import sys
import argparse
import logging
import datetime
import csv

import anticrlf
from veracode_api_py import VeracodeAPI as vapi

log = logging.getLogger(__name__)

def setup_logger():
    handler = logging.FileHandler('vcappprofiles.log', encoding='utf8')
    handler.setFormatter(anticrlf.LogFormatter('%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'))
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

def creds_expire_days_warning():
    creds = vapi().get_creds()
    exp = datetime.datetime.strptime(creds['expiration_ts'], "%Y-%m-%dT%H:%M:%S.%f%z")
    delta = exp - datetime.datetime.now().astimezone() #we get a datetime with timezone...
    if (delta.days < 7):
        print('These API credentials expire ', creds['expiration_ts'])

def get_all_apps():
    applist = vapi().get_apps()
    return applist

def get_app(app_guid):
    return vapi().get_app(app_guid)

def list_to_string(l):
    separator = ', '
    return (separator.join(l))

def write_apps_to_csv(apps):
    status = 'Writing application profiles to vcappprofiles.csv'
    print(status)
    log.info(status)
    fields = [ 'app_guid','app_legacy_id','app_name','last_completed_scan_date','created','modified','url','tags','business_criticality',
                'policy_name','policy_compliance_status','results_url','teams','business_unit','business_owners','archer_app_name',
                'nextday_consultation_allowed','static_scan_dependencies_allowed']

    with open("vcappprofiles.csv", "w", newline='') as f:
        w = csv.DictWriter(f, fields)
        w.writeheader()
        for a in apps:
            p = a.get('profile')
            pl = p.get('policies')[0]
            s = p.get('settings')
            teams = p.get('teams')
            team_list = []
            for t in teams:
                team_list.append(t.get('team_name'))
            # this method does not include custom fields. it can be expanded as follows:
            # c = p.get('custom_fields')
            # c1 = next((item for item in c if item["name"] == "<Custom Field 1>"), None) 
            # c1_value = c1.get('value')
            # Then add a header to fields above, and write '<header>': c1_value below

            w.writerow({'app_guid': a.get('guid'), 'app_legacy_id': a.get('id'), 'app_name': p.get('name'),
                'last_completed_scan_date': a.get('last_completed_scan_date'), 'created': a.get('created'),
                'modified': a.get('modified'), 'url': a.get('app_profile_url'), 'tags': p.get('tags'),
                'business_criticality': p.get('business_criticality'),'policy_name': pl.get('name'),
                'policy_compliance_status': pl.get('policy_compliance_status'),'results_url': a.get('results_url'),
                'teams': list_to_string(team_list), 'business_unit': p.get('business_unit').get('name'),
                'business_owners': p.get('business_owners'),'archer_app_name': p.get('archer_app_name'),
                'nextday_consultation_allowed': s.get('nextday_consultation_allowed'), 
                'static_scan_dependencies_allowed': s.get('static_scan_dependencies_allowed')})

def log_and_print(message):
    log.info(message)
    print(message)

def main():
    parser = argparse.ArgumentParser(
        description='This script exports application profile information to csv.')
    parser.add_argument('-a', '--application', required=False, help='Application guid to export.')
    parser.add_argument('--all', '-l',action='store_true', help='Export all applications.')
    args = parser.parse_args()

    appguid = args.application
    checkall = args.all
    setup_logger()

    # CHECK FOR CREDENTIALS EXPIRATION
    creds_expire_days_warning()

    appcount=0
    applist = []
    
    if checkall:
        log_and_print("Getting application list…")
        applist = get_all_apps()
        log_and_print("Exporting {} applications to csv…".format(len(applist)))
        
    elif appguid != None:
        log_and_print("Exporting application {} to csv…".format(appguid))
        applist.append (get_app(appguid))
    else:
        print('You must either provide an application guid or check all applications.')
        return

    appcount = len(applist)
    write_apps_to_csv(applist)

    print("Exported {} applications to vcappprofiles.csv".format(appcount))
    log.info("Exported {} applications to vcappprofiles.csv.".format(appcount))
    
if __name__ == '__main__':
    main()