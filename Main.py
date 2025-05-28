from .modules import Check, Loading

class Main:
    def __init__(self):
        self.check = Check.Check()
        
    def main(self):
        print("\n----------------------------------------NOTE----------------------------------------\n")
        print("1. Please ensure proper versions of PIM is used to apply the EBF\n")
        print("2. Ensure that the PIM server is stopped before the execution of this program\n")
        print("3. Please have a backup of the PIM folder before proceeding further\n")
        print("4. This program will apply the EBF only with plugins, features for client, server & variants folders\n")
        print("To stop processing, press Ctrl+C at any time.\n")
        print("--------------------------------------------------------------------------------------\n")
        
        # Display loading bar
        print("Have a look at the notes above and wait for the loading to complete.\n")
        Loading.Loading(duration=10)
        print("\n\n")

        # Prompt user for EBF hotfolder and PIM folder paths
        hotfolder = input("Enter the path to the EBF hotfolder: ")
        pim_path = input("Enter the path to the PIM folder: ")

        # Start processing the EBF folder
        self.check.startProcessing(hotfolder, pim_path)

        print("\nProcess of applying EBF completed. Please start the server to verify the changes.\n")
        
if __name__ == "__main__":
    main = Main()
    main.main()