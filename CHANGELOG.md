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
