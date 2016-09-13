"""Setup for twitter client for services"""
import codecs

from setuptools import setup, find_packages

with codecs.open('README.md', encoding='utf-8') as inf:
    long_description = inf.read()

reqs = []
with open('requirements.txt') as inf:
    for line in inf:
        line = line.strip()
        reqs.append(line)

setup(
    name='aquatic-twitter',
    version='0.1.2',
    description='Twitter client for various projects',
    long_description=long_description,
    author='Brett Smythe',
    author_email='smythebrett@gmail.com',
    maintainer='Brett Smythe',
    maintainer_email='smythebrett@gmail.com',
    packages=find_packages(),
    install_requires=reqs
)
