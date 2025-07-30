import sys
from cx_Freeze import setup, Executable

# Устанавливаем base для Windows GUI приложения
base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable("main.py", base=base, target_name="SpeedTestApp.exe")
]

# Включаем необходимые файлы и пакеты
buildOptions = dict(
    packages=["PySide6", "subprocess"],
    includes=["res_rc"],
    include_files=[]
)

setup(
    name="SpeedTestApp",
    version="1.0",
    description="SpeedTest Application",
    options=dict(build_exe=buildOptions),
    executables=executables
)
