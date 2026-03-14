import os
import zipfile

class GetFile:
    def __init__(self, ebf_path: str) -> None:
        self.return_path = ""
        self.ebf_path = ebf_path
        self.client_folders = []
        self.server_folders = []
    
    # Separate client and server EBF zip files into respective lists based on naming conventions.
    def separateClientServerFolders(self) -> None:
        for root, _, files in os.walk(self.ebf_path):
            for file in files:
                if "_client_" in file.lower() and file.endswith(".zip"):
                    self.client_folders.append(os.path.join(root, file))

                elif "_server_" in file.lower() and file.endswith(".zip"):
                    self.server_folders.append(os.path.join(root, file))
        
        self.unzipFolders()
    
    # Unzip all client and server EBF zip files into their respective directories for easier access.
    def unzipFolders(self) -> None:
        # Unzip client folders
        for i, zip_path in enumerate(self.client_folders):
            try:
                extract_path = os.path.join(os.path.dirname(zip_path), os.path.splitext(os.path.basename(zip_path))[0])
                os.makedirs(extract_path, exist_ok=True)

                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)

                os.remove(zip_path)
                self.client_folders[i] = extract_path

            except Exception as e:
                raise RuntimeError(f"Failed to unzip {zip_path}: {str(e)}")
        
        # Unzip server folders
        for i, zip_path in enumerate(self.server_folders):
            try:
                extract_path = os.path.join(os.path.dirname(zip_path), os.path.splitext(os.path.basename(zip_path))[0])
                os.makedirs(extract_path, exist_ok=True)

                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)

                os.remove(zip_path)
                self.server_folders[i] = extract_path

            except Exception as e:
                raise RuntimeError(f"Failed to unzip {zip_path}: {str(e)}")
    
    # Retrieve the file path for the specified component and accelerator from the respective lists of client or server folders.
    def getFilePath(self, component_name: str, accleartor: str = "") -> str:
        if component_name.lower() == "server":
            if not self.server_folders:
                raise FileNotFoundError("No server EBF zip files found in the provided path.")
            
            else:
                if accleartor == "":
                    for path in self.server_folders:
                        if "_win64" in path.lower():
                            self.return_path = os.path.join(path, component_name.lower())
                            break
                else:
                    for path in self.server_folders:
                        if accleartor.lower() in path.lower():
                            self.return_path = os.path.join(path, component_name.lower())
                            break
        
        elif component_name.lower() == "client":
            if not self.client_folders:
                raise FileNotFoundError("No client EBF zip files found in the provided path.")
            
            else:
                if accleartor == "":
                    for path in self.client_folders:
                        if "_win64" in path.lower():
                            self.return_path = os.path.join(path, component_name.lower())
                            break
                else:
                    for path in self.client_folders:
                        if accleartor.lower() in path.lower():
                            self.return_path = os.path.join(path, component_name.lower())
                            break
        
        if not self.return_path:
            raise FileNotFoundError(f"No EBF zip file found for the specified component '{component_name}' with the given accelerator '{accleartor}'.")
        
        return self.return_path
