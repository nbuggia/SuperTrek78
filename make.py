#!/usr/bin/env python3

import argparse
import subprocess
import sys
import os
import shutil

VENV_DIR = "venv"
REQUIREMENTS_FILE = "requirements.txt"
REQUIREMENTS_DEV_ENVIRON_FILE = "requirements-dev.txt"
APP_ENTRY = "main.py"  

def setup():
    # Create virtual environment
    if not os.path.isdir(VENV_DIR):
        print("[*] Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True)
    else:
        print("[*] Virtual environment already exists.")

    # Install requirements
    pip = os.path.join(VENV_DIR, "bin", "pip") if os.name != "nt" else os.path.join(VENV_DIR, "Scripts", "pip.exe")
    print("[*] Installing requirements...")
    subprocess.run([pip, "install", "--upgrade", "pip"])
    subprocess.run([pip, "install", "-r", REQUIREMENTS_FILE], check=True)
    subprocess.run([pip, "install", "-r", REQUIREMENTS_DEV_ENVIRON_FILE], check=True)

def run():
    python = os.path.join(VENV_DIR, "bin", "python") if os.name != "nt" else os.path.join(VENV_DIR, "Scripts", "python.exe")
    print("[*] Running SuperTrek78...")
    subprocess.run([python, APP_ENTRY], check=True)


def test():
    python = os.path.join(VENV_DIR, "bin", "python") if os.name != "nt" else os.path.join(VENV_DIR, "Scripts", "python.exe")
    print("[*] Running tests...")
    subprocess.run([python, "-m", "unittest", "discover", "-s", "tests"], check=True)


def clean():
    print("[*] Cleaning up temporary files...")
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if name.endswith(".pyc") or name.endswith(".pyo"):
                os.remove(os.path.join(root, name))
        for name in dirs:
            if name == "__pycache__":
                shutil.rmtree(os.path.join(root, name))
    print("[*] Clean complete.")


def main():
    parser = argparse.ArgumentParser(description="Manage project")
    parser.add_argument("command", choices=["setup", "run", "test", "clean"], help="Command to run")

    args = parser.parse_args()
    if args.command == "setup":
        setup()
    elif args.command == "run":
        run()
    elif args.command == "test":
        test()
    elif args.command == "clean":
        clean()


if __name__ == "__main__":
    main()
