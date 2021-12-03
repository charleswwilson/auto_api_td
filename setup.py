from setuptools import setup
from setuptools import find_namespace_packages

#  Readme file
with open(file="README.md", mode="r") as readme_handle:
    long_description = readme_handle.read()

setup(
    name='tdamerapi',
    author='Charles Wilson',
    author_email='charleswwilson@outlook.com',
    version='0.0.1',
    description='access td ameritrade api',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['tdamerapi'],
    package_dir={'': 'TD_API_PROJECT'},
    url='',
)
