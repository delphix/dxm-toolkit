#!/bin/bash

cd /github/workspace/dxm/lib/DxEngine
mv secret.py secret.py.orig
cat secret.py.orig | sed -e "s/changemechangemechagemechangemec/${INPUT_ENCKEY}/" > secret.py

cat /github/workspace/dxm/lib/DxEngine/secret.py

cd /github/workspace/
ls -l 
python3 setup.py install
pyinstaller --onefile --clean dxmc.py
cd /github/workspace/dist



