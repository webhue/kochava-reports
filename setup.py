from distutils.util import convert_path
from setuptools import find_packages
from setuptools import setup

ns = {}
version_path = convert_path('kochavareports/version.py')
with open(version_path) as version_file:
    exec(version_file.read(), ns)

setup_args = dict(
    name='kochava-reports',
    description='Python library to generate reports in the Kochava platform.',
    url='https://github.com/mbodea/kochava-reports',
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
        'Programming Language :: Python',
    ],
)

if __name__ == '__main__':
    setup(**setup_args)
