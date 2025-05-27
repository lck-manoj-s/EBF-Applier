import os
from collections import defaultdict
from .Apply import Apply

class Check:

    def __init__(self):
        self.items = []
        self.folders = defaultdict(list)
        self.allowed_folders = ["plugins", "features","variants"]
        self.file_obj = None

    # Check if the provided path exists and is a directory.
    def check_paths(self, path):
        if not path:
            print("Path is empty.")
            return False
        
        return os.path.exists(path) and os.path.isdir(path)
    
    def get_folders(self, path: str) -> bool:
        if not self.check_paths(path):
            print(f"Path '{path}' does not exist or is not a directory.")
            return []
        
        self.items = os.listdir(path)

        if not self.items:
            print(f"No items found in the directory: {path}")
            return False
        
        return True
    
    # List all files in the provided directory path.
    def list_files(self, path: str) -> None:
        isItems = self.get_folders(path)

        if isItems:
            for item in self.items:
                item_path = os.path.join(path, item)
                print("\n",item)

                # Check if the item is a file
                if os.path.isfile(item_path):
                    print(f"File: {item}")

                # Check if the item is a directory and list its contents
                if os.path.isdir(item_path):
                    files = os.listdir(item_path)
                    if files:
                        for file in files:
                            print(f"    - {file}")
                            self.folders[item].append(file)
                    else:
                        print(f"Directory: {item} is empty.")

    def create_log(self, path: str) -> None:
        if not self.check_paths(path):
            print(f"Path '{path}' does not exist or is not a directory.")
            return
        
        log_file = os.path.join(path, "ebf_log.txt")
        self.file_obj = open(log_file, "w")
        print(f"Log file created at: {log_file}")
    
    def startProcessing(self, hotfolder: str, pim: str) -> None:
        if not self.check_paths(hotfolder):
            print("Invalid EBF path provided. Please check and try again.")
            return

        if not self.check_paths(pim):
            print("Invalid PIM path provided. Please check and try again.")
            return
        
        # List all files in the hotfolder
        self.list_files(hotfolder)

        print("\nAll the files in the hotfolder will be processed. Please ensure these are the correct files.")
        proceed = input("Do you want to proceed? (yes/no): ").strip().lower()

        if proceed != 'yes':
            print("Exiting the program.")
            return
        
        self.create_log(hotfolder)
        if not self.file_obj:
            print("Log file not created. Exiting the program.")
            return
        
        startEBF = Apply()

        for items, folders in self.folders.items():
            for folder in folders:
                hotfolder_path = os.path.join(hotfolder, items, folder)
                pim_path = os.path.join(pim, items, folder)

                # Check if the folder is in the allowed folders list
                if folder in self.allowed_folders:
                    if self.check_paths(pim_path):
                        self.file_obj.write(f"Processing folder: {folder} in {items}\n")
                        startEBF.process(src=hotfolder_path, dst=pim_path, fileObj=self.file_obj)
                    else:
                        self.file_obj.write(f"Skipping folder: {folder} in {items} does not exist in PIM path.\n")
                else:
                    self.file_obj.write(f"Skipping folder: {folder} in {items} as it is not allowed.\n")