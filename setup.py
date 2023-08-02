from setuptools import setup, find_packages
import setuptools.command.build_py


class BuildPyCommand(setuptools.command.build_py.build_py):
  """Custom build command."""

  def run(self):
    # add here a build
    setuptools.command.build_py.build_py.run(self)

setup(
    cmdclass={
        'build_py': BuildPyCommand
    },
    name='dxm',
    #version=dxm.dxm.__version__,
    packages=find_packages(),
    install_requires=[
        'pyparsing==3.0.7',
        'click == 7.1.2',
        'requests',
        'pytz', 
        "urllib3 <= 2.0.0a", 
        "six >= 1.10", 
        "certifi", 
        "python-dateutil == 2.8.1", 
        "colorama == 0.4.3", 
        "tqdm == 4.47.0", 
        "packaging == 20.4", 
        "keyring == 21.2.1", 
        "cryptography == 41.0.3"
    ],
    entry_points='''
        [console_scripts]
        dxmc=dxm.dxm:dxm
    ''',
    author = "Marcin Przepiorowski",
    license = "Apache 2",
    description = ("DxToolkit for Masking - command line tool to manage Delphix Masking environment"),
    classifiers = [
        "Development Status :: 2 - Beta"
    ],
    dependency_links=[
        'git+https://github.com/pioro/masking_api_53.git#egg=masking_api_53-1.0.0',
        'git+https://github.com/pioro/masking_api_60.git#egg=masking_api_60-6.0.4.2'
    ]
)


# add swagger libs
# docker run --rm -v ${PWD}:/local swaggerapi/swagger-codegen-cli generate -DapiDocs=false -DapiTests=false -DmodelTests=false -DmodelDocs=false -i http://myengine/masking/api/swagger-basepath.json -l python -o /local/masking_api_60 -DpackageName=masking_api_60
# cd masking_api_60
# python setup.py install
