import sys
import time
from intelxapi import intelx
import requests

class IdentityService(intelx):

    def __init__(self, api_key, user_agent, api_root):
        super().__init__(api_key, user_agent)
        self.API_ROOT = 'https://3.intelx.io'
        self.HEADERS = {'X-Key': self.API_KEY, 'User-Agent': self.USER_AGENT}

    def get_search_results(self, id, format=1):
        params = {'id': id, 'format': format}
        r = requests.get(self.API_ROOT + '/live/search/result', params, headers=self.HEADERS)
        if r.status_code == 200:
            return r.json()
        else:
            return r.status_code

    def search(self, selector, date_from="", date_to="", limit=10, skip_invalid=False, bucket_filter=[], analyze=False, terminate=None):
        p = {
            "selector": selector,
            "bucket": bucket_filter,
            "skipinvalid": skip_invalid,
            "limit": limit,
            "analyze": analyze,
            "datefrom": date_from, # "YYYY-MM-DD HH:MM:SS",
            "dateto": date_to, # "YYYY-MM-DD HH:MM:SS"
            "terminate": terminate,
        }
        done = False
        results = []
        r = requests.get(self.API_ROOT + '/live/search/internal', headers=self.HEADERS, params=p)
        if r.status_code == 200:
            search_id = r.json()['id']
        if(len(str(search_id)) <= 3):
            print(f"[!] intelx.IDENTITY_SEARCH() Received {self.get_error(search_id)}")
        while done == False:
            time.sleep(1)
            r = self.get_search_results(search_id, limit=limit)
            for a in r['records']:
                results.append(a)
            limit -= len(r['records'])
            if(r['status'] == 1 or r['status'] == 2 or limit <= 0):
                if(limit <= 0):
                    self.terminate_search(search_id)
                done = True
        return {'records': results}
        
    def terminate_search(self, id):
        p = {
            "id": id,
        }
        r = requests.get(self.API_ROOT + '/live/search/internal', headers=self.HEADERS, params=p)
        if r.status_code == 204:
            return (r.status_code, r.text)
        else:
            return (r.status_code, r.text)
        
    def export_csv(self, selector, date_from=None, date_to=None, limit=10, bucket_filter=[], terminate=None):
        p = {
            "selector": selector,
            "bucket": bucket_filter,
            "limit": limit,
            "datefrom": date_from, # "YYYY-MM-DD HH:MM:SS",
            "dateto": date_to, # "YYYY-MM-DD HH:MM:SS"
            "terminate": terminate,
        }
        r = requests.get(self.API_ROOT + '/accounts/csv', headers=self.HEADERS, params=p)
        if r.status_code == 200:
            return r.json()['id']
        else:
            return (r.status_code, r.text)
    
    