import setuptools


def load_reqs(path):
  reqs = []
  with open(path) as f:
    for line in f.readlines():
      _line = line.strip()
      if not _line.startswith('#'):
        reqs.append(_line)
  return reqs


setuptools.setup(
    name='gitlab_webhook',
    version='0.0.1',
    py_modules=['gitlab_webhook'],
    install_requires=load_reqs('requirements.txt'),
    python_requires='>=3.7',
)
