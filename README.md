# WEB
This repository is a part of the SEPAD project and was developed by [Parsa Safaie](https://github.com/parsasafaie) to serve schools within the larger SEPAD system.

Click [here](https://github.com/SEPAD-Project) to visit the SEPAD organization.

## Repository Cloning
To clone this repository, open your terminal in the desired directory and run:
```bash
git clone https://github.com/SEPAD-Project/WEB.git
```
Then, navigate to the repository directory:
```bash
cd Web
```

## Downloading Submodules
Sometimes, when you clone the project, submodule files are not downloaded automatically. To fix this, simply run:
```bash
git submodule init
git submodule update
```

## Installing Dependencies
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
2. Activate the virtual environment:
   
   * On Windows:
     ```bash
     .venv\Scripts\activate.bat
     ```

   * On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ``` 

Now you're ready! 🚀

## Running the Project
To run the project, simply execute run.py:
```bash
python run.py
```
You can then access the output at:
```
http://127.0.0.1:2568
```
>(Note: The actual URL may differ. Check the Flask log in your runnig terminal for the correct address.)
