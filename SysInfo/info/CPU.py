import base.powershell

command = '(Get-CimInstance Win32_Processor) | ForEach-Object {"$($_.Manufacturer)|$($_.Name)|$($_.NumberOfCores)"}'

print(base.powershell.run_command(command).replace('|', ', '))