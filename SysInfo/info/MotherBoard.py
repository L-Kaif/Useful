import base.powershell

command = 'Get-CimInstance Win32_BaseBoard | Format-List *'

print(base.powershell.run_command(command))
