try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


NAME = 'manipulator'
VERSION = '0.1'


setup(
    name=NAME,
    license='MIT',
    version=VERSION,
    description='A library for vote manipulation on Reddit',
    install_requires=[
        'colorama',
        'mechanize',
        'pysocks'
    ],
    packages=[NAME]
)
