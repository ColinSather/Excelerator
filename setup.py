import sys, os
import winreg as reg

cwd = os.getcwd()
python_exe = sys.executable

key_path = r"Directory\\Background\\shell\\excelerator"
key = reg.CreateKeyEx(reg.HKEY_CLASSES_ROOT, key_path)

reg.SetValue(key, '', reg.REG_SZ, "&Excelerator")

key1 = reg.CreateKeyEx(key, r"command")
print(python_exe)
print(f'"{cwd}\\main.py"')
reg.SetValue(key1, '', reg.REG_SZ, python_exe + f' {cwd}\\main.py %*')


# This script kinda works 
# Computer\HKEY_CLASSES_ROOT\Excel.CSV\shell\Excelerator\command

# above path is where the csv context menu lives in the registry editor
# Value Data: F:\python_xlsx\venv\Scripts\python.exe F:\python_xlsx\main.py %1