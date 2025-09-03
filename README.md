[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/SEPAD-Project/WebApplication/blob/main/README.md)
[![fa](https://img.shields.io/badge/lang-fa-blue.svg)](https://github.com/SEPAD-Project/WebApplication/blob/main/README.fa.md)
# WebApplication
This repository is a part of the SEPAD project and was developed by [Parsa Safaie](https://github.com/parsasafaie) to serve schools within the larger SEPAD system.

Click [here](https://github.com/SEPAD-Project) to visit the SEPAD organization.

The application is currently deployed and accessible at http://sepad-project.ir/ where you can view the live results.


## Cloning the Repository
To clone the repository with its submodules, run:
```bash
git clone --recurse-submodules https://github.com/SEPAD-Project/WebApplication.git
cd WebApplication
```

## Installing Dependencies
> Recommended Python version for this project is: 3.10.*
   1. Create a virtual environment:
      ```bash
      python -m venv .venv
      ```

   2. Activate the virtual environment:
      - On **Windows**:

         ```bash
         .venv\Scripts\activate.bat
         ```
      - On **Linux**:

         ```bash
         source .venv\bin\activate
         ```

   3. Install the dependencies:
      ```bash
      pip install -r requirements.txt
      ```

## Celery & Redis Setup
This project uses Celery for asynchronous task management and requires Redis as the message broker.
   - On **Windows**:
      1. Download the Redis installer from [Microsoft's Redis releases](https://github.com/microsoftarchive/redis/releases).
      2. Follow the installation wizard.
      3. Use the default port 6379 when prompted.
   - On **Linux**:

      Install Redis using your package manager:
      ```bash
      sudo apt update
      sudo apt install redis
      ```


## Running the Project
To start the project (Django + Celery), use the scripts file:

- On **Windows**:
   ```bash
   scripts/start_server.bat
   ```
- On **Linux**:
   ```bash
   chmod +x scripts/start_server.sh
   scripts/start_server.sh
   ```

After starting, the application will be accessible at:
```
http://0.0.0.0:8000
```
