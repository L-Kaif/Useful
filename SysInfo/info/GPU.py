import base.powershell

command = '(Get-CimInstance Win32_VideoController) | ForEach-Object {"$($_.AdapterCompatibility)|$($_.Name)"}'

gpus = base.powershell.run_command(command).splitlines()

for gpu in gpus:
    manufacturer, name = gpu.split("|")
    print(manufacturer, "-", name)