from setuptools import setup, find_packages

setup(
    name='pyintelxio',
    version='1.0.0',
    author='Fermin',
    description='Un servicio para usar las api de IntelligenceX',
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=['requests'],
    license='MIT',
    keywords='python, package, distribution'
)
