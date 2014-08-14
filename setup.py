from setuptools import setup

requires = [
    'bricks',
    'common_components',
]

links = [
    'git+ssh://phil@home.volguine.com/usr/share/repositories/common_components.git#egg=common_components',
    'git+https://github.com/Zer0-/bricks.git#egg=bricks',
]

setup(
    name='listrr',
    version='0.0',
    description='Webapp for simple nested todo list',
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Philipp Volguine',
    author_email='phil.volguine@gmail.com',
    packages=['listrr'],
    include_package_data=True,
    install_requires=requires,
    dependency_links=links,
)
