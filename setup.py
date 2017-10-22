from setuptools import find_packages, setup

setup(
    name='checkdnssec',
    version='0.1',
    packages=find_packages(),
    install_requires=[
      'dnspython',
      'pycrypto',
    ],
    entry_points={
        'console_scripts': [
            'checkdnssec = checkdnssec:main',
        ],
    },
)
