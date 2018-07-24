# Dxm - DxToolkit for Masking

## What is it

Dxtoolkit for masking is a command line script to manipulate Delphix Masking Engine and it is delivered by Delphix professional services team.
Dxmc script is a single command with parameters and arguments delivered as executable file with libraries. Dxm is written in Python, but no knowledge of Python is required unless you want to extend it.  In fact, no programming experience whatsoever is required to use the Dxtoolkit for masking.

## What's new

Please check a [change log](https://github.com/delphix/dxm/blob/master/CHANGELOG.md) for list of changes.

## How to get started
### Compiled version

Download a compiled version of Dxm for required platform from a [releases  page](https://github.com/delphix/dxtoolkit/releases).
Dxm keep a configuration using SQLLite database and it's creating a configuration file when a first engine is added.
When dxm is started it will execute an action against Masking engine specified in option or against engine configured as default one.

Configure a masking engine using the following steps:

* add engine
```
dxm engine engine add --engine testeng --ip testeng.foo.com --username delphix_admin --default Y
Password:
Repeat for confirmation:
Engine added to configuration
```

* list all engines from configuration
```
 dxm engine list

 Engine name                     IP                              username                        protocol  port   default
 ==============================  ==============================  ==============================  ========  =====  =======
 testeng                         testeng.foo.com                 delphix_admin                   http      8282   Y       

```

Check a [documentation](https://github.com/delphix/dxtoolkit/wiki) for more details

### Known issues

No paging support

### Source version

Python 2.7.X

**Required packages**
Delphix Masking API libraries are required.
Check setup.py for list of packages

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
Copyright (c) 2014, 2016 by Delphix. All rights reserved.
