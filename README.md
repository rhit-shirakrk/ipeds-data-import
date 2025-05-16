
# Installation/Dependencies

Ensure you are on Windows and using Python 3.10 or greater.

Run `pip install -r requirements.txt` to install all dependencies. Ensure you are
using a virtual environment such as `venv`

This pipeline assumes you are running on Windows and have the Microsoft Access
Driver (*.mdb,*.accdb) installed. To check for this, please follow the steps
described in [pyodbc's documentation](https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-Microsoft-Access).

- Unless you're willing to jump through many hoops, because Microsoft Access DB
files are (basically) proprietary to Windows, there is no support for running
this pipeline on MacOS or Linux

# Usage

This pipeline requires two inputs:

- A credentials file (.ini) for your MySQL database. See below for the expected
format
- A Windows path to a Mirosoft Access DB file. While it would be possible to
instead have the user supply a URL that links to the [IPEDS data](https://nces.ed.gov/ipeds/use-the-data/download-access-database),
due to client concerns that the website may be taken down in the near future, I
felt it made more sense to have the file on hand.

Logs are written to a file named `app.log`, which documents all successful table
creation/data imports. Adjustments to variable-size data types are also documented.
For example, when a column is identified as `VARCHAR`, the logs will explicitly
indicate what size it was set to (ex. `VARCHAR(255)`). This also applies to
`DECIMAL` (ex. `DECIMAL(20, 2)`, `DECIMAL(10, 0)`, etc.). Such values are based
on certain fields found in the Microsoft Access DB table schemas.

- Field size for text data types
- Precision/Scale for `DECIMAL`

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

# Other

Python may give a warning similar to something below:

`UserWarning: pandas only supports SQLAlchemy connectable (engine/connection) or database string URI or sqlite3 DBAPI2 connection. Other DBAPI2 objects are not tested. Please consider using SQLAlchemy.`

However, as of now, this is not a concern as other DBAPI connections do work.
There are existing solutions to this problem, but I chose to use pyodbc for it's
convenient API.

- <https://stackoverflow.com/a/71083448>
