import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

with open(os.path.join(here, 'CHANGES.rst')) as f:
    CHANGES = f.read()


requires = ["six", "Django", "pymemcache"]
test_requires = ['nose']


setup(name='django-pymemcache-pool',
      version='0.5',
      description='A Memcached Pool for Django',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: OSI Approved :: Apache Software License",
        ],
      author='Duan Hongyi',
      author_email='sduanhongyi@doopai.com',
      url='https://github.com/duanhongyi/django-pymemcache-pool',
      keywords='django pymemcache pool',
      packages=find_packages(),
      zip_safe=False,
      install_requires=requires,
      dependency_links=[
        'https://github.com/duanhongyi/pymemcache/archive/master.zip#egg=pymemcache-1.3.0',
      ],
      tests_require=test_requires,
      test_suite="memcachepool.tests")
