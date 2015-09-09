import sys
import os
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

exe = Executable(script="towers.py", base=base)

include_files = [os.path.join("resources", "graphics"),
                 os.path.join("resources", "fonts")]
includes = []
excludes = []
packages = []

setup(version="1.0",
      description="A game about towers",
      author="cactusson",
      name="Towers",
      options={"build_exe": {"includes": includes,
                             "include_files": include_files,
                             "packages": packages,
                             "excludes": excludes}},
      executables=[exe])
