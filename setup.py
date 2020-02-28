import re

from setuptools import find_packages, setup

with open('isimip_validator/__init__.py') as f:
    metadata = dict(re.findall(r'__(.*)__ = [\']([^\']*)[\']', f.read()))

setup(
    name=metadata['title'],
    version=metadata['version'],
    author=metadata['author'],
    author_email=metadata['email'],
    maintainer=metadata['author'],
    maintainer_email=metadata['email'],
    license=metadata['license'],
    url='https://github.com/ISI-MIP/isimip-validator',
    description=u'',
    long_description=open('README.md').read(),
    install_requires=[
        'jsonschema~=3.2',
        'requests~=2.23',
        'python-dotenv~=0.10'
    ],
    classifiers=[
        # https://pypi.org/classifiers/
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'isimip-validator=isimip_validator.main:main',
        ]
    }
)
