from setuptools import setup

requires = [
    'bricks',
    'common_components',
    'werkzeug'
]

links = [
    'git+https://github.com/Zer0-/bricks.git#egg=bricks',
    'git+https://github.com/Zer0-/common_components.git#egg=common_components',
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
