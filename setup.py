from setuptools import setup, find_packages

def install_driver():
        import pyderman
        pyderman.install(browser=pyderman.chrome, file_directory='lib/driver/', filename='chromedriver') 

def _setup():
        install_requires = [
                'lxml',
                'pyderman',
                'selenium==4.0.0a6.post2',
                'beautifulsoup4',
                'requests',
                'pytest',
                'inquirer',
                ]

        setup(name='PCC Bots',
                version='1.0.0',
                description='Bots for surviving at PCC',
                author='Travis/Jaeyoung Cho',
                author_email='jcho30@go.pasadena.edu',
                url='https://github.com/chotravis87/pcc-bots',
                packages=find_packages(),
                install_requires=install_requires,
                setup_requires=install_requires,
                )

if __name__ == "__main__":
        _setup()
        install_driver()
    