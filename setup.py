from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='e_utils',
    url='https://github.com/ebravofm/e_utils',
    author='Emilio Bravo',
    author_email='ebravofm@gmail.com',
    scripts=['e_utils'],
    # Needed to actually package something
    packages=['e_utils'],
    # Needed for dependencies
    install_requires=['numpy'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='Random Utilities',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)