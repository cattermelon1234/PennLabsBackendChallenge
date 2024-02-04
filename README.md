# Penn Labs Backend Challenge

## Installation

1. Click the green "use this template" button to make your own copy of this repository, and clone it. Make sure to create a **private repository**.
2. Change directory into the cloned repository.
3. Install `pipx`
   - `brew install pipx` (macOS)
   - See instructions here https://github.com/pypa/pipx for other operating systems
4. Install `poetry`
   - `pipx install poetry`
5. Install packages using `poetry install`.
6. Install flask using `pip install flask`
7. Install flask_sqlalchemy using `pip install flask_sqlalchemy`
8. Install flask_caching using `pip install flask_caching`

### Loading Data into Database
run `poetry run python bootstrap.py` to populate the database. You should only need to do this once. 

## Design Documentation

### API (app.py)
| URL Route                | HTTP Method | Parameters | Usage                                                                     |
| ------------------------ | ----------- | ---------- | --------------------------------------------------------------------      |
| `/`                      | `GET`       | `N/A`      | Returns a welcome message: 'Welcome to Penn Club Review!'                 |
| `/api`                   | `GET`       | `N/A`      | Returns a jsonified message welcoming to the Club Review api              | 
| `/api/clubs`             | `GET`       | `N/A`      | Returns a jsonified list of all clubs and all their attributes            |
| `/api/<user_id>`         | `GET`       | `<user_id>`| Returns a json of the attributes of the user in question (searched by id) |    
| `/api/search/<search>`   | `GET`       | `<search>` | Returns a jsonified list of all clubs containing search string in its name |
| `/api/create_club/`      | `POST`      | `code`: club code, <br> `name`: club name, <br>`description`: summary of the club, <br>`tags`: array of tag strings describing the club | Creates a new club and commits it to the database with all the given specifications (must be in json format)
| `/api/favorite/<club_code>` | `POST`     | `<club_code>`: the code of an existing club | Adds a like to the specified club in `club_code` | 



### Models (models.py)



## File Structure

- `app.py`: Main file. Has configuration and setup at the top. Add your [URL routes](https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing) to this file!
- `models.py`: Model definitions for SQLAlchemy database models. Check out documentation on [declaring models](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/) as well as the [SQLAlchemy quickstart](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#quickstart) for guidance
- `bootstrap.py`: Code for creating and populating your local database. You will be adding code in this file to load the provided `clubs.json` file into a database.

## Developing

0. Determine how to model the data contained within `clubs.json` and then complete `bootstrap.py`
1. Activate the Poetry shell with `poetry shell`.
2. Run `python3 bootstrap.py` to create the database and populate it.
3. Use `flask run` to run the project.
4. Follow the instructions [here](https://www.notion.so/pennlabs/Backend-Challenge-862656cb8b7048db95aaa4e2935b77e5).
5. Document your work in this `README.md` file.

## Submitting

Follow the instructions on the Technical Challenge page for submission.

## Installing Additional Packages

Use any tools you think are relevant to the challenge! To install additional packages
run `poetry add <package_name>` within the directory. Make sure to document your additions.
