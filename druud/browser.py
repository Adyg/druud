import requests

class DruudBrowser:

    def __init__(self, config):
        self.config = config
        self.auth = None
        self.headers = None
        self.payload = config['payload']

        if self.config['http_auth_username'] and self.config['http_auth_password']:
            self.auth = (self.config['http_auth_username'], self.config['http_auth_password'])

        if self.config['headers']:
            self.headers = self.config['headers']

    def get_request(self):
        payload = {}

        for param in self.payload:
            payload[param.key] = param.value

        response = self.send_request('get', self.config['url'], headers=self.headers, auth=self.auth, params=payload)

        return response

    def head_request(self):
        response = self.send_request('head', self.config['url'], headers=self.headers, auth=self.auth)

        return response

    def send_request(self, request_type, url, **args):
        response = False
        request_info = {
            'status': False,
            'elapsed': 0,
            'error': 0,
            'error_message': '',
        }

        try:
            if request_type == 'head':
                response = requests.head(url, **args)
            elif request_type == 'get':
                response = requests.get(url, **args)

            request_info['status'] = response.ok
            request_info['elapsed'] = response.elapsed.total_seconds()
            request_info['status_code'] = response.status_code

        except requests.exceptions.RequestException, e:
            request_info['error'] = 1
            request_info['error_message'] = str(e)
        except requests.exceptions.HTTPError, e:
            request_info['error'] = 2
            request_info['error_message'] = str(e)
        except requests.exceptions.ConnectionError, e:
            request_info['error'] = 3
            request_info['error_message'] = str(e)
        except requests.exceptions.ProxyError, e:
            request_info['error'] = 4
            request_info['error_message'] = str(e)
        except requests.exceptions.SSLError, e:
            request_info['error'] = 5
            request_info['error_message'] = str(e)
        except requests.exceptions.ConnectTimeout, e:
            request_info['error'] = 6
            request_info['error_message'] = str(e)
        except requests.exceptions.ReadTimeout, e:
            request_info['error'] = 7
            request_info['error_message'] = str(e)
        except requests.exceptions.TooManyRedirects, e:
            request_info['error'] = 8
            request_info['error_message'] = str(e)
        except requests.exceptions.InvalidURL, e:
            request_info['error'] = 9
            request_info['error_message'] = str(e)
        except requests.exceptions.ChunkedEncodingError, e:
            request_info['error'] = 10
            request_info['error_message'] = str(e)
        except requests.exceptions.ContentDecodingError, e:
            request_info['error'] = 11
            request_info['error_message'] = str(e)
        except:
            request_info['error'] = 12

        return request_info
