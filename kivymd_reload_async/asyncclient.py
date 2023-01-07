import os
import httpx
import trio
from kivymd.app import MDApp

class AsyncClient():

    def Default():
        resource = os.environ['REST_RESOURCE']
        keys = os.environ['REST_KEYS'].split(',')
        return AsyncClient(resource, keys)

    def __init__(self, resource, id_keys):
        self.resource = resource
        self.keys = id_keys # Name Detail

    def extract(self, data):
        FIELDS = ['text','secondary_text', 'resource_id']
        values = [data[k] for k in self.keys]
        fields = dict(zip(FIELDS, values))
        fields[FIELDS[2]] = data['id']
        return fields

    def ids_text(self, ids):
        return {k: ids[k].text for k in self.keys}

    async def ping(self):
        url = 'ping'
        return await self.call('GET', url)

    async def login(self, username, password):
        options = {'username': username, 'password': password}
        url = 'login'
        return await self.call('POST', url, options)

    async def logout(self):
        url = 'logout'
        return await self.call('POST', url)

    async def get(self, resource_id=None, **kwargs):
        url = f"{self.resource}/{resource_id}" if resource_id else self.resource 
        return await self.call('GET', url, kwargs)

    async def post(self, ids,**kwargs):
        options = self.ids_text(ids) | kwargs
        url = self.resource
        return await self.call('POST', url, options)

    async def put(self, ids, resource_id, **kwargs):
        options = self.ids_text(ids) | kwargs
        options['id'] = resource_id
        url = f"{self.resource}/{resource_id}"
        return await self.call('PUT', url, options)

    async def delete(self, resource_id, **kwargs):
        url = f"{self.resource}/{resource_id}"
        return await self.call('DELETE', url)

    def sync_call(self, method, route, options={}):
        endpoint = os.environ['REST_ENDPOINT']
        app = MDApp.get_running_app()
        url = f"{endpoint}/{route}"
        params = {
            'method': method,
            'options': options,
            'cookie': app.session_cookie,
        } | options
        return fetch(url, **params)

    async def call(self, method, route, options={}):
        endpoint = os.environ['REST_ENDPOINT']
        app = MDApp.get_running_app()
        url = f"{endpoint}/{route}" if len(route) > 0 else endpoint
        print('url', url)
        options['cookies'] = app.session_cookie
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, **options)
            return response
        return True
