from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_exe_options = dict(packages = ["idna"], excludes = [])
install_options = dict(install_exe = 'dist')

base = 'Console'

executables = [
    Executable('dxmc.py', base=base)
]

setup(name='dxmc',
      version = '0.1',
      description = '',
      options = {"build_exe": build_exe_options,
                 "install": install_options},
      executables = executables)
