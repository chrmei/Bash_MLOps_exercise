# Linux & Bash

## Exam

You work for a company that sells graphics cards and you are tasked with automating a process for data collection, preprocessing, and training a sales prediction model. Your manager has assigned you a project where you will need to use Linux tools and scripts to automate each step of this process.

Your goal is to design an automated pipeline that allows for:

- **Collect data** from an API every minute,
- **Save it** in a CSV file,
- **Preprocess it**, 
- **Train a prediction model** on this preprocessed data.

The entire process must be automated using **Bash scripts** to chain the different steps, **Python** for data processing and model training, **cron** to schedule the execution of scripts at regular intervals, and a **Makefile** to run all steps in a single command line.

---

#### Setting up the API

In this course, we have seen how a Linux system works. We could have gone even further into detail, but we have built the foundation for the rest of the journey. Follow the instructions below to complete the exercise.

<div class="alert alert-info"><i class="icon circle info"></i>
Exercise to be completed <i>mandatory</i> on the Linux machine provided to you.
</div>

> Connect to your machine and run the following command to retrieve the API

```shell
wget --no-cache https://dst-de.s3.eu-west-3.amazonaws.com/bash_fr/api.tar
```

You now have a file with the `.tar` extension. It is simply an archive similar to a compressed `zip` file, but specific to Linux. To manipulate this file, we use the `tar` command (for _tape archiver_). For all tar-based formats, you will see that the options for tar are the same:

- c : create the archive
- x : extract the archive
- f : use the specified file as a parameter
- v : enable verbose mode.

> Unzip the archive using the following command:

```shell
    tar -xvf api.tar
```

The archive excerpt reveals the _api_ script.

> Launch the `api` script after granting execution rights:

```shell
chmod +x api
./api &
```

Our API is now running on `localhost` (0.0.0.0) on port 5000.

<div class="alert alert-info"> <i class="icon circle info"></i>
It is entirely possible to run the API without putting it in the background, but doing so will block any manipulation on your VM. You will then need to open a 2nd terminal and reconnect to the VM, working only with the 2nd terminal.
</div>

This API reveals the sales per minute of the largest graphics card resellers for the models rtx3060, rtx3070, rtx3080, rtx3090, and rx6700.
It is possible to retrieve this information using the **cURL** command. However, you may not have cURL on your machine; to remedy this, we use `apt` on Linux.


#### Apt Command

`apt` is a package manager that contains various software that you can install quite easily with a single line of code.

On the current version of **Ubuntu 20.04.2 LTS**, you can use the `apt-get` command to manage software via the command line. This allows you to install, update, or remove packages precisely.

```shell
apt-get install software_name
```

In most cases, you need `sudo` to enforce the installation rights of software.

Before installing anything, it is recommended to update the list of available packages on your system by running:

```shell
sudo apt-get update
```

Then, you can apply the available updates for your installed software with:
```shell
sudo apt-get upgrade
```

To remove a software along with its configuration files, you can use the command:
```shell
sudo apt-get purge software_name
```

> Install `curl` with `apt`.

```shell
sudo apt-get update
```
```shell	
sudo apt-get install curl
```

Now that we have `curl`, let's explain the tool.

#### curl Command

cURL, which stands for client URL, is a command-line tool for transferring files with a URL syntax. It supports a number of protocols (HTTP, HTTPS, FTP, and many others). HTTP/HTTPS makes it an excellent candidate for interacting with APIs.

We can, for example, retrieve the sales of RTX 3060 using the following command.

```shell
curl "http://0.0.0.0:5000/rtx3060"
```

### Setting up the exam

- Create a folder exam_LASTNAME where LASTNAME is your last name.
- Add a folder named exam_bash
- Clone the Git for the exam modalities: https://github.com/DataScientest/exam_Bash_MLOps.git in the `English` branch


When cloning the git, you will have the following structure:
```txt
exam_NAME/
  ├── exam_bash/
      ├── data/
      │   ├── processed/              # Preprocessed CSV files
      │   └── raw/
      │       └── sales_data.csv      # CSV file of raw data (500 lines)
      ├── logs/
      │   ├── test_logs/
      │   ├── collect.logs            # Data collection logs
      │   ├── preprocessed.logs       # Data preprocessing logs
      │   └── train.logs              # Model training logs
      ├── model/                      # Storage for trained models
      ├── scripts/
      │   ├── collect.sh              # Data collection script (every 2 minutes)
      │   ├── preprocessed.sh         # Data preprocessing script
      │   ├── train.sh                # Model training script
      │   └── cron.txt                # Cron job configuration file
      ├── src/
      │   ├── preprocessed.py         # Data preprocessing script (Python)
      │   └── train.py                # Model training script (Python)
      ├── tests/
      │   ├── test_collect.py         # Test for data collection and existence of the CSV
      │   ├── test_model.py           # Test for model training and existence of model.pkl
      │   └── test_preprocessed.py    # Test for proper data preprocessing
      ├── Makefile                    # Makefile to automate tasks
      ├── README.md                   # Project documentation
      ├── requirements.txt            # Project dependencies
      ├── pyproject.toml              # Project configuration (dependencies and other settings)
      └── uv.lock                     # Dependency lock file for uv
```
> The version of Python used for this project is Python 3.12

In the project tree, you will find the files **uv.lock** and **pyproject.toml** which are necessary for dependency management that must be configured following the various commands discussed in the course of best practices.

Before starting the exam, make sure to sync with the project and activate your virtual environment.

#### 1. **Data Collection**
The process begins with the collection of graphics card sales data via an API that you will need to query every **3 minutes**. This data is retrieved and stored in a CSV file located in the `data/raw/` folder.

#### 2. **Data Preprocessing**
Once the data is collected, you will need to apply preprocessing. This preprocessing may include:
- Removing missing or incorrect values,
- Converting the data into the appropriate format (for example, date conversion or transforming data types),
- Aggregating or filtering the data if necessary.

The preprocessing results must be saved in a CSV file located in the `data/processed/` folder.

#### 3. **Model Training**
The preprocessed data will be used to train a graphics card sales prediction model. You will likely use an **XGBoost** model for this task. The trained model will be saved in the `model/` folder and will be used for future predictions.

#### 4. **Automation via Cron**
The complete process (data collection, preprocessing, and training) must be executed automatically. You will use **cron** to schedule the tasks to be executed every **3 minutes**. A `cron.txt` file will be provided to configure the cron tasks.

#### 5. **Using a Makefile**
A **Makefile** will be used to facilitate the execution of tasks and automate the entire pipeline with the following command:
```bash
make bash
```
Here is a diagram that briefly summarizes the expected operation of the program when executing this command:

<center><img src="https://assets-datascientest.s3.eu-west-1.amazonaws.com/MLOPS/image.png" style="width:80%"/></center>

#### Files to Modify

You will find in the different files to modify, the instructions corresponding to each task to be completed.

**⚠️ Attention: We will also assess the adherence to best practices in this exam.**

1. **collect.sh**  
   The script `collect.sh` must be modified to automate data collection every 3 minutes.

2. **preprocessed.sh**  
   The script `preprocessed.sh` must be modified to initiate the preprocessing of the collected data.

3. **train.sh**  
   The script `train.sh` must be modified to train the model with the preprocessed data.

4. **cron.txt**  
   You need to configure `cron.txt` to automatically run the collection, preprocessing, and model training every 3 minutes.

5. **preprocessed.py**  
   The script `preprocessed.py` must be modified to perform preprocessing of the collected data (cleaning, data transformation, etc.).

6. **train.py**  
   The script `train.py` must be modified to train the prediction model with the preprocessed data.

7. **Makefile**  
   The `Makefile` must be adjusted to automate the entire process with a single command :  
   ```bash  
   make bash  
   ```  

   The workflow diagram is shown earlier in the README file.
   
8. **requirements.txt**  
   The **requirements.txt** file should only include the libraries necessary for the execution of the program.

<br>

### Tests and Verifications

**⚠️ You must not modify the provided test files. These will validate the compliance of your work.**

- **Data Collection Test** (`test_collect.py`)
- **Model Training Test** (`test_model.py`)
- **Data Preprocessing Test** (`test_preprocessed.py`)

To run the tests, you can use the following command:
```bash
make tests
```

This will create files test_*.logs in logs/tests_logs.

Example of log output generated by your functional automation program:

**test_collect.logs** : 
```txt
=== Start of tests (2025-04-30 15:21:03) ===
Start of CSV structure test
CSV file loaded with 520 lines and 3 columns
Test successful: The CSV is valid.
End of CSV structure test
=== End of tests ===
```

**test_preprocessed.logs** : 
```txt
=== Start of tests (2025-04-30 15:21:19) ===
Start of the preprocessed file structure test
File loaded: data/processed/sales_processed_20250430_1516.csv
Checking column 'timestamp': OK (not present)
Checking integer types: OK (all columns are integers)
Test completed for the preprocessed file.
=== End of tests ===
```

**test_model.logs** : 
```txt
=== Start of tests (2025-04-30 15:21:23) ===
Start of model file presence test
Test successful: the model file exists.
=== End of tests (2025-04-30 15:21:23) ===
```

Once the entire program is executed (collection, preprocessing, training), here is what you should observe:

**data/raw** :
- CSV files containing the **raw sales data** automatically retrieved from the API.
- These files follow a naming convention of the type: `sales_YYYYMMDD_HHMM.csv`.

**data/processed/** :
- CSV files containing the **preprocessed data**, ready to be used for model training.
- These files follow a naming convention of the type: `sales_processed_YYYYMMDD_HHMM.csv`.

**model/** :
- One or more versions of the **trained model**, saved as a `.pkl` file.
- Example: `model.pkl` or `model_YYYYMMDD_HHMM.pkl`.

## Final Render

**⚠️ Please do not include the `venv` folder in the project archive, as this will make the file considerably heavier.**
   
> Create an archive exam_NAME.tar

```bash
# Create a tar archive named exam_NAME.tar from the directory exam_NAME

# Command:
tar -cvf exam_NAME.tar exam_NAME
```

### SCP Command

The `scp` command allows for the secure transfer of a file or an archive (folders cannot be transferred) via an SSH connection.

You can download your archive by running the following command `on a terminal of your own machine`.

```shell
scp -i "data_enginering_machine.pem" ubuntu@VOTRE_IP:~/exam_NAME.tar .
```

<div class="alert alert-info"> <i class="icon circle info"></i>
Several details regarding the above order:
  <br>
  </br>
  - When you open your terminal on your local computer to transfer your archive from the VM, specify the absolute path to your file data_enginering_machine.pem
  <br>
  </br>
  - Your archive will be downloaded in the same folder where your file data_enginering_machine.pem is located
</div>

Once you have downloaded your archive to your local machine, you can upload it via the `My Exams` tab.

Good luck!
