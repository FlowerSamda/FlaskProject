from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),  # package directories and python files
    include_package_data=True,  # static, templates directories
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)