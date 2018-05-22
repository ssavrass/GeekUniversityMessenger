import json

import pytest

from datetime import datetime

from jsonformat.jimprotocolclient import JSONResponse

import settings


@pytest.fixture
def code():

    return 200


@pytest.fixture
def action():

    return 'sendto'


@pytest.fixture
def time():

    dt = datetime.now()

    return dt.strftime('%d/%m/%y')


@pytest.fixture
def from_client():

    return '@fromclientname'


@pytest.fixture
def to_client():

    return '@toclientname'


@pytest.fixture
def body():

    return 'Message body from one client to another'


@pytest.fixture
def headers(time, from_client, to_client):

    return {'time':time, 'to':to_client, 'from':from_client}


@pytest.fixture
def raw_response(code, action, headers, body):

    data = {'code':code, 'action':action, 'headers':headers, 'body':body}

    str_data = json.dumps(data)

    return str_data.encode(settings.ENCODING)


@pytest.fixture
def response(raw_response):

    return JSONResponse(raw_response)


def test_code(response, code):

    assert response.code == code


def test_action(response, action):

    assert response.action == action


def test_headers(response, headers):

    response_headers = dict(response.headers)

    assert len(response_headers) == len(headers)


def test_time(response, time):

    response_headers = dict(response.headers)

    response_time = response_headers.get('time')

    assert response_time == time


def test_from(response, from_client):

    response_headers = dict(response.headers)

    response_from = response_headers.get('from')

    assert response_from == from_client


def test_to(response, to_client):

    response_headers = dict(response.headers)

    response_to = response_headers.get('to')

    assert response_to == to_client


def test_body(response, body):

    assert response.body == body
    
