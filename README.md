
# Command-line App for Data Processing

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Features](#features)
- [Usage](#usage)
- [Test](#test)


## Introduction

This Python command line application is designed to handle various data processing tasks, including data input, cleaning
, transformation, and export. The primary purpose of this application is to provide users with a versatile tool to 
efficiently process data from different sources and output it to a specified location. 

## Getting Started

### Prerequisites

To use this application, you need the following:

- Python 3: You can download and install Python 3.10.11.
- If you are using AWS S3, your credentials should be configured. Follow the guide below if you have not done so.

### Installation

#### 1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```
   
#### 2. Set up your AWS credentials:

**On Linux/macOS:**

1. Open your terminal.

2. Edit your shell configuration file (e.g., `~/.bashrc`, `~/.bash_profile`, or `~/.zshrc`) using a text editor. For example:

   ```bash
   nano ~/.bashrc
   ```

3. Add the following lines to set the AWS Access Key and Secret Access Key:

   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   ```

   Replace `your_access_key` and `your_secret_key` with your actual AWS credentials.

4. Save the file and exit the text editor.

5. Source the configuration file to apply the changes:

   ```bash
   source ~/.bashrc
   ```

**On Windows:**

1. Open the "Environment Variables" settings:

   - In Windows 10/11, search for "Environment Variables" in the Start menu.

   - In older versions of Windows, go to "Control Panel" > "System and Security" > "System" > "Advanced system settings" > "Environment Variables."

2. Under "User variables," click "New" to add two variables:

   - Variable name: `AWS_ACCESS_KEY_ID`

   - Variable value: your AWS Access Key

   - Variable name: `AWS_SECRET_ACCESS_KEY`

   - Variable value: your AWS Secret Access Key

3. Click "OK" to save the variables.

Note: Depending on your system, you may need to **restart your computer** for the changes to take effect.

## Features

- **Data Input:** The application can read data from various sources, including compressed files in .gz, .bz2, .xz, and API JSON endpoints.

- **Data Flattening:** For API JSON data, the application can flatten results if there are nested elements in the JSON attributes.

- **Data Cleaning:** You can use the application to clean the data by removing missing values (NA) and dropping duplicate entries.

- **Data Export:** The application supports data export in multiple formats, including .csv and .parquet. Note that .xlsx export is not recommended for large datasets.

- **Compression:** You can choose to output the data in compressed formats such as .gz, .bz2, and .xz.

- **S3 Integration:** Files can be exported to a local directory or a public S3 bucket.

## Usage

### Running the command-line application
   ```bash
   python main.py
   ```
---

### 1. Please Respond with 'Yes' or 'No'

For each prompt in this application, you can provide your response in the following ways:
- `yes` or `no`
- `y` or `n`

The input is not case-sensitive, so feel free to use lowercase or uppercase letters.

### 2. Extra Spaces

You don't need to worry about extra spaces in your responses. The application will process your input correctly regardless of leading or trailing spaces.

### 4.Providing paths
When prompted for path, **do not** use quotations. Instead, just input the absolute path.
```
  /path/to/file
```

### 5. Providing API endpoints
When prompted for API endpoint, you may test with
```
    http://makeup-api.herokuapp.com/api/v1/products.json?brand=maybelline
```

### 6. Providing Bucket Name
When prompted, please input the name of your public S3 Bucket.
```
    myawsbucket-example
```
If you encounter any errors, check that your S3 bucket policies have been configured as such
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AddPerm",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::myawsbucket-example/*"
        }
    ]
}
```
Note: It is advisable to verify that the region configuration of your AWS credentials matches the region of your intended S3 Bucket. This alignment in region settings will help ensure a seamless interaction with your S3 resources.

## Test
To ensure that your command line application works as expected, you can run the provided tests from `test.py`.
Some test cases may take a while to complete.

Before running the tests, ensure that the following files are present in `example_data` directory:
1. `title.basics.tsv.gz`
2. `data.tsv`

The first file can be obtained from [here](https://datasets.imdbws.com/title.basics.tsv.gz). The second file is obtained from extracting the first file.