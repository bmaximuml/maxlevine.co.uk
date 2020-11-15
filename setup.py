from setuptools import setup, find_packages

setup(
    name='maxlevine.co.uk',
    version='1.1',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'datetime',
        'Flask',
        'Flask-SQLAlchemy',
        'mysql-connector-python',
        'requests',
        'WTForms',
        'email-validator',
        'Flask-xCaptcha',
    ],
    author='Max Levine',
    author_email='max@maxlevine.co.uk',
    url='https://github.com/benjilev08/maxlevine.co.uk'
)
