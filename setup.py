
from distutils.core import setup

setup(name='zmq_requests',
      version='1.0',
      description='Client requests that mimic bindings',
      author='Lucas Harim G. C.',
      author_email='harimlgc@usp.br',
      packages = ['zmq_requests'],
    install_requires = [
        'pyzmq',
        'orjson']
     )