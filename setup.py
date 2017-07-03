
from setuptools import find_packages, setup

setup(
    name='retail-proxy',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    url='',
    license='',
    author='tjdai',
    author_email='',
    description='',
    install_requires=[
        'pyyaml',
        'AWSIoTPythonSDK', 'nose', 'yaml'
    ],
)
