## Version 0.9.5
Tested with engines 6.0.12 and above

### Added:
- timeout is now configurable in the engine menu

### Changed:
 - Various bugs

## Version 0.9.1

Support for many engine versions added. Since version 0.9.1 dxm-toolkit should support all versions
of 6.0.X engines plus 5.3.9


### Added:
- dxmc engine upload - upload file command -
- dxmc jdbc - a group of command to add, delete and list extended jdbc connectors

### Changed:
 - fix for engine user support - now same engine can be added to configuration with different users
 - move from Swagger based model to custom model

## Version 0.8.2

### Changed:
 - Fix for job report


## Version 0.8

If you are upgrading from previous version, you need to update all engines in your configuration
and set again engine password.

### Added:
 - Added Job Report [Job history report](https://github.com/delphix/dxm-toolkit/issues/37)
 - Support for encrypted passwords in Engine config database 
 - Add support for Proxy on Windows / OSX
 - [fix for #33](https://github.com/delphix/dxm-toolkit/issues/33) - DateFormat not extracted with column list


### Changed:
 - Support for 5.3.X and 6.0.X in single build
 - [fix for #32](https://github.com/delphix/dxm-toolkit/issues/32) - Unable to call pre and post script with script Path

## Version 0.7

### Changed:
 - initial support for 6.0

## Version 0.6

### Added:
 - Ruleset refresh operation added
 - Possibility to automatically add all or filtered list of tables from connector to ruleset
 - The bulk flag added to addmeta operaion while loading table from csv file or directly from connector list of tables 
 - Supoprt for domain creation, list, update and delete
 - support for JDBC connection string (advanced option) added to connector 

### Changed:
 - None

## Version 0.53

### Changed:
 - fix for export/import ruleset
 - fix for export inventory in GUI format

## Version 0.52

### Added:
 - Support to import and export inventory using a GUI format

### Changed:
 - [fix for #9](https://github.com/delphix/dxm-toolkit/issues/9) - ID method change supported in batch option
 - [fix for #18](https://github.com/delphix/dxm-toolkit/issues/18) - adding on the fly jobs
 - bug fixes

## Version 0.51


### Added:
 - added role support (listing only)

### Changed:
 - bug fixes

## Version 0.5

### Added:
 - user support added

### Changed:
 - fix for port and protocol setting
 - [fix for #11](https://github.com/delphix/dxm-toolkit/issues/11) - Output in JSON for metadata fetch
 - [fix for #15](https://github.com/delphix/dxm-toolkit/issues/15) - Multitenant for profile job
 - [fix for #16](https://github.com/delphix/dxm-toolkit/issues/16) - fix for MS SQL and Sybase connectors



## Version 0.42

### Added:
 - log export

### Changed:
 - various bug fixes

## Version 0.4

### Added:
 - support for sync API to export / import object between engines
 - support for Delphix Engine 5.3
 - column list is displaying a data type plus column type (index, FK, PK)

### Changed:
 - various bug fixes
 - UTF-8 related bug fixes
 - column save / batch format file is changed to similar to GUI inventory export


## Version 0.3

### Added:
 - support for profile (sets, expressions, jobs)
 - support for export/import/check ruleset with all depended objects into JSON files  

### Changed:
 - various bug fixes
 
## Version 0.22

### Changed:
 - fix for adding file into files rulesets
 - other small bug fixs

## Version 0.21

### Changed:
 - bug fixed for status in job list
 - bug fixed for same connector id for file and database connectors

## Version 0.2

### Added:
 - jobs queue added - multiple jobs can be run in parallel or serial

### Changed:
 - bug fixed for on the fly job
 - bug fixed for listing jobs

## Version 0.1

Initial release of DXM toolkit.
It's supporting the following operations:

- adding an application
- listing/adding/deleting an environment
- listing/adding/deleting a container
- listing/adding/deleting/cloning a ruleset
- listing/adding/deleting a metadata for ruleset (tables or files)
- listing/adding/deleting/setting as masked/unmasked a column for metadata (table or file)
- batch algorithm replace for columns
- load/save rulesets from/to CSV files
- load/save columns from/to CSV files
- list/adding/deleting/starting/cancelling/updating/copy a masking job
- listing/updating a table or file details ( like adding a key, where clause)
- listing/adding/deleting a file format
