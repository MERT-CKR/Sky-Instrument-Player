import subprocess, sys#, os
import time
import pkg_resources
from modules.utils import print_green

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
        print_green("Done, Its ready")
        time.sleep(2)
        
    else:
        print_green("Done, Its ready")
        time.sleep(2)
        # script_path = os.path.abspath(__file__)
        # os.remove(req_path)
        # os.remove(script_path)

if __name__ == "__main__":
    main()
