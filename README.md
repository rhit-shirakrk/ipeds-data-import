
# Installation/Dependencies

Ensure you are on Python 3.13.

Run `pip install -r requirements.txt` to install all dependencies. Ensure you are
using a virtual environment such as `venv`

This pipeline assumes you are running on Windows and have the Microsoft Access
Driver (*.mdb,*.accdb) installed. To check for this, please follow the steps
described in [pyodbc's documentation](https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-Microsoft-Access).

- Unless you're willing to jump through many hoops, because Microsoft Access DB
files are (basically) proprietary to Windows, there is no support for running
on MacOS or Linux

# Usage

Because this pipeline converts Micrsoft Access DB data to MySQL data, this pipeline
can only be run on Windows. This is because certain ODBC drivers pertinent to
Microsoft Access DB are required to access the data in the file. While there are
some alternatives, I believed it would be easiest to make this pipeline be run
on Windows, especially since Microsoft Access DB files are primarily used on Windows.

Besides the environment, this pipeline requires two inputs:

- A credentials file (.ini) for your MySQL database. See below for the expected
format
- A Windows path to a Mirosoft Access DB file. While it would be possible to
instead have the user supply a URL that links to the [IPEDS data](https://nces.ed.gov/ipeds/use-the-data/download-access-database),
due to client concerns that the website may be taken down in the near future, I
felt it made more sense to have the file on hand.

To run the script, call `python -c WINDOWS_PATH_TO_CREDS_FILE -a WINDOWS_PATH_TO_ACCESS_DB_FILE`

## Credentials File Format

```python
[ipeds_db]
user = "USERNAME_HERE"
password = "PASSWORD_HERE"
hostname = "HOSTNAME_HERE"
port = "PORT_HERE"
database = "DATABASE_NAME_HERE"
table_name = "TABLE_NAME_HERE"
```

# Expandability

I also made a [data archive](https://github.com/rhit-shirakrk/ipeds-data-archive) of all publicly-available IPEDS files, so
if one wanted to run this pipeline on all of the files, it would require
relatively small changes. However, because the Gender Fair 2024-2025 team only
chose to analyze data from one year, I felt this was a simpler implementation.
