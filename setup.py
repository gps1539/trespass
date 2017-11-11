from setuptools import setup
setup(
  name = 'trespass',
  packages = ['trespass'], # this must be the same as the name above
  install_requires=[
	'numpy',
	'pygpgme',
	'pyperclip',
	'argparse',
  ],
  version = '0.6.5.8',
  description = 'A secure password keeper', 
  author = 'Graham Smith',
  author_email = 'gps1539@gmail.com',
  scripts = ['trespass/trespass'],
  license='GPL3',
  url = 'https://github.com/gps1539/trespass', # use the URL to the github repo
  download_url = 'https://github.com/gps1539/trespass/archive/0.1.tar.gz',
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  classifiers = [],
)
