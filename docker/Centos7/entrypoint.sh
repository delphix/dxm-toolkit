#!/bin/bash

source /root/.bashrc

cd /github/workspace/dxm/lib/DxEngine
mv secret.py secret.py.orig
cat secret.py.orig | sed -e "s/changemechangemechagemechangemec/${INPUT_ENCKEY}/" > secret.py


cd /github/workspace/
ls -l 
pip install six
pip install pyinstaller
python3 setup.py install
pyinstaller --onefile --clean dxmc.py
cd /github/workspace/dist



