import sys
from intelxapi import intelx
import requests

class IntelXService(intelx):
    def __init__(self, api_key, user_agent):
        super().__init__(api_key, user_agent)

    def search_v2(self, term, date_from=None, date_to=None, max_results=10, buckets=[]):
        data = self.search(term, maxresults=max_results, datefrom=date_from, dateto=date_to, buckets=buckets)
        return data
    
    def get_storage_data(self, id, bucket):
        return self.FILE_VIEW(0, 0, id, bucket) 
    
    def get_storage_preview(self, id, bucket, ctype, media):
        return self.FILE_PREVIEW(ctype, media, 0, id, bucket) 
    
    def get_capabilities(self):
        return self.GET_CAPABILITIES()
    
class IdentityService(intelx):

    def __init__(self, api_key, user_agent, api_root):
        super().__init__(api_key, user_agent)
        self.API_ROOT = api_root
        self.HEADERS = {'X-Key': self.API_KEY, 'User-Agent': self.USER_AGENT}

    def get_search_results(self, id, format=1):
        params = {'id': id, 'format': format}
        r = requests.get(self.API_ROOT + '/live/search/result', params, headers=self.HEADERS)
        if r.status_code == 200:
            return r.json()
        else:
            return r.status_code

    def search(self, selector, date_from="", date_to="", limit=10, skip_invalid=False, bucket_filter=[], analyze=False, terminate=None):
        #TODO: Creo que las busquedas pueden tardar un toque, habria que mirar eso
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
        r = requests.get(self.API_ROOT + '/live/search/internal', headers=self.HEADERS, params=p)
        if r.status_code == 200:
            return r.json()['id']
        else:
            return r.status_code
        
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
    
    