# FacialDetectionWithDatabase
This is my project showcasing Computer Vision application: "Checking attendance"

## Table of Contents

- [Installation](#installation)
- [Project Overview](#project-overview)
- [Usage](#usage)
- [License](#license)

**Functionaility:**
1. Can count attendance of preloaded student and recognise face
2. Linked with Real Time Database, powered by Firebase by Google
3. Can retrieved people's information from Firebase with different traits, demonstrating in json format

## Installation

To get started, you can follow these steps to set up the project on your local machine:

### Prerequisites
- To install requirements
```
pip install requirement.txt
```
- Python 3.6 or higher installed on your system.
- Git installed on your system.

### Clone the Repository

You can clone this repository using the following command:

```bash
git clone https://github.com/phanng0605/facialDetectionWithDatabase.git
```

### Create a Virtual Environment (Optional but recommended)
It's a good practice to create a virtual environment for your project to manage dependencies. You can create one using Python's built-in venv module:
```
python -m venv myenv
```
or by conda 
```
conda create --name environment_name python=3.7
```

### Activate the virtual environment:

On Windows:
```
myenv\Scripts\activate
```

On macOS and Linux:
```
source myenv/bin/activate
```

Through Conda
```
conda activate environment_name
```
### Install Dependencies
Navigate to the project directory and install the required packages using pip:
```
pip install -r requirements.txt
```

### Project Overview
This project includes the following files and directories:

AddDataToDatabase.py
EncodeFile.p
EncodeGenerator.py
EncodingList.p
README.md
facerecognitionrealtime-746da-firebase-adminsdk-d6luq-ccd6437c55.json
main.py
tempCodeRunnerFile.py
LICENSE: MIT License file for the project.

### Usage
Once you have installed the dependencies and set up the project, you can run the web application locally:
```
python main.py
```


