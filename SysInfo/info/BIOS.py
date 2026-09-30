import base.powershell

command = '(Get-CimInstance Win32_BIOS) | ForEach-Object {"$($_.Manufacturer)|$($_.SMBIOSBIOSVersion)|$($_.SerialNumber)|$($_.ReleaseDate)"}'

print(base.powershell.run_command(command))