import subprocess
import sys
import time

def InstallModule(package):
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))

print("Installing required files...")

InstallModule("colorama")
InstallModule("requests")



print("All files have been installed, you can now use the main program by running main.py")
print("You will not need to run this file ever again")
print("You can now close this")

time.sleep(100)
