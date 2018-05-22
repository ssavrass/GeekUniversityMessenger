import sys

import pytest

import mock

import socket

from server import EchoServer

from client import EchoClient

from jsonformat.jimprotocolserver import JSONRequest, JSONResponse


@pytest.fixture
def client_host():

    return 'localhost'


@pytest.fixture
def client_port():

    return 8000
    

@pytest.fixture
def client_address(client_host, client_port):

    return client_host, client_port


@pytest.fixture
def clients_number():

    return 10


@pytest.fixture
def server_timeout():

    return 0

@pytest.fixture
def connect_message():

    return 'socket bind successfully'

@pytest.fixture
def JSON_bytes():
    JSONbytes = JSONResponse('code',"action","body").to_bytes()
    return JSONbytes

@pytest.fixture
def JSON_bytessend():
    JSONbytessend = JSONResponse('code',"server received message from client","body").to_bytes()
    return JSONbytessend

@pytest.fixture
def message():
    return 'body'

@pytest.fixture
def JSON_read():
    
    return "'action': 'action'"

@pytest.fixture
def mocked_connect(connect_message, monkeypatch):

    def mock_connect(self, *args, **kwargs):

        print(connect_message)

    monkeypatch.setattr(socket.socket, 'connect', mock_connect)

@pytest.fixture
def mocked_send(JSON_bytes, monkeypatch):

    def mock_send(self, *args, **kwargs):

        return JSON_bytes

    monkeypatch.setattr(socket.socket, 'send', mock_send)    

@pytest.fixture
def mocked_recv(JSON_bytes, monkeypatch):

    def mock_recv(self, *args, **kwargs):

        return JSON_bytes

    monkeypatch.setattr(socket.socket, 'recv', mock_recv)

@pytest.fixture
def mocked_request(JSON_bytes):

    return JSONRequest(JSON_bytes)


@pytest.fixture
def mocked_recvsend(JSON_bytessend, monkeypatch):

    def mock_recv(self, *args, **kwargs):

        return JSON_bytessend

    monkeypatch.setattr(socket.socket, 'recv', mock_recv) 


@mock.patch('socket.socket.bind')
@mock.patch('socket.socket.listen')
@mock.patch('socket.socket.settimeout')
def test_bind(mocked_settimeout, mocked_listen, mocked_bind, client_address):

    EchoServer()

    mocked_bind.assert_called_once_with(client_address)


@mock.patch('socket.socket.bind')
@mock.patch('socket.socket.listen')
@mock.patch('socket.socket.settimeout')
def test_listen(mocked_settimeout, mocked_listen, mocked_bind, clients_number):

    EchoServer()

    mocked_listen.assert_called_once_with(clients_number)


@mock.patch('socket.socket.bind')
@mock.patch('socket.socket.listen')
@mock.patch('socket.socket.settimeout')
def test_settimeout(mocked_settimeout, mocked_listen, mocked_bind, server_timeout):

    EchoServer()

    mocked_settimeout.assert_called_once_with(server_timeout)


@mock.patch('socket.socket.bind')
@mock.patch('socket.socket.listen')
@mock.patch('socket.socket.settimeout')
@mock.patch('socket.socket.accept')
def test_connect(mocked_accept, mocked_settimeout, mocked_listen, mocked_bind, client_address):

    mocked_accept.return_value = (client_address, socket.socket())

    srv = EchoServer()

    srv.connect()

    mocked_accept.assert_called_once_with()


@mock.patch('socket.socket.bind')
@mock.patch('socket.socket.listen')
@mock.patch('socket.socket.settimeout')
@mock.patch('socket.socket.accept')
def test_connect_timeout(mocked_accept, mocked_settimeout, mocked_listen, mocked_bind, client_address):

    mocked_accept.side_effect = OSError()

    srv = EchoServer()

    srv.connect()

    mocked_accept.assert_called_once_with()


@mock.patch('socket.socket.bind')
@mock.patch('socket.socket.listen')
@mock.patch('socket.socket.settimeout')
def test_perform_mainloop(mocked_settimeout, mocked_listen, mocked_bind, server_timeout):

    srv = EchoServer()

    srv.perform_mainloop()


@mock.patch('socket.socket.bind')
@mock.patch('socket.socket.listen')
@mock.patch('socket.socket.settimeout')
@mock.patch('socket.socket.accept')
@mock.patch('server.EchoServer.perform_mainloop')
def test_mainloop(mocked_perform_mainloop, mocked_accept, mocked_settimeout, mocked_listen, mocked_bind, client_address):

    mocked_perform_mainloop.side_effect = KeyboardInterrupt()

    mocked_accept.return_value = (client_address, socket.socket())

    srv = EchoServer()

    srv.mainloop()

    mocked_accept.assert_called_once_with()



@mock.patch('socket.socket.bind')
@mock.patch('socket.socket.listen')
@mock.patch('socket.socket.settimeout')
def test_read(mocked_settimeout, mocked_listen, mocked_bind, mocked_connect, mocked_send, mocked_recv):


    clt = EchoClient()
    
    srv = EchoServer()

    srv.connect()

    clt.write('body')

    srv.read(clt._sock, ['localhost',8000])

    request = list(srv._requests.values())[0]

    assert 'body' in request.body

@mock.patch('socket.socket.bind')
@mock.patch('socket.socket.listen')
@mock.patch('socket.socket.settimeout')
def test_write(mocked_settimeout, mocked_listen, mocked_bind, mocked_connect, mocked_send, mocked_recvsend, mocked_request, capsys):


    clt = EchoClient()
    
    srv = EchoServer()

    srv.connect()

    request = mocked_request

    srv.write(clt._sock, request, ['localhost',8000])

    clt.read()

    out, err = capsys.readouterr()

    assert 'server received message from client' in out
    
  



    
