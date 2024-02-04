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
| URL Route                | HTTP Method | Parameters         | Usage                                                                     |
| ------------------------ | ----------- | ----------    | --------------------------------------------------------------------      |
| `/`                      | `GET`       | `N/A`         | Returns a welcome message: 'Welcome to Penn Club Review!'                 |
| `/api`                   | `GET`       | `N/A`         | Returns a jsonified message welcoming to the Club Review api              | 
| `/api/clubs`             | `GET`       | `N/A`         | Returns a jsonified list of all clubs and all their attributes            |
| `/api/<user_id>`         | `GET`       | `<user_id>`  | Returns a json of the attributes of the user in question (searched by id) |    
| `/api/search/<search>`   | `GET`       | `<search>`    | Returns a jsonified list of all clubs containing search string in its name |
| `/api/tags`              | `GET`       | `N/A`         | Returns a jsonified list of all tags and their attributes, including which clubs they are attached to |
| `/api/create_club/`      | `POST`      | `code`, `name` <br>`description`, `tags` | Creates a new club and commits it to the database with all the given specifications (must be in json format)
| `/api/favorite/<club_code>` | `POST`     | `<club_code>` | Adds a like to the specified club in `club_code` | 
| `/api/modify_club/<club_code>` | `POST`  | `code`, `name`, `description` <br> `tags_to_add`, `tags_to_delete` | Modifies each parameter changed by the request (in json format), changes nothing if the string "N/A" is passed into the field| 



### Models (models.py)
My database contained 3 classes and 1 association table. 

1. User Class (a database representing registered users)
   * id: a unique String id of the user comprised of their name and a number (ex: josh150) (NOT MUTABLE)
   * name: the name of the user (String), the maximum length is 80
   * email: the email of the user (String), the maximum length is 120

3. Club Class (a database representing registered clubs)
   * code: a unique String code assigned to every club upon creation (NOT MUTABLE)
   * name: the assigned name of the club, the maximum length is 50
   * description: a short blurb describing the club to potential newcomers, the maximum length is 500
   * likes: an integer representing the amount of likes a club has received
   * tags: relationship with the "Tag" class, refers to the secondary database "Club_Categories"
     
4. Tag Class (a database representing registered tags)
   * id: a unique id of each created tag, autoincremented by row
   * name:
   * clubs: relationship with the "Club" class, refers to the secondary database "Club_Categories"
   
6. Club_Categories Table (a table relating clubs to their assigned tags, and vice versa)
   * id: a unique id of each relationship entry in the table, autoincremented by row
   * club_code: Foreign Key linking a Tag to the specified club the tag is assigned to
   * tag_id: Foreign Key linking a Club to the tags assigned to it

## Testing

### POST REQUESTS
#### OPTION 1: Using Curl to create POST requests

Example Request 1 (create_club)
```
curl --location 'http://127.0.0.1:5000/api/create_club' \
--header 'Content-Type: application/json \
--data
{
   "code": "abcd",
   "name": "Penn Alphabet Club",
   "description": "This is a club for alphabet enjoyers at Penn!",
   "tags": ["Literary", "Undergraduate"]
}
```
Example Request 2 (modify_club)
```
curl --location 'http://127.0.0.1:5000/api/modify_club/abcd' \
--header 'Content-Type: application/json \
--data
{
   "name": "Penn ABC Song Club",
   "description": "This is a club for people who love to sing the alphabet at Penn!",
   "tags_to_add": ["Singing"],
   "tags_to_remove": "N/A"
}
```
One possible method to test out Curl requests is through making curl requests once the server is active. 

#### OPTION 2: Using POSTMAN to create POST requests
1. Open `https://www.postman.com/` and click `My workspace` and the `+` button near the tabs
2. Paste in the desired api route (ex: `http://127.0.0.1:5000/api/modify_club/abcd'`) and make sure to toggle to `POST`
3. Under the bar where you entered the URL, you should see a lot of options. Click `Body` then `raw`, which should prompt you with an empty text box
4. Enter in the desired post request content in json form in the text box, following the examples above

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
