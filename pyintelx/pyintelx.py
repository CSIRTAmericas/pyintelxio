import time
from intelxapi import intelx
import requests


class IdentityService(intelx):

    def __init__(self, api_key, user_agent='IX-Python/0.5'):
        super().__init__(api_key, user_agent)
        self.API_ROOT = 'https://3.intelx.io'
        self.HEADERS = {'X-Key': self.API_KEY, 'User-Agent': self.USER_AGENT}

    def get_search_results(self, id, format=1, maxresults=100):
        params = {'id': id, 'format': format, 'limit': maxresults}
        r = requests.get(self.API_ROOT + '/live/search/result',
                         params, headers=self.HEADERS)
        if r.status_code == 200:
            return r.json()
        else:
            return r.status_code

    def search(self, term, maxresults=100, buckets=[], timeout=5, datefrom="", dateto="",
               terminate=[], analyze=False, skip_invalid=False):
        p = {
            "selector": term,
            "bucket": buckets,
            "skipinvalid": skip_invalid,
            "limit": maxresults,
            "analyze": analyze,
            "datefrom": datefrom,  # "YYYY-MM-DD HH:MM:SS",
            "dateto": dateto,  # "YYYY-MM-DD HH:MM:SS"
            "terminate": terminate,
        }
        done = False
        results = []
        r = requests.get(self.API_ROOT + '/live/search/internal',
                         headers=self.HEADERS, params=p)
        if r.status_code == 200:
            search_id = r.json()['id']
        else:
            return (r.status_code, r.text)
        if (len(str(search_id)) <= 3):
            print(
                f"[!] intelx.IDENTITY_SEARCH() Received {self.get_error(search_id)}")
        while not done:
            time.sleep(1)
            r = self.get_search_results(search_id, maxresults=maxresults)
            if (r["status"] == 0 and r["records"]):
                for a in r['records']:
                    results.append(a)
                maxresults -= len(r['records'])
            if (r['status'] == 1 or r['status'] == 2 or maxresults <= 0):
                if (maxresults <= 0):
                    self.terminate_search(search_id)
                done = True
        return {'records': results}

    def terminate_search(self, id):
        p = {
            "id": id,
        }
        r = requests.get(self.API_ROOT + '/live/search/internal',
                         headers=self.HEADERS, params=p)
        if r.status_code == 204:
            return (r.status_code, r.text)
        else:
            return (r.status_code, r.text)

    def export_csv(self, selector, date_from=None, date_to=None, limit=10, bucket_filter=[], terminate=None):
        p = {
            "selector": selector,
            "bucket": bucket_filter,
            "limit": limit,
            "datefrom": date_from,  # "YYYY-MM-DD HH:MM:SS",
            "dateto": date_to,  # "YYYY-MM-DD HH:MM:SS"
            "terminate": terminate,
        }
        r = requests.get(self.API_ROOT + '/accounts/csv',
                         headers=self.HEADERS, params=p)
        if r.status_code == 200:
            return r.json()['id']
        else:
            return (r.status_code, r.text)
