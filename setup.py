from setuptools import setup

setup(
    name='theatre_tcp_ip',
    version='0.1',
    packages=['theatre_tcp_ip'],
    package_dir={'': '.'},
    url='https://github.com/twsswt/theatre_tcp_ip',
    license='',
    author='Tim Storer',
    author_email='timothy.storer@glasgow.ac.uk',
    description='An example of using Theatre_Ag for modelling TCP clients and servers.',
    setup_requires={},
    test_suite='nose.collector',
    tests_require=['mock', 'nose']
)
