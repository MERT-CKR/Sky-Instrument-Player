import subprocess, sys, os
import pkg_resources
import time
req_path ="modules/requirements.txt"
def main():
    with open(req_path) as f:
        required = f.read().splitlines()

    
    installed = {pkg.key for pkg in pkg_resources.working_set}
    
    missing = [
        pkg for pkg in required 
        if pkg.split("==")[0].lower() not in installed
    ]

    if missing:
        print("Missing package:", missing)
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
    else:
        script_path = os.path.abspath(__file__)
        print("Done, now You can open Sky-Auto Instrument Player.py")
        time.sleep(2)
        os.remove(req_path)
        os.remove(script_path)

if __name__ == "__main__":
    main()
