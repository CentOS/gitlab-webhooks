import os
import json
from unittest import mock

from fedora_messaging import api

from gitlab_webhook import app


def test_health():
  with app.test_client() as client:
    rv = client.get('/health')

  expected = {'status': 'OK'}
  current = json.loads(rv.data)

  assert expected == current


def test_info_default():
  with app.test_client() as client:
    rv = client.get('/info')

  expected = {
    'is_production': False,
    'log': {
      'level': 30,
      'name': 'gitlab_webhook'
    },
    'topic_template': '{web_url.hostname}.{web_url.path}.{object_kind}'
  }
  current = json.loads(rv.data)

  assert expected == current


def test_info_custom(monkeypatch):
  values = {
    'IS_PRODUCTION': 'True',
    'LOGGER_NAME': 'gunicorn.error',
    'TOPIC_TEMPLATE': 'org.centos.prod.gitlab.{web_url.path}.{object_kind}'
  }
  with app.test_client() as client, mock.patch.dict(os.environ, values):
    rv = client.get('/info')

  expected = {
    'is_production': True,
    'log': {
      'level': 30,
      'name': 'gunicorn.error'
    },
    'topic_template': 'org.centos.prod.gitlab.{web_url.path}.{object_kind}'
  }
  current = json.loads(rv.data)

  assert expected == current


def test_root_no_token(fixtures_dir):
  with app.test_client() as client:
    rv = client.post('/')
  
  assert 401 == rv.status_code


def test_root_no_header_token(fixtures_dir):
  values = {
    'GITLAB_TOKEN': 'foo'
  }
  with app.test_client() as client, mock.patch.dict(os.environ, values):
    rv = client.post('/', headers={})
  
  assert 401 == rv.status_code


def test_root_invalid_token(fixtures_dir):
  values = {
    'GITLAB_TOKEN': 'foo'
  }
  with app.test_client() as client, mock.patch.dict(os.environ, values):
    rv = client.post('/', headers={'X-Gitlab-Token': 'bar'})
  
  assert 401 == rv.status_code


def test_root_no_prod(fixtures_dir):
  with open(f'{fixtures_dir}/push.json') as f:
    raw = f.read()

  values = {
    'GITLAB_TOKEN': 'foo'
  }
  
  with app.test_client() as client, mock.patch.dict(os.environ, values):
    rv = client.post('/', data=raw, headers={'X-Gitlab-Token': 'foo'})
  
  assert 204 == rv.status_code
  assert b'' == rv.data


def test_root_prod(fixtures_dir):
  with open(f'{fixtures_dir}/push.json') as f:
    raw = f.read()

  values = {
    'GITLAB_TOKEN': 'foo',
    'IS_PRODUCTION': 'True'
  }
  
  with app.test_client() as client, mock.patch.dict(os.environ, values), mock.patch.object(api, 'publish'):
    rv = client.post('/', data=raw, headers={'X-Gitlab-Token': 'foo'})
  
  assert 204 == rv.status_code
  assert b'' == rv.data
