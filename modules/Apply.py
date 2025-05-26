import os
from os.path import isdir, join
from shutil import rmtree, copy2, copytree
from typing import TextIO

class Apply:
    def __init__(self):
        self.source = []
        self.target = []

    def process(self, src: str, dst: str, fileObj: TextIO) -> None:
        self.getFiles(dir=src, source=True)
        self.getFiles(dir=dst, source=False)

        self.changeFiles(src=src, dst=dst, fileObj=fileObj)

    def getFileName(self, file: str) -> str:
        n = len(file)

        if file[n-4:n] == '.jar':
            n -= 5
        else:
            n -= 1
        
        while n >= 0 and file[n] != 'r':
            n -= 1
        
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

            name = self.getFileName(sfile)
            src_path = join(src, sfile)

            for tfile in self.target:

                if tfile.startswith(name):
                    removed_files += 1

                    dst_path = join(dst, tfile)

                    if isdir(dst_path):
                        rmtree(dst_path)
                    
                    if os.path.exists(dst_path):
                        os.remove(dst_path)
            
            copied_files += 1
            dst_path = join(dst, sfile)
            
            if isdir(src_path):
                os.mkdir(dst_path)
                copytree(src_path, dst_path, dirs_exist_ok=True)
                    
            else:
                copy2(src_path, dst)  

            fileObj.write("The file %s has been copied to %s\n\n"%(src_path, dst))

        fileObj.write("Total number of items removed: %d\nTotal number of items copied: %d\n"%(removed_files, copied_files))
    
