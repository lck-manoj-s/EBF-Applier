import os
from os.path import isdir, join
from shutil import rmtree, copy2, copytree
from typing import TextIO
import re

class Apply:
    def __init__(self):
        self.allowed = ['features', 'plugins']
        
    def checkPath(self, dirPath: str) -> None:
        if not os.path.exists(dirPath):
            raise FileNotFoundError(f"Directory path '{dirPath}' does not exist.")
        
    def getFileName(self, file: str, file_path: str) -> str:
        n = len(file)

        if isdir(file_path):
            n -= 1
        
        elif file[n-4:n] == '.jar':
            file = file[0:n-4]
            n -= 5
        
        revision = file[n-6:]

        #print("File name: %s, Revison: %s\n"%(file, revision))
        
        pattern = r'^\.r\d{5}$'
        if re.match(pattern, revision):
            n -= 6

        return file[0:n]
    
    def startProcessing(self, src: str, dest: str, file_obj: TextIO) -> None:
        
        for folder in os.listdir(src):
            # Maintain count of copied & removed files
            copied, removed = 0, 0

            # Iterate only through allowed folders in the source directory
            if folder in self.allowed:
                src_folder = join(src, folder)
                dest_folder = join(dest, folder)
                
                try:
                    self.checkPath(dest_folder)

                except FileNotFoundError as e:
                    print(f"Error: {e}\n")
                    return
                
                file_obj.write("-----------------------------------------------------------------------------\n")
                file_obj.write(f"Processing folder: {src_folder}\n")
                file_obj.write("-----------------------------------------------------------------------------\n")

                for src_file in os.listdir(src_folder):
                    src_path = join(src_folder, src_file)
                    src_file_name = self.getFileName(src_file, src_path)

                    for dest_file in os.listdir(dest_folder):

                        if dest_file.startswith(src_file_name):
                            removed += 1

                            dest_path = join(dest_folder, dest_file)

                            # If it's a directory, remove it
                            if isdir(dest_path):
                                rmtree(dest_path)
                            
                            # If it's a file, remove it
                            else:
                                os.remove(dest_path)
                            
                            file_obj.write(f"Item removed: {dest_path}\n")

                    copied += 1
                    copy_path = join(dest_folder, src_file)

                    # Copy the new directory
                    if isdir(src_path):
                        copytree(src_path, copy_path)
                    
                    # Copy the new file
                    else:
                        copy2(src_path, dest_folder)

                    file_obj.write(f"Item copied:  {copy_path}\n\n")

                file_obj.write(f"\nTotal items removed: {removed}\nTotal items copied: {copied}\n")
                file_obj.write("-----------------------------------------------------------------------------\n\n")
            else:
                print(f"\nPlease look into the skipped folder: {join(src,folder)} and apply changes as required\n")
                file_obj.write(f"Skipped folder: {join(src,folder)}\n")