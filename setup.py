from setuptools import setup

setup(name='speck',
      version='0.1',
      description='Tool for semantic modification of spec files',
      author='Matej Stuchlik',
      include_package_data=True,
      py_modules=['speck'],
      test_suite="tests",
      install_requires=[
          'Click',
          'Tabulate',
          ],
      entry_points='''
          [console_scripts]
          speck=speck:cli
          ''',
      )
