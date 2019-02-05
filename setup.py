from setuptools import setup, find_packages
#import dxm.dxm

setup(
    name='dxm',
    #version=dxm.dxm.__version__,
    packages=find_packages(),
    install_requires=[
        'click','requests','pytz', "urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil", "masking_apis", "colorama", "tqdm"
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


