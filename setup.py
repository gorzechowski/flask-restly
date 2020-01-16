#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='flask-restly',
    version='1.0.1',
    description='Build a REST API with Flask',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gorzechowski/flask-restly',
    author='Gracjan Orzechowski',
    author_email='orzechowski.gracjan@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    keywords='flask api rest',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[
        'flask>=1.0',
        'wrapt>=1.0',
    ],
)
