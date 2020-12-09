import os
import re
import json
import collections
import logging
from urllib import parse

import distutils.util
from flask import Flask, request, jsonify
from fedora_messaging import message, api


DEFAULT_LOGGER_NAME =__name__
DEFAULT_TOPIC_TEMPLATE = '{web_url.hostname}.{web_url.path}.{object_kind}'
DEFAULT_IS_PRODUCTION = 'False'

DQ = collections.deque()

app = Flask(__name__)
gunicorn_logger = logging.getLogger(os.environ.get('LOGGER_NAME', __name__))
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)


def get_bool_env(name, default='False'):
  return bool(distutils.util.strtobool(
    os.environ.get(name, 'False'))
  )


def get_str_env(name, default=''):
  return os.environ.get(name, default)


def is_authenticated(token):
  if not 'GITLAB_TOKEN' in os.environ:
    return False

  env_token = os.environ['GITLAB_TOKEN']

  return env_token == token


def get_topic_vars(data):
  object_kind = data['object_kind']
  if 'project' in data:
    web_url = data['project']['web_url']
  else:
    web_url = data['repository']['homepage']
  web_url = parse.urlsplit(web_url)

  return object_kind, web_url


def get_parsed_topic(**kwargs):
  return re.sub('[./]+', '.', get_str_env('TOPIC_TEMPLATE', DEFAULT_TOPIC_TEMPLATE).format(
    env=os.environ, **kwargs))


@app.route('/health', methods=['GET'])
def health():
  return jsonify({
    'status': 'OK'
  })


@app.route('/info', methods=['GET'])
def info():
  return jsonify({
    'is_production': get_bool_env('IS_PRODUCTION', DEFAULT_IS_PRODUCTION),
    'topic_template': get_str_env('TOPIC_TEMPLATE', DEFAULT_TOPIC_TEMPLATE),
    'log': {
      'name': get_str_env('LOGGER_NAME', DEFAULT_LOGGER_NAME),
      'level': app.logger.getEffectiveLevel()
    }
  })


@app.route('/', methods=['POST'])
def root():
  if not is_authenticated(request.headers.get('X-Gitlab-Token')):
    return ('', 401)
  data = json.loads(request.data)
  object_kind, web_url = get_topic_vars(data)
  topic = get_parsed_topic(
    object_kind=object_kind,
    web_url=web_url)
  headers = {
    'event_name': request.headers.get('x-gitlab-event')
  }

  enqueue(data, topic, headers)

  return ('', 204)


def enqueue(data, topic, headers):
  DQ.append((data, topic, headers))

  while DQ:
    _data, _topic, _headers = DQ.popleft()
    try:
      if get_bool_env('IS_PRODUCTION', DEFAULT_IS_PRODUCTION):
        msg = message.Message(
          topic=_topic,
          headers=_headers,
          body=_data
        )
        api.publish(msg)
        app.logger.info(f'Sending payload to {_topic}')
      else:
        app.logger.info(f'\n---\n{_topic}\n{_headers}\n{_data}\n---')
    except Exception:
      app.logger.exception('Error during sending message, will be retried')
      DQ.appendleft((_data, _topic, _headers))


if __name__ == '__main__':
  app.run(debug=True, port=5000)
