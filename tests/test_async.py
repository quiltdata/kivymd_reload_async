from .conftest import *
from dataclasses import dataclass
import os
import httpx

TEST_HOST = "https://example.com"

class MockClient(AsyncClient):
    def __init__(self, method, route, keys=[]):

        super().__init__(route.split('/')[0], keys)
        self.method = method
        self.route = route

    async def call(self, method, route, body={}):
    	assert method == self.method
    	assert route == self.route
    	return body

    def sync_call(self, method, route, callback, body={}):
    	assert method == self.method
    	assert route == self.route
    	return body

@dataclass
class MockWidget:
    text: str

BOOK_IDS = { 'title':MockWidget("Moby"),'author':MockWidget("Melville") }

def no_callback():
	assert False


def test_httpx():
	with httpx.Client() as client:
	    r = client.get(TEST_HOST)
	print(dir(r))
	assert r.status_code == 200
	assert r.url == TEST_HOST

async def test_call(monkeypatch):
    monkeypatch.setenv('REST_ENDPOINT', TEST_HOST)
    print(os.environ['REST_ENDPOINT'])
    client = AsyncClient.Default()
    resp = await client.call('GET', '')
    assert resp.status_code == 200
    assert str(resp.url) == TEST_HOST

def test_client():
	client = AsyncClient.Default()
	assert client
	assert client.keys
	assert client.keys[0] == 'title'

def test_client_extract():
	client = AsyncClient.Default()
	book = client.ids_text(BOOK_IDS)
	book['id'] = 1
	fields = client.extract(book)
	assert fields['resource_id'] == 1
	assert fields.get('text') == book['title']
	assert fields.get('secondary_text') == book['author']


async def test_mock():
	mock = MockClient('PUT', '/')
	assert mock
	assert mock.method == 'PUT'
	assert mock.route == '/'
	result = await mock.call('PUT', '/', None)
	assert result == None

async def test_ids_text():
	mock = MockClient('POST', 'books', ['a'])
	ids = {'a': MockWidget('b')}
	result = await mock.post(ids)
	assert result.get('a') == 'b'

# fetch(f"{rest_endpoint}/ping", callback, cookie=cookie, on_error=lambda rq, rp: False)
async def test_ping():
	mock = MockClient('GET', 'ping')
	result = await mock.ping()

# fetch(f"{rest_endpoint}/login", self.login_success, method='POST', data=body, on_error=login_error)
async def test_login():
	mock = MockClient('POST', 'login')
	result = await mock.login('user', 'pw')
	assert result.get('username') == 'user'
	assert result.get('password') == 'pw'

# fetch(f"{rest_endpoint}/books", _load_data, on_error=_on_error)
async def test_get_all():
	mock = MockClient('GET', 'books')
	result = await mock.get()

async def test_get_one():
	mock = MockClient('GET', 'books/1')
	result = await mock.get(1)

# fetch(f"{rest_endpoint}/{rest_resource}", self.save_success, method=method, data=body, cookie=app.session_cookie)
async def test_post():
	mock = MockClient('POST', 'books', ['title','author'])
	result = await mock.post(BOOK_IDS)
	assert result.get('title') == 'Moby'
	assert result.get('author') == 'Melville'

async def test_put():
	mock = MockClient('PUT', 'books/1', ['title','author'])
	result = await mock.put(BOOK_IDS, 1)
	assert result.get('title') == 'Moby'
	assert result.get('author') == 'Melville'

# fetch(f"{REST_ENDPOINT}/books/{self.resource_id}", self.delete_success, method='DELETE', cookie=app.session_cookie)
async def test_delete():
	mock = MockClient('DELETE', 'books/1')
	await mock.delete(1)


