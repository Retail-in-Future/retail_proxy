
from setuptools import find_packages, setup

setup(
    name='retail-proxy',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    url='https://tjdai@bitbucket.org/retail_in_future/retail_proxy.git',
    license='',
    author='tjdai',
    author_email='tjdai@thoughtworks.com',
    description='nodemcu to amazon IoT',
    install_requires=[
        'pyyaml',
        'AWSIoTPythonSDK', 'nose'
    ],
)
