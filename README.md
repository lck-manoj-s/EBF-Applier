# EBF Applier

## Table of Contents
- [Overview](#overview)
- [What it does](#what-it-does)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  
## Overview
This repository houses the automation scripts designed to streamline the deployment of Emergency Bug Fixes (EBFs) within the Informatica PIM (Product Information Management) system.

## What it does
Informatica PIM EBFs often involve updated `.jar` files for various system components, such as the server, client, and other related modules. Manually replacing these files across your PIM environment can be a time-consuming and error-prone process.

This automation code simplifies this critical task by:

- Identifying the relevant .jar files within the EBF package.
- Locating their corresponding counterparts within the Informatica PIM installation.
- Replacing the older versions of these .jar files with the newer revisions from the EBF folder.

By automating this process, the code ensures that the Informatica PIM system is updated correctly and efficiently with the necessary bug fixes, minimizing downtime and human error.

## Project Structure
```
EBF-Applier
├── modules/
    ├── Apply.py
    ├── Check.py
    ├── Loading.py
    └── __init__.py
├── Main.py
├── __init__.py
├── README.md
```

- `modules/`: Contains all the python files required for running the application.
- `Apply.py`: Scripts that automate the moving of required `.jar` files from the EBF folder to the PIM folder.
- `Check.py`: The python script that is used to validate all the paths used in the process and some listing tasks.
- `Loading.py`: Script that is used to generate the loading part of the application.
- `__init__.py`: Created to make the python look these files as a package.
- `Main.py`: The main python script that is used to interlink & co-ordinate all the modules for efficient working of the application.
- `READE.md`: Project Documentation

## Installation
To run this application, you must have Python installed in the local environment. Clone this repository and start using the application

```
git clone https://github.com/your-username/EBF-Applier.git
```

## Usage
Run Main.py which will prompt the NOTE to be read while the application is loading. After that ensure all proper files are kept in some folder. Enter the path where EBF files are located and the PIM path. Now, the application lists all the content till second level and type `yes` to proceed further. Once entered, it will create a `log` file to record the movements of files and lists the number of deleted and copied files.

```
cd ..
python -m EBF-Applier.Main
```
