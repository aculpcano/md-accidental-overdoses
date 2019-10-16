from setuptools import find_packages, setup

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='overdoses',
    version=0.1,
    author='Alexander Wesley Culp Cano',
    author_email='awccdev@gmail.com',
    description='Mapping the MD drug overdoses between 2013 and 2018',
    install_requires=['folium>=0.10.0', 'geopandas>=0.6.0', 'pandas>=0.25.1'],
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.7'
)
