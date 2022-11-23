#!/bin/bash

cd /github/workspace/dxm/lib/DxEngine
mv secret.py secret.py.orig
cat secret.py.orig | sed -e "s/changemechangemechagemechangemec/${INPUT_ENCKEY}/" > secret.py


cd /github/workspace/
ls -l
pip3 install -r requirements.txt
python3 setup.py install
pyinstaller --onefile --clean dxmc.py
cd /github/workspace/dist



