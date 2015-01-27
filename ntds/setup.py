from setuptools import setup

setup(
    name='rapidsms-ntds',
    version='0.1',
    license="BSD",

    install_requires = ["rapidsms", 'rapidsms-generic'],

    dependency_links = [
        "http://github.com/unicefuganda/rapidsms-generic/tarball/master#egg=rapidsms-generic"
    ],

    description='Mass Drug administration statistics for neglected tropical diseases',
    long_description=open('README.rst').read(),
    author='Moses Mugisha',
    author_email='mugisha@sparkpl.ug',

    url='http://github.com:/unicefuganda/rapidsms-ntds',
    download_url='http://github.com:/unicefuganda/rapidsms-ntds/downloads',

    include_package_data=True,

    packages=['ntds'],
    package_data={'ntds':['templates/*/*.html','templates/*/*/*.html','static/*/*']},
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
