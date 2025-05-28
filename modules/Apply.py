import os
from os.path import isdir, join
from shutil import rmtree, copy2, copytree
from typing import TextIO
import re

class Apply:
    def __init__(self):
        self.source = []
        self.target = []

    def process(self, src: str, dst: str, fileObj: TextIO) -> None:
        self.getFiles(dir=src, source=True)
        self.getFiles(dir=dst, source=False)

        self.changeFiles(src=src, dst=dst, fileObj=fileObj)

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

    def getFiles(self, dir: str, source: bool) -> None:
        items = os.listdir(dir)

        if source:
            self.source.extend(items)
        else:
            self.target.extend(items)

    def changeFiles(self, src: str, dst: str, fileObj: TextIO) -> None:
        copied_files, removed_files = 0, 0 

        for sfile in self.source:

            sfile_path = os.path.join(src, sfile)
            name = self.getFileName(file=sfile, file_path=sfile_path)

            src_path = join(src, sfile)

            for tfile in self.target:

                if tfile.startswith(name):
                    removed_files += 1

                    dst_path = join(dst, tfile)

                    if isdir(dst_path):
                        rmtree(dst_path)
                    
                    if os.path.exists(dst_path):
                        os.remove(dst_path)
                
                    fileObj.write("File Deleted: %s \n"%(dst_path))
            
            copied_files += 1
            dst_path = join(dst, sfile)
            
            if isdir(src_path):
                os.mkdir(dst_path)
                copytree(src_path, dst_path, dirs_exist_ok=True)
                    
            else:
                copy2(src_path, dst)  

            fileObj.write("File Copied: %s\\%s\n\n"%(dst, sfile))

        fileObj.write("Total number of items removed: %d\nTotal number of items copied: %d\n"%(removed_files, copied_files))

        #Clearing the source and target lists
        self.source.clear() 
        self.target.clear()