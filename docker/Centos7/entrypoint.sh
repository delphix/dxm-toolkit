#!/bin/bash

# TODO: replace encryption key

# cd /github/workspace/lib
# mv dbutils.pm dbutils.orig.pm
# cat dbutils.orig.pm | sed -e "s/put your encryption key here/${INPUT_ENCKEY}/" > dbutils.pm



# cd /github/workspace
# tar czvf /github/workspace/dxtoolkit.tar.gz dxtoolkit2/

# echo ${HOME}

# cp /github/workspace/dxtoolkit.tar.gz ${HOME}


cd /github/workspace
ls -l 
python3 setup.py install
pip3 install pyinstaller
# for pyinstaller to run
pip3 uninstall jeepney -y
pip3 install jeepney
pyinstaller --onefile --clean dxmc.py
cd /github/workspace/dist



