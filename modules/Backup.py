import os
import shutil
import subprocess
import zipfile
import sys

class Backup():
    def __init__(self):
        self.src = ""
        self.dest = ""

    def backup7z(self) -> bool:
        creationflags = 0
        
        if sys.platform.startswith('win'):
            creationflags = subprocess.CREATE_NO_WINDOW
        
        try:
            # Run 7z as administrator using PowerShell to zip the folder with minimal compression (mx=1)
            command = [
                'powershell',
                '-Command',
                f'Start-Process -FilePath "7z" -ArgumentList "a,-tzip,-mx=1,\\"{self.dest}\\",\\"{self.src}\\"" -Verb RunAs -Wait'
            ]
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                creationflags=creationflags
            )
            print(f"Backup completed: {self.dest}")
            return True
        
        except Exception as e:
            print(f"Unexpected error with 7z compression: {e}")
            print("Falling back to standard compression methods.\n")
            return False

    def backupZipfile(self) -> None:
        
        with zipfile.ZipFile(self.dest, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(self.src):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, self.src))
                    
        print(f"Backup completed: {self.dest}")

    def backup(self, src: str, dest: str, fileName: str) -> None:
        self.src = src
        self.dest = os.path.join(dest, fileName)
        
        if shutil.which('7z'):
            success = self.backup7z()
            if success:
                return
        
        self.backupZipfile()
