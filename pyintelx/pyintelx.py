import time
from intelxapi import intelx
import requests


class IdentityService(intelx):

    def __init__(self, api_key, user_agent='IX-Python/0.5', timeout=10, pause_between_requests=1):
        super().__init__(api_key, user_agent)
        self.API_ROOT = 'https://3.intelx.io'
        self.HEADERS = {'X-Key': self.API_KEY, 'User-Agent': self.USER_AGENT}
        self.TIMEOUT = timeout
        self.PAUSE_BETWEEN_REQUESTS = pause_between_requests

    def get_search_results(self, id, format=1, maxresults=100):
        params = {'id': id, 'format': format, 'limit': maxresults}
        try:
            # Solicitud HTTP con timeout
            r = requests.get(self.API_ROOT + '/live/search/result',
                             params=params, headers=self.HEADERS, timeout=self.TIMEOUT)
            r.raise_for_status()  # Lanzará una excepción si el código no es 200

            return r.json()  # Devolver JSON si la solicitud es exitosa
        except requests.exceptions.HTTPError as errh:
            print("Error HTTP:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error de conexión:", errc)
        except requests.exceptions.Timeout as errt:
            print("Tiempo de espera agotado:", errt)
        except requests.exceptions.RequestException as err:
            print("Error en la solicitud:", err)
        return None  # Retorna None si ocurre un error

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

        try:
            r = requests.get(self.API_ROOT + '/live/search/internal',
                             headers=self.HEADERS, params=p, timeout=self.TIMEOUT)
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("Error HTTP:", errh)
            return (r.status_code, r.text)
        except requests.exceptions.ConnectionError as errc:
            print("Error de conexión:", errc)
            return "Error de conexión"
        except requests.exceptions.Timeout as errt:
            print("Tiempo de espera agotado:", errt)
            return "Tiempo de espera agotado"
        except requests.exceptions.RequestException as err:
            print("Error en la solicitud:", err)
            return "Error en la solicitud"

        search_id = r.json().get('id')
        if len(str(search_id)) <= 3:
            print(f"[!] intelx.IDENTITY_SEARCH() Received {self.get_error(search_id)}")

        while not done:
            time.sleep(self.PAUSE_BETWEEN_REQUESTS)
            r = self.get_search_results(search_id, maxresults=maxresults)
            if r and r.get("status") == 0 and r.get("records"):
                results.extend(r['records'])
                maxresults -= len(r['records'])

            if r and (r.get("status") == 2 or maxresults <= 0):
                if maxresults <= 0:
                    self.terminate_search(search_id)
                done = True
        return {'records': results}

    def terminate_search(self, id):
        p = {
            "id": id,
        }
        try:
            r = requests.get(self.API_ROOT + '/live/search/terminate',
                             headers=self.HEADERS, params=p, timeout=self.TIMEOUT)
            r.raise_for_status()
            return (r.status_code, r.text)
        except requests.exceptions.HTTPError as errh:
            print("Error HTTP:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error de conexión:", errc)
        except requests.exceptions.Timeout as errt:
            print("Tiempo de espera agotado:", errt)
        except requests.exceptions.RequestException as err:
            print("Error en la solicitud:", err)
        return None  # Retorna None si ocurre un error

    def export_accounts(self, term, datefrom=None, dateto=None, maxresults=10, buckets=[], terminate=None):
        p = {
            "selector": term,
            "bucket": buckets,
            "limit": maxresults,
            "datefrom": datefrom,  # "YYYY-MM-DD HH:MM:SS"
            "dateto": dateto,      # "YYYY-MM-DD HH:MM:SS"
            "terminate": terminate,
        }
        
        # Limpiar parámetros opcionales que sean None
        p = {k: v for k, v in p.items() if v is not None}

        done = False
        results = []
   
        try:
            # Primera solicitud a /accounts/csv con timeout
            r = requests.get(self.API_ROOT + '/accounts/csv',
                             headers=self.HEADERS, params=p, timeout=self.TIMEOUT)
            r.raise_for_status()  # Verifica si la solicitud fue exitosa (código 200)

            search_id = r.json().get('id')  # Obtiene el ID de la búsqueda
            if not search_id or len(str(search_id)) <= 3:
                print(f"[!] intelx.IDENTITY_EXPORT() Received {self.get_error(search_id)}")
                return

            # Loop para obtener resultados de búsqueda
            while not done:
                time.sleep(self.PAUSE_BETWEEN_REQUESTS)
                r = self.get_search_results(search_id, maxresults=maxresults)

                if r and r.get("status") == 0 and r.get("records"):
                    results.extend(r['records'])
                    maxresults -= len(r['records'])

                # Si el estado es 2 o se alcanzan los resultados deseados, termina la búsqueda
                if r and (r.get("status") == 2 or maxresults <= 0):
                    if maxresults <= 0:
                        self.terminate_search(search_id)
                    done = True

            return {'records': results}

        except requests.exceptions.HTTPError as errh:
            print("Error HTTP:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error de conexión:", errc)
        except requests.exceptions.Timeout as errt:
            print("Tiempo de espera agotado:", errt)
        except requests.exceptions.RequestException as err:
            print("Error en la solicitud:", err)

        return None  # Retorna None si ocurre un error
   
   

    def export_csv(self, selector, date_from=None, date_to=None, limit=10, bucket_filter=[], terminate=None):
        p = {
            "selector": selector,
            "bucket": bucket_filter,
            "limit": limit,
            "datefrom": date_from,  # "YYYY-MM-DD HH:MM:SS",
            "dateto": date_to,  # "YYYY-MM-DD HH:MM:SS"
            "terminate": terminate,
        }
       try:
            r = requests.get(self.API_ROOT + '/accounts/csv',
                             headers=self.HEADERS, params=p, timeout=self.TIMEOUT)
            r.raise_for_status()  # Verifica si la solicitud fue exitosa (código 200)
            return r.json().get('id')  # Devuelve el 'id' si la solicitud es exitosa
        except requests.exceptions.HTTPError as errh:
            print("Error HTTP:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error de conexión:", errc)
        except requests.exceptions.Timeout as errt:
            print("Tiempo de espera agotado:", errt)
        except requests.exceptions.RequestException as err:
            print("Error en la solicitud:", err)
        return None  # Retorna None si ocurre un error