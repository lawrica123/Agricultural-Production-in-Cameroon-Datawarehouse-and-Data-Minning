# Agricultural-Production-in-Cameroon-Datawarehouse-and-Data-Minning

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Fork and Clone the Repository](#fork-and-clone-the-repository)
3. [Create Datawarehouse](#Create Datawarehouse)
4. [Testing Connection](#Testing Connection)
5. [Load data into Datawarehouse](#Load data into Datawarehouse)


---

## Prerequisites

Before you begin, ensure you have the following software installed:

- **Python**: Version 3.7 or higher
- **pip**: Python package installer
- **MySQL Workbench 8.0 CE**: to create your database
- **Git**: To clone the repository 

You can check the installed versions by running the following commands:

```bash
python --version
pip --version
git --version
```

## Fork and Clone the Repository

1. Go to the [repository URL](https://github.com/GinaBlack/Agricultural-Production-in-Cameroon-Datawarehouse-and-Data-Minning).
2. Click on the **Fork** button (top-right corner) to fork the repository to your own GitHub account.
3. Clone your forked repository to your local machine:

    ```bash
    https://github.com/<Your-github-name>/Agricultural-Production-in-Cameroon-Datawarehouse-and-Data-Minnin.git
    ```

4. Navigate into the project directory:

    ```bash
    cd Agricultural-Production-in-Cameroon-Datawarehouse-and-Data-Minning
    ```

## Installation

1. **Create a Virtual Environment** (optional but recommended):

    ```bash
    python -m venv venv
    ```

2. **Activate the Virtual Environment**:

   - On **Windows**:
    
        ```bash
        venv\Scripts\activate
        ```

   - On **Mac/Linux**:
    
        ```bash
        source venv/bin/activate
        ```

3. **Install the required dependencies**:

    ```bash
    pip install 
                matplotlib          
                mysql-connector      
                mysql-connector-python 
                numpy                  
                pandas                 
                pillow                 
                scikit-learn         
                scipy             
                six                   
                SQLAlchemy            
                wheel                 
    ```

    Install all the necessary libraries for the python scripts to run.

---

## Contributing

If you'd like to contribute to this project:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to your branch (`git push origin feature-branch`).
6. Create a new pull request.

---

#Create Datawarehouse

- open MySQL 8.0 Command Line Client
- login 
- copy the  sql query from create database and tables.txt file and paste in its CLI and press enter
- open your workbench login refresh and verify if the database has been created


---

#Testing Connection

-After ccreating your environment open the check connect.py script
- Edit 
        host='localhost', #with your localhost
        user='root',       #with your username
        password='000000', #your database password
- run the script 

---

#Load data into Datawarehouse

- using the credentials above edit the load.py script to establish the Connection
- Run the script

