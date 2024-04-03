# Project World population application


## <span style='color:red'>Description</span>
The project is for the extraction of data from various sources, storing it in a database, and printing it to the screen. This project consists of two Docker containers: one for parsing data and storing it in a database, and another for retrieving the data from the database and printing it to the screen.

Parsing data from different sources such as websites, APIs.
## <span style='color:red'>Configuration</span>

### <span style='color:yellow'>Choise of source</span>
```bash
# In the `.env` file, add environment variables to select the SOURCE:

# Parsers configuration
...
SOURCE="wikipedia"
# SOURCE="statisticstimes"
# SOURCE="geonames"
...

- Comment out the variable for choosing a source.
- ! Only one source can be choosen in one moment.

```
### Run application

```bash
# To start the containers, run:

# first container extraction and storing of data in database
...
docker compose up get_data
...
# second container retrieving the data from the database and printing it to the screen.
...
docker compose up print_data
...
```
### <span style='color:yellow'>Adding a New Source</span>
```bash
If you want to add a new source, create a parser`s class with your parser in the `src/countries/parsers` file and add name of class, url to the file `settings` and variables for parser to the `.env` file.

example:

`.env`
SOURCE="wikipedia"

`settings.py`
PARSERS_MAPPING = {
    ...
    "wikipedia": [
        "ParserWiki",
        "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population",
    ...
    ],
In the file get_data.py in import add paasrer`s class

from countries.parsers import ParserWiki..., "NewParserClass"
```
### Database
```bash
- The project utilizes a {PostgreSQL} database;
- Database is automatically initialized and spun up along with the Docker containers;
- No additional setup is required.
```
### async
```bash
To scale the project, the code is executed asynchronously
```

## Development environment
### <span style='color:yellow'>Instal Deps</span>
```bash
# install pipenv
pip install pipenv

# activate virtual env
pipenv shell

# install deps
pipenv sync --dev
```
## Usage code quality tools
```bash
# The pre-commit hook will be automatically run
- flake8, black, isort
```

