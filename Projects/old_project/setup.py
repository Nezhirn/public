from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "asyncio", "subprocess", "qasync", "PySide6"],
    "includes": ["res_rc"],
    "excludes": [],
    "include_files": []
}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="SpeedTestApp",
    version="0.1",
    description="A speed test application",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
)
