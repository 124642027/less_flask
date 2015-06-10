from setuptools import setup


setup(
    name='hello_app',
    version='1.0',
    long_description=__doc__,
    packages=['hello_app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)