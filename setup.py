from setuptools import setup

setup(
    name='theatre_tcp_ip',
    version='0.1',
    packages=['theatre_tcp_ip'],
    package_dir={'': '.'},
    url='https://github.com/twsswt/theatre_tcp_ip',
    dependency_links=[
        'https://github.com/twsswt/theatre_ag/tarball/master#egg=theatre_ag-0.1'],
    license='',
    author='Tim Storer',
    author_email='timothy.storer@glasgow.ac.uk',
    description='An example of using Theatre_Ag for modelling TCP clients and servers.',
    setup_requires={'theatre_ag'},
    test_suite='nose.collector',
    tests_require=['mock', 'nose']
)
