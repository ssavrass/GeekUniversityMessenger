import pytest

import socket

from client import EchoClient
from jsonformat.jimprotocolclient import JSONRequest, JSONResponse


@pytest.fixture
def connect_message():

    return 'socket bind successfully'


@pytest.fixture
def JSON_bytes():
    JSONbytes = JSONRequest("action","body").to_bytes()
    return JSONbytes
    

@pytest.fixture
def JSON_read():
    
    return "'action': 'action'"

@pytest.fixture
def mocked_connect(connect_message, monkeypatch):

    def mock_connect(self, *args, **kwargs):

        print(connect_message)

    monkeypatch.setattr(socket.socket, 'connect', mock_connect)


@pytest.fixture
def mocked_recv(JSON_bytes, monkeypatch):

    def mock_recv(self, *args, **kwargs):

        return JSON_bytes

    monkeypatch.setattr(socket.socket, 'recv', mock_recv)

@pytest.fixture
def mocked_send(JSON_bytes, monkeypatch):

    def mock_send(self, *args, **kwargs):

        return JSON_bytes

    monkeypatch.setattr(socket.socket, 'send', mock_send)

@pytest.fixture
def mocked_perform(monkeypatch):

    def mock_perform(self, *args, **kwargs):

        raise KeyboardInterrupt()

    monkeypatch.setattr(EchoClient, 'perform_run', mock_perform)


def test_connect(mocked_connect, connect_message, capsys):

    EchoClient()

    out, err = capsys.readouterr()

    assert connect_message in out


def test_read(mocked_connect, mocked_recv, JSON_read, capsys):

    clt = EchoClient()

    clt.read()

    out, err = capsys.readouterr()

    assert JSON_read in out

def test_write(mocked_connect, mocked_send):

    clt = EchoClient()

    clt.write('hey')
    

def test_perform(mocked_connect):

    clt = EchoClient()

    clt.perform_run()    


def test_run(mocked_connect, mocked_recv, mocked_perform):

    clt = EchoClient()
    
    try:
        clt.run()
    except IOError:
        pass    