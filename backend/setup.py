from setuptools import setup, find_packages

with open('README.md') as fp:
    longdesc = fp.read()

setup(
    name='ausweis',
    version='0.9.0',
    author='OWBA',
    description='Django app for digital membership cards',
    long_description=longdesc,
    long_description_content_type="text/markdown",
    url='https://github.com/owba/ausweis',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    packages=find_packages(),
    scripts=['manage.py'],
    install_requires=[],
)
