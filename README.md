## WEB
This repository is a part of the SAP project and was developed by [Parsa Safaie](https://github.com/parsasafaie) to handle image processing tasks within the larger SAP system.

Click [here](https://github.com/SAP-Program) to visit the SAP organization.

## Repository Cloning
To clone this repository, open your terminal in the desired directory and run:
```
git clone https://github.com/SAP-Program/WEB.git
```

## Download Submodules
Sometimes, when you clone the project, submodule files are not downloaded automatically. To fix this, simply run:
```
git submodule init
git submodule update
```

## Installing Dependencies
To install the required dependencies, open a terminal and run:
```
pip install -r requirements.txt
``` 

## Fix an inconsistency
Due to the structure of the WEB repository, there is a minor inconsistency between the main repository and its submodule. To fix this, navigate to: 
```
app/server_side/directory_manager.py
```
Then, on **line 4**, replace: 
```
from log_handler import log_message
```
with:
```
from app.server_side.log_handler import log_message
```

Now you're ready! 🚀

## Running the Project
To run the project, simply execute run.py:
```
python run.py
```
You can then access the output at:
```
http://127.0.0.1:5000
```
>(Note: The actual URL may differ. Check the Flask log in your runnig terminal for the correct address.)