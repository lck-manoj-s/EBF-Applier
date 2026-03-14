from Loading import loading
from Backup import Backup
from Apply import Apply
from GetFile import GetFile

from time import sleep
import os
import datetime

class Main:
    def __init__(self) -> None:
        self.file_obj = None
        self.apply_obj = None
        self.client = ""
        self.server = ""
        self.ebf_path = ""

    # Check if the provided path exists; create if destination path doesn't exist
    def checkPath(self, dirPath: str, dest: bool) -> None:
        if not os.path.exists(dirPath):
            if dest:
                os.makedirs(dirPath)
            else:
                raise FileNotFoundError(f"Directory path '{dirPath}' does not exist.")
            
    # Display welcome message and instructions
    def welcome(self) -> None:
        print("+---------------------------------------------------------------------------------------+")
        print("|                                    PIM EBF APPLIER                                    |")
        print("+---------------------------------------------------------------------------------------+")
        print("|                                                                                       |")
        print("| 1. It is mandatory to use proper versions of PIM to apply the EBF                     |")
        print("| 2. The PIM server must be stopped before executing this program                       |")
        print("| 3. Database.exe must be run before proceeding if available                            |")
        print("| 4. Just extract the EBF folder and don't touch any folders inside it                  |")
        print("| 5. Have a look at the extracted folders before choosing the components to apply EBF   |")
        print("|                                                                                       |")
        print("| To stop processing, press Ctrl+C at any time and wait for 5 seconds.                  |")
        print("|                                                                                       |")
        print("+---------------------------------------------------------------------------------------+\n")

    # Create a log file in the specified path.
    def createLogFile(self, path: str) -> None:
        self.checkPath(path, dest=True)

        log_file = os.path.join(path, "ebf_log.txt")
        self.file_obj = open(log_file, "w")
        print(f"-----Log file created at: {log_file}------\n")
    
    def getBackupFileName(self, target: str) -> str:
        default_name = f"{target.lower()}_backup.zip"
        backup_name = input(f"Enter the name for the {target} backup zip file (default: {default_name}): ").strip()
        return backup_name if backup_name else default_name

    # Starts applying EBF based on user selections for components.
    def componentProcessing(self, target: str, dest: str, getFileObj: GetFile) -> None:
        target_EBF = getFileObj.getFilePath(component_name=target, accleartor="win64")

        self.checkPath(target_EBF, dest=False)


        self.apply_obj.startProcessing(src=target_EBF, dest=dest, file_obj=self.file_obj)
        print(f"\n{target} EBF application completed !!...\n")

        component_map = {"1": "GDSN", "2": "Variant", "3": "AI"}

        print("\n\nList of components for which EBF can be applied")
        print("1. GDSN\n2. Variants\n3. Claire AI\n")
        
        to_apply = input("Do you want to apply EBF to any of above components? (yes/no): ").strip().lower()

        if to_apply == "yes":
            components = input("Enter the numbers corresponding to the components (space-separated): ")
            components =  [comp.strip() for comp in components.split(" ")]

            for comp in components:
                if comp in component_map:
                    comp_name = component_map[comp]
                    comp_EBF = getFileObj.getFilePath(component_name=target, accleartor=comp_name)

                    self.checkPath(comp_EBF, dest=False)

                    self.apply_obj.startProcessing(src=comp_EBF, dest=dest, file_obj=self.file_obj)
                    print(f"\n{target} {comp_name} EBF application completed !!...\n")

                else:
                    print(f"Invalid component selection: {comp}. Skipping...")

        else:
            return

    def main(self) -> None:
        
        self.welcome()

        # Display loading bar
        print("Have a look at the notes above and wait for the loading to complete.\n")
        loading(duration=10)
        print("\n")

        
        # Prompt user for selection between client and server
        menu = """
Please select the target for which EBF needs to be applied:
1. Server
2. Client
3. Both Server and Client
"""
        print(menu)

        target = int(input("Enter your choice (1/2/3): ").strip())

        if target not in [1, 2, 3]:
            raise ValueError("Invalid selection. Exiting the application.")

        apply_to_server = target in [1, 3]
        apply_to_client = target in [2, 3]

        # Prompt user for PIM server, client & EBF folder paths
        if apply_to_server:
            example_server_path = r"C:\Informatica\PIM\server"
            self.server = input(f"Enter the path to the PIM server folder (Ex:- {example_server_path}): ")
            self.checkPath(self.server, dest=False)

        if apply_to_client:
            example_client_path = r"C:\Informatica\PIM\client"
            self.client = input(f"Enter the path to the PIM client folder (Ex:- {example_client_path}): ")
            self.checkPath(self.client, dest=False)

        print("\n")
        # Create backup directory
        current_date = datetime.datetime.now().strftime("%d-%m-%Y")
        backup_dir = os.path.join("C:\\Informatica\\PIM\\backups", current_date)
        self.checkPath(backup_dir, dest=True)

        # Create log file in the backup directory
        self.createLogFile(backup_dir)

        # Create an instance of Backup class
        backup = Backup().backup

        # Prompt user for backup file names
        if apply_to_server:
            backup_server = self.getBackupFileName("Server")
            
            print("\n\nInitiating server backup. This operation may take a few moments.\n")
            backup(src=self.server, dest=backup_dir, fileName=backup_server)

            self.file_obj.write(f"Server backup created at: {os.path.join(backup_dir, backup_server)}\n")

        if apply_to_client:
            print("\n")
            backup_client = self.getBackupFileName("Client")

            print("\n\nInitiating client backup. This operation may take a few moments.\n")
            backup(src=self.client, dest=backup_dir, fileName=backup_client)
            
            self.file_obj.write(f"Client backup created at: {os.path.join(backup_dir, backup_client)}\n")

        print("\n\n")
        # Prompt user for EBF folder path
        example_ebf_path = r"C:\PIM_10.5.xx.xx.xx"
        self.ebf_path = input(f"Enter the path to the EBF folder (Ex:- {example_ebf_path}): ")
        self.checkPath(self.ebf_path, dest=False)

        # Create an instance of Apply class
        self.apply_obj = Apply()
        print("\n")

        # Create an instance of GetFile class and separate client and server folders from the provided EBF path
        getFile = GetFile(self.ebf_path)
        getFile.separateClientServerFolders()

        # Process components based on user selection
        if apply_to_server:
            self.componentProcessing(target="Server", dest=self.server, getFileObj=getFile)
        
        if apply_to_client:
            self.componentProcessing(target="Client", dest=self.client, getFileObj=getFile)
        



        
if __name__ == "__main__":
    try:
        mainObj = Main()
        mainObj.main()

        print("EBF application process completed. Please check the log file for details or start the server.")
        print("\n\n-->> Thank you for using the PIM EBF Applier. <<--\n")

    except Exception as e:
        print(f"An error occurred during the execution: {e}")
    
    finally:
        if mainObj.file_obj:
            mainObj.file_obj.close()
        
        sleep(5)