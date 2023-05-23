from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='gadapt',
    version='0.1',
    license='MIT',
    author="Zoran Jankovic",
    author_email='bpzoran@yahoo.com',
    packages=find_packages(),
    url='https://github.com/bpzoran/gadapt',
    keywords='example project',
    description="GAdapt: A Python Library for Self-Adaptive Genetic Algorithm.",
    long_description=long_description,
    long_description_content_type="text/markdown",

)
