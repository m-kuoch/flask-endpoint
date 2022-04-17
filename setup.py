from setuptools import setup, find_packages

requires = [
    'flask',
]

setup(
    name='flask_endpoint',
    version='0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)