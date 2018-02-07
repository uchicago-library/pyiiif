from setuptools import setup, find_packages


def readme():
    with open("README.md", 'r') as f:
        return f.read()


setup(
    name="pyiiif",
    description="Library code for working with the IIIF specifications",
    version="0.0.1",
    long_description=readme(),
    author="Brian Balsamo",
    author_email="brian@brianbalsamo.com",
    packages=find_packages(
        exclude=[
        ]
    ),
    include_package_data=True,
    url='https://github.com/bnbalsamo/pyiiif',
    install_requires=[
        'requests'
    ],
    tests_require=[
        'pytest'
    ],
    test_suite='tests'
)
