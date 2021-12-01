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
        'Flask==1.1.2',
        'Flask-SQLAlchemy',
        'mysql-connector-python',
        'requests',
        'WTForms==2.3.3',
        'email-validator',
        'Flask-xCaptcha',
    ],
    author='Max Levine',
    author_email='max@maxlevine.co.uk',
    url='https://github.com/bmaximuml/maxlevine.co.uk'
)
