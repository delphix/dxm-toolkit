from setuptools import setup, find_packages
#import dxm.dxm

setup(
    name='dxm',
    #version=dxm.dxm.__version__,
    packages=find_packages(),
    install_requires=[
        'click','requests','pytz', "urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil", "colorama", "tqdm", "packaging", "keyring", "cryptography"
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
    ]
)

# add swagger libs
# docker run --rm -v ${PWD}:/local swaggerapi/swagger-codegen-cli generate -DapiDocs=false -DapiTests=false -DmodelTests=false -DmodelDocs=false -i http://myengine/masking/api/swagger-basepath.json -l python -o /local/masking_api_60 -DpackageName=masking_api_60
# cd masking_api_60
# python setup.py install
