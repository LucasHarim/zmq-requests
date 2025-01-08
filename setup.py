
from distutils.core import setup

with open('README.md', 'r') as readme:
  long_desc = readme.read()

setup(name='zmq_requests',
      version='0.1.0',
      description='Client requests that mimic bindings',
      long_description = long_desc,
      long_description_content_type = 'text/markdown',
      author='Lucas Harim G. C.',
      author_email='harimlgc@usp.br',
      keywords = 'zmq-requests',
      packages = ['zmq_requests'],
      install_requires = [
        'pyzmq',
        'orjson']
     )