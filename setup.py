from setuptools import setup, find_packages
from nginxtest import __version__
import sys

install_requires = ["Mako", "requests"]
description = ''

for file_ in ('README',):
    with open('%s.rst' % file_) as f:
        description += f.read() + '\n\n'


classifiers = ["Programming Language :: Python",
               "Development Status :: 1 - Planning"]


setup(name='NginxTest',
      version=__version__,
      url='https://github.com/tarekziade/NginxTest',
      packages=find_packages(),
      long_description=description,
      description=("Helpers to drive a local Nginx server"),
      author="Tarek Ziade",
      author_email="tarek@ziade.org",
      include_package_data=True,
      zip_safe=False,
      classifiers=classifiers,
      install_requires=install_requires,
      )
