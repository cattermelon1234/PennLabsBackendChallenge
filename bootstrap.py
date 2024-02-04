import json
import os
from app import app, db, DB_FILE

from models import *

def create_user():
    user = User(id='josh150', name='Josh', email='josh150@seas.upenn.edu')
    db.session.add(user)
    db.session.commit()

def load_data():
    f = open('clubs.json')
    data = json.load(f)
    for club in data:
        newClub = Club(code=club['code'], name=club['name'], description=club['description'], likes=0)
        for tag in club['tags']:
            q = db.session.query(Tag).filter(Tag.name==tag)
            if db.session.query(q.exists()).scalar():
                t = Tag.query.filter_by(name=tag).first()
                newClub.tags.append(t)
            else:
                newTag = Tag(name=tag)
                newClub.tags.append(newTag)
                db.session.add(newTag)    
        db.session.add(newClub)
    
    db.session.commit()
    f.close()

# No need to modify the below code.
if __name__ == "__main__":
    # Delete any existing database before bootstrapping a new one.
    LOCAL_DB_FILE = "instance/" + DB_FILE
    if os.path.exists(LOCAL_DB_FILE):
        os.remove(LOCAL_DB_FILE)

    with app.app_context():
        db.create_all()
        create_user()
        load_data()
