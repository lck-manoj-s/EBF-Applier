import os

class Check:

    # Check if the provided path exists and is a directory.
    def check_paths(self, path):
        if not path:
            print("Path is empty.")
            return False
        
        return os.path.exists(path) and os.path.isdir(path)
    
    # List all files in the provided directory path.
    def list_files(self, path):

        if not self.check_paths(path):
            print(f"Path '{path}' does not exist or is not a directory.")
            return
        
        items = os.listdir(path)

        if not items:
            print(f"No items found in the directory: {path}")
            return
        
        else:
            for item in items:
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
                            print(f"  - {file}")
                    else:
                        print(f"Directory: {item} is empty.")
    
    def startProcessing(self, hotfolder, pim_path):
        if not self.check_paths(hotfolder):
            print("Invalid EBF path provided. Please check and try again.")
            return

        if not self.check_paths(pim_path):
            print("Invalid PIM path provided. Please check and try again.")
            return
        
        # List all files in the hotfolder
        self.list_files(hotfolder)

        print("\nAll the files in the hotfolder will be processed. Please ensure these are the correct files.")
        proceed = input("Do you want to proceed? (yes/no): ").strip().lower()

        if proceed != 'yes':
            print("Exiting the program.")
            return