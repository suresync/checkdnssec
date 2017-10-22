from setuptools import find_packages, setup
from subprocess import check_output


def version_from_git():
    """Acquire package version form current git tag."""
    return check_output(['git', 'describe', '--tags', '--abbrev=0'],
                        universal_newlines=True)


setup(
    name='checkdnssec',
    version=version_from_git(),
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
