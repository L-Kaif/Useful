import base.powershell

command = '(Get-CimInstance Win32_ComputerSystemProduct).UUID'

print(base.powershell.run_command(command))