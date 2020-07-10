# Dxm - DxToolkit for Masking

## What is it

Dxtoolkit for masking is a command line script to manipulate Delphix Masking Engine and it is delivered by Delphix professional services team.
Dxmc script is a single command with parameters and arguments delivered as executable file with libraries. Dxm is written in Python, but no knowledge of Python is required unless you want to extend it.  In fact, no programming experience whatsoever is required to use the Dxtoolkit for masking.

Supperted Delphix Engine version: >= 5.3.X and 6.0.X

## What's new

Please check a [change log](https://github.com/delphix/dxm-toolkit/blob/master/CHANGELOG.md) for list of changes.

## How to get started
### Compiled version

Download a compiled version of Dxm for required platform from a [releases  page](https://github.com/delphix/dxm-toolkit/releases).
Dxm keep a configuration using SQLLite database and it's creating a configuration file when a first engine is added.
When Dxm is started it will execute an action against Masking engine specified in option or against engine configured as default one.

Compiled version is distributed as single command on Linux and OSX and a zipped folder on Windows platform.
Single command distribution on Windows is limited by PyInstaller issue which require to disable some security features on Windows 10.
To start a DXM on the Linux or OSX, please run dxmc command from place where it was downloaded. On Windows please run dxmc.exe from unzipped folder.

Configure a masking engine using the following steps:

* add engine
```
dxmc engine engine add --engine testeng --ip testeng.foo.com --username delphix_admin --default Y
Password:
Repeat for confirmation:
Engine added to configuration
```

* list all engines from configuration
```
dxmc engine list

Engine name                     IP                              username                        protocol  port   default
==============================  ==============================  ==============================  ========  =====  =======
testeng                         testeng.foo.com                 delphix_admin                   http      8282   Y       

```

* check if configuration is OK and list all applications from Masking Engine
```
dxmc application list

Engine name                     Application name
==============================  ==============================
testeng                         test app 2
```

Check a [documentation](https://github.com/delphix/dxm-toolkit/wiki) for more details

### Known issues

- No pagination support
- No password encryption in configuration database - it will be addressed in next release

### Source version

Python 3.7.X

**Required packages**
- Check setup.py for list standard Python packages
- Delphix Masking Engine Swagger SDK is required

To generate Masking SDK version 6.0.X run the following commands where _myengine_ is a name or IP of Delphix Masking Engine

```
mkdir masking_api_60

docker run --rm -v ${PWD}:/local swaggerapi/swagger-codegen-cli generate -DapiDocs=false -DapiTests=false -DmodelTests=false -DmodelDocs=false -i http://myengine/masking/api/swagger-basepath.json -l python -o /local/masking_api_60 -DpackageName=masking_api_60

cd masking_api_60

python setup.py install
```

To generate Masking SDK version 5.3.X run the following commands where _myengine_ is a name or IP of Delphix Masking Engine:

```
mkdir masking_api_53

docker run --rm -v ${PWD}:/local swaggerapi/swagger-codegen-cli generate -DapiDocs=false -DapiTests=false -DmodelTests=false -DmodelDocs=false -i http://myengine/masking/api/swagger-basepath.json -l python -o /local/masking_api_53 -DpackageName=masking_api_53

cd masking_api_53

python setup.py install
```


## Legalness
```
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
```
Copyright (c) 2018 by Delphix. All rights reserved.
