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

    def get_search_results(self, search_id, search_format=1, maxresults=100):
        ''' This functions return search_results from a search_id '''
        params = {'id': search_id, 'format': search_format, 'limit': maxresults}
        try:
            # Solicitud HTTP con timeout
            response = requests.get(self.API_ROOT + '/live/search/result',
                             params=params, headers=self.HEADERS, timeout=self.TIMEOUT)
            response.raise_for_status()  # Lanzará una excepción si el código no es 200

            return response.json()  # Devolver JSON si la solicitud es exitosa
        except requests.exceptions.HTTPError as errh:
            print("Error HTTP:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error de conexión:", errc)
        except requests.exceptions.Timeout as errt:
            print("Tiempo de espera agotado:", errt)
        except requests.exceptions.RequestException as err:
            print("Error en la solicitud:", err)
        return None  # Retorna None si ocurre un error

    def search(self, term, maxresults=100, buckets=None, datefrom="", dateto="",
               terminate=None, analyze=False, skip_invalid=False):
        if buckets is None:
            buckets = []
        if terminate is None:
            terminate = []
        search_params = {
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
            response = requests.get(self.API_ROOT + '/live/search/internal',
                             headers=self.HEADERS, params=search_params, timeout=self.TIMEOUT)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("Error HTTP:", errh)
            return (response.status_code, response.text)
        except requests.exceptions.ConnectionError as errc:
            print("Error de conexión:", errc)
            return "Error de conexión"
        except requests.exceptions.Timeout as errt:
            print("Tiempo de espera agotado:", errt)
            return "Tiempo de espera agotado"
        except requests.exceptions.RequestException as err:
            print("Error en la solicitud:", err)
            return "Error en la solicitud"

        search_id = response.json().get('id')
        if len(str(search_id)) <= 3:
            print(f"[!] intelx.IDENTITY_SEARCH() Received {self.get_error(search_id)}")

        while not done:
            time.sleep(self.PAUSE_BETWEEN_REQUESTS)
            response = self.get_search_results(search_id, maxresults=maxresults)
            if response and response.get("status") == 0 and response.get("records"):
                results.extend(response['records'])
                maxresults -= len(response['records'])

            if response and (response.get("status") == 2 or maxresults <= 0):
                if maxresults <= 0:
                    self.terminate_search(search_id)
                done = True
        return {'records': results}

    def terminate_search(self, search_id):
        search_params = {
            "id": search_id,
        }
        try:
            response = requests.get(self.API_ROOT + '/live/search/terminate',
                             headers=self.HEADERS, params=search_params, timeout=self.TIMEOUT)
            response.raise_for_status()
            return (response.status_code, response.text)
        except requests.exceptions.HTTPError as errh:
            print("Error HTTP:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error de conexión:", errc)
        except requests.exceptions.Timeout as errt:
            print("Tiempo de espera agotado:", errt)
        except requests.exceptions.RequestException as err:
            print("Error en la solicitud:", err)
        return None  # Retorna None si ocurre un error

    def export_accounts(self, term, datefrom=None, dateto=None, maxresults=10,
                        buckets=None, terminate=None):
        if buckets is None:
            buckets = []
        search_params = {
            "selector": term,
            "bucket": buckets,
            "limit": maxresults,
            "datefrom": datefrom,  # "YYYY-MM-DD HH:MM:SS"
            "dateto": dateto,      # "YYYY-MM-DD HH:MM:SS"
            "terminate": terminate,
        }
        # Limpiar parámetros opcionales que sean None
        search_params = {k: v for k, v in search_params.items() if v is not None}
        done = False
        results = []

        try:
            # Primera solicitud a /accounts/csv con timeout
            response = requests.get(self.API_ROOT + '/accounts/csv',
                             headers=self.HEADERS, params=search_params, timeout=self.TIMEOUT)
            response.raise_for_status()  # Verifica si la solicitud fue exitosa (código 200)

            search_id = response.json().get('id')  # Obtiene el ID de la búsqueda
            if not search_id or len(str(search_id)) <= 3:
                print(f"[!] intelx.IDENTITY_EXPORT() Received {self.get_error(search_id)}")

            # Loop para obtener resultados de búsqueda
            while not done:
                time.sleep(self.PAUSE_BETWEEN_REQUESTS)
                response = self.get_search_results(search_id, maxresults=maxresults)

                if response and response.get("status") == 0 and response.get("records"):
                    results.extend(response['records'])
                    maxresults -= len(response['records'])

                # Si el estado es 2 o se alcanzan los resultados deseados, termina la búsqueda
                if response and (response.get("status") == 2 or maxresults <= 0):
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

    def export_csv(self, selector, date_from=None, date_to=None, limit=10, bucket_filter=None,
                   terminate=None):
        if bucket_filter is None:
            bucket_filter = []
        search_params = {
            "selector": selector,
            "bucket": bucket_filter,
            "limit": limit,
            "datefrom": date_from,  # "YYYY-MM-DD HH:MM:SS",
            "dateto": date_to,  # "YYYY-MM-DD HH:MM:SS"
            "terminate": terminate,
        }
        try:
            response = requests.get(self.API_ROOT + '/accounts/csv',
                             headers=self.HEADERS, params=search_params, timeout=self.TIMEOUT)
            response.raise_for_status()  # Verifica si la solicitud fue exitosa (código 200)
            return response.json().get('id')  # Devuelve el 'id' si la solicitud es exitosa
        except requests.exceptions.HTTPError as errh:
            print("Error HTTP:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error de conexión:", errc)
        except requests.exceptions.Timeout as errt:
            print("Tiempo de espera agotado:", errt)
        except requests.exceptions.RequestException as err:
            print("Error en la solicitud:", err)
        return None  # Retorna None si ocurre un error
