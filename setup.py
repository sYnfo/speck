from setuptools import setup

setup(name='speck',
      version='0.1',
      description='Tool for semantic modification of spec files',
      author='Matej Stuchlik',
      scripts=['bin/speck'],
      packages=['speck'],
      test_suite="tests",
      )
