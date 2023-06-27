from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    
DEPENDENCIES = open('requirements.txt', 'r').read().split('\n')
setup(
    name='pyintelx',
    version='0.0.9',
    description='This lib add support to use the Identity API from Intelx.io',
    license='MIT',
    keywords=['python, package, distribution'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Fermin Baudino, Einar Lanfranco, Federico Carrilao',
    url='https://github.com/csirtamericas/pyintelxio',
    packages=['pyintelx'],
    install_requires=DEPENDENCIES,
    scripts=['pyintelx/cli/pyintelx'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6'
)
