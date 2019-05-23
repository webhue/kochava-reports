from __future__ import absolute_import
from distutils.util import convert_path
from setuptools import find_packages
from setuptools import setup
from io import open

ns = {}
version_path = convert_path('kochavareports/version.py')
with open(version_path, encoding='utf-8') as version_file:
    exec(version_file.read(), ns)

setup_args = dict(
    name='kochava-reports',
    description='Python library to generate reports in the Kochava platform.',
    url='https://github.com/webhue/kochava-reports',
    version=ns['__version__'],
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    author='Marius Bodea',
    author_email='mbodea@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
    ],
)

if __name__ == '__main__':
    setup(**setup_args)
