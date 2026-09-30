import base.powershell

command = "Get-NetAdapter | Where-Object {$_.Status -eq 'Up'}"
print(base.powershell.run_command(command))