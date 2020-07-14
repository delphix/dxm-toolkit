name: dxmc

on:
  push:
    branches: [ develop ]


jobs:
  build:

    runs-on: windows-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.8
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        python setup.py install
        pip install pyinstaller
        pyinstaller --onefile --clean dxmc.py
