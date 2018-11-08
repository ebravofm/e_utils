from setuptools import setup

setup(
    name='e_utils',
    url='https://github.com/ebravofm/e_utils',
    author='Emilio Bravo',
    author_email='ebravofm@gmail.com',
    # Needed to  package something
    packages=['e_utils'],
    install_requires=['numpy', 'pandas', 'leven', 'sklearn', 'unidecode'],
    version='0.1',
    license='MIT',
    description='Random Utilities',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)