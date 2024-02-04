import json
from flask import Flask, request, jsonify
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
#from flask_bcrypt import Bycrpt

DB_FILE = "clubreview.db"

cache_config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_FILE}"
#app.config['SECRET_KEY'] = 'cocomelon'
app.config.from_mapping(cache_config)
db = SQLAlchemy(app)
cache = Cache(app)
#bcrypt = Bcrypt(app)

from models import *

@app.route("/")
def main():
    return "Welcome to Penn Club Review!"


@app.route("/api")
def api():
    return jsonify({"message": "Welcome to the Penn Club Review API!."})

@app.route("/api/clubs", methods=["GET"])
@cache.cached(timeout=30)
def getClubs():
    clubs = Club.query.all()
    final_resultset = []

    for club in clubs:
        tagArr = []
        result = {}
        result["code"] = club.code
        result["name"] = club.name
        result["description"] = club.description
        result["likes"] = club.likes

        for tag in club.tags:
            tagArr.append(tag.name)
            result["tags"] = tagArr

        final_resultset.append(result)

    return jsonify(final_resultset)


@app.route("/api/<user_id>")
@cache.cached(timeout=15)
def get(user_id):
    user = User.query.filter_by(id=user_id).first()
    result = {}
    result["id"] = user.id
    result["name"] = user.name
    result["email"] = user.email

    return jsonify(result)

@app.route("/api/search/<search>", methods=["GET"])
@cache.cached(timeout=15)
def getSearch(search):
    clubs = Club.query.all()
    final_resultset = []

    for club in clubs:
        tagArr = []
        result = {}
        if ((club.name.lower()).find(search.lower()) != -1):
            result["code"] = club.code
            result["name"] = club.name
            result["description"] = club.description
            result["likes"] = club.likes

            for tag in club.tags:
                tagArr.append(tag.name)
                result["tags"] = tagArr

            final_resultset.append(result)

    return jsonify(final_resultset)

@app.route("/api/create_club", methods=["POST"])
def create_club():
    data = request.get_json()

    code = data['code']
    name = data['name']
    description = data['description']
    tags = data['tags']

    newClub = Club(code=code, name=name, description=description, likes=0)

    for tag in tags:
        q = Tag.query.filter(Tag.name==tag)
        if db.session.query(q.exists()).scalar():
            t = Tag.query.filter_by(name=tag).first()
            newClub.tags.append(t)
        else:
            newTag = Tag(name=tag)
            newClub.tags.append(newTag)
            db.session.add(newTag)   

    db.session.add(newClub)
    db.session.commit()
    return jsonify(data)

@app.route("/api/favorite/<club_code>")
def favorite(club_code):
    club = Club.query.filter_by(code=club_code).first()
    club.likes += 1
    db.session.commit()
    result = {}

    tagArr = []
    result["code"] = club.code
    result["name"] = club.name
    result["description"] = club.description
    result["likes"] = club.likes

    for tag in club.tags:
        tagArr.append(tag.name)
        result["tags"] = tagArr

    return jsonify(result)

@app.route("/api/tags")
@cache.cached(timeout=15)
def getTags():
    tags = Tag.query.all()
    club_list = []
    final_resultset = []
    clubCount = 0

    for tag in tags:
        club_list = []
        result = {}
        clubCount = 0
        clubs = tag.clubs
    
        for club in clubs:
            clubCount+= 1
            club_list.append(club.name)
        
        result["count"] = clubCount
        result["clubs"] = club_list
        result["name"] = tag.name
        final_resultset.append(result)

    return jsonify(final_resultset)

@app.route("/api/modify_club/<club_code>", methods=["POST"])
def modify_club(club_code):
    data = request.get_json()
    name = data['name']
    description = data['description']
    tags_to_add = data['tags_to_add']
    tags_to_delete = data['tags_to_delete']

    club = Club.query.filter_by(code=club_code).first()
    
    if (description != 'N/A'):
          club.description = description
    if (name != 'N/A'):
        club.name = name
  
    if (tags_to_add != 'N/A'):
        for tag in tags_to_add:
            q = Tag.query.filter(Tag.name==tag)
            t = Tag.query.filter_by(name=tag).first()
            if t not in club.tags:
                if db.session.query(q.exists()).scalar():
                    club.tags.append(t)
                else:
                    newTag = Tag(name=tag)
                    club.tags.append(newTag)
                    db.session.add(newTag) 
    if (tags_to_delete != 'N/A'):
        for tag in tags_to_delete:
            t = Tag.query.filter_by(name=tag).first()
            if (t in club.tags):
                club.tags.remove(t)

    db.session.commit()
    return jsonify(data)

    #UNFINISHED CODE FOR USER AUTHENTICATION
    """
    @app.route("/login", methods=['GET', 'POST'])
    def login():
        data = request.get_json()
        result = {}

        givenUsername = data['username']
        givenPassword = data['password']

        user = User.query.filter_by(username=givenUsername).first()
        if user:
            if bcrypt.check_password_hash(user.password, givenPassword):
                login_user(user)

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        data = request.get_json()
        result = {}

        username = data['username']
        password = data['password']

        existing_user_username = User.query.filter_by(username=username.data).first()

        if not existing_user_username:
            hashed_password = bcrypt.generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
    """

if __name__ == "__main__":
    app.run(debug=True, port="9090")
