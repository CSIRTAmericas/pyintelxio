from setuptools import setup, find_packages

setup(
    name='pyintelxio',
    version='1.0.0',
    author='Fermin',
    description='This lib add support to use the Identity API from Intelx.io',
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=['requests'],
    license='MIT',
    keywords='python, package, distribution'
)
