from requests import Response, Session
from urllib.parse import urljoin


class BaseApiClient:

    timeout = None
    base_url = ''

    def __init__(self):
        self.http_session = Session()
        self.default_headers = {}

    def set_default_headers(self, key, value):
        self.default_headers[key] = value

    def get(self, path, params=None) -> Response:
        return self._send_request('get', path, params=params)

    def post(self, path, params) -> Response:
        return self._send_request('post', path, params=params)

    def put(self, path, params) -> Response:
        return self._send_request('put', path, params=params)

    def delete(self, path, params) -> Response:
        return self._send_request('delete', path, params=params)

    def _send_request(self, method, url, params=None) -> Response:
        req_params = {}
        headers = self.default_headers

        if method in ('post', 'put', 'delete'):
            headers['Content-Type'] = 'application/json'
            req_params['data'] = params
        if method == 'get':
            req_params['params'] = params
        req_params['headers'] = headers

        func = getattr(self.http_session, method)
        resp = func(
            url,
            timeout=self.timeout,
            **req_params,
        )
        breakpoint()
        resp.raise_for_status()
        return resp.json()


class WabaClient(BaseApiClient):
    """Rest client to access Waba services."""

    api_version = 'v21.0'
    base_url = f'https://graph.facebook.com/{api_version}/'
    timeout = 10

    def __init__(self, access_token, waba_id, phone_number_id):
        super().__init__()
        self.access_token = access_token or self.access_token
        self.waba_id = waba_id  or self.waba_id
        self.phone_number_id = phone_number_id
        self.default_headers = {
            'Authorization': 'Bearer %s' % access_token,
        }

    def get_message_templates(self):
        url = urljoin(self.base_url, f'{self.waba_id}/message_templates/')
        resp = self.get(url)
        return resp

    def create_message_template(self, data):
        url = urljoin(self.base_url, f'{self.waba_id}/message_templates')
        resp = self.post(url, data)
        return resp

    def update_message_template(self):
        ...

    def send_template_message(self, data):
        url = urljoin(self.base_url, f'{self.phone_number_id}/messages')
        resp = self.post(url, data)
        return resp

    def get_messages(self):
        # For connection testing
        url = urljoin(self.base_url, f'{self.phone_number_id}/whatsapp_business_profile?fields=about,address,description,email,profile_picture_url,websites,vertical')
        res = self.get(url)
        return res

    def get_subscriptions(self):
        # For connection testing
        url = urljoin(self.base_url, f'{self.waba_id}/subscribed_apps')
        res = self.get(url)
        return res

    def get_phone_numbers(self):
        url = urljoin(self.base_url, f'{self.waba_id}/phone_numbers')
        res = self.get(url)
        return res

    def register_phone_number(self):
        url = urljoin(self.base_url, f'{self.phone_number_id}/register')
        res = self.post(url, {})
        return res
