from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='Easy Apriori',
    url='https://github.com/ronaldolagepessoa/easyapriori',
    author='Ronaldo Lage',
    author_email='ronaldo.lage.pessoa@gmail.com',
    # Needed to actually package something
    packages=['apriori'],
    # Needed for dependencies
    install_requires=['pandas', 'apyori'],
    # *strongly* suggested for sharing
    version='1.0.0',
    # The license can be anything you like
    license='FREE',
    description='Solução simples para utilização do algoritmo Apriori no python',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)