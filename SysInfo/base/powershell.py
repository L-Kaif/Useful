import subprocess

CREATE_NO_WINDOW = 0x08000000

def run_command(command):
    return subprocess.check_output(
        ["powershell", "-NoProfile", "-Command", command],
        text=True,
        creationflags=CREATE_NO_WINDOW,
    ).strip()