from setuptools import setup
import app

setup(
    name='Example Flask API',
    version=app.__version__,
    packages=['app'],
)
