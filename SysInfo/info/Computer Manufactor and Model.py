import base.powershell

command = '(Get-CimInstance Win32_ComputerSystem) | ForEach-Object {"$($_.Manufacturer)|$($_.Model)"}'

print(base.powershell.run_command(command))