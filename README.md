# WEB
This repository is a part of the SEPAD project and was developed by [Parsa Safaie](https://github.com/parsasafaie) to serve schools within the larger SEPAD system.

Click [here](https://github.com/SEPAD-Project) to visit the SEPAD organization.

The application is currently deployed and accessible at http://185.4.28.110:85 where you can view the live results.

>Note: This application has Windows-specific dependencies and is optimized for Windows environments.

## Repository Cloning
To clone this repository, open your terminal in the desired directory and run:
```bash
git clone --recurse-submodules https://github.com/SEPAD-Project/WEB.git
```
Then, navigate to the repository directory:
```bash
cd Web
```

## Installing Dependencies
   1. Create a virtual environment:
      ```bash
      python -m venv .venv
      ```

   2. Activate the virtual environment:
      ```bash
      .venv\Scripts\activate.bat
      ```

## Required Dependencies For Flask limiter
For run project, you need to install redis app:
   1. Download the msi file from [Microsoft's Redis releases](https://github.com/microsoftarchive/redis/releases)
   2. Follow the installation wizard
   3. Select default port (6379)


## Running the Project
To run the project, simply use `run.bat` file.
You can then access the output at:
```
http://0.0.0.0:85
```
