import os
from flask_admin import Admin
<<<<<<< HEAD
from models import db, User,Planets,People
=======
from models import db, User,Todo
>>>>>>> 2027cc7631155cad1eb81301ac4224d01b944311
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
<<<<<<< HEAD
    admin.add_view(ModelView(Planets, db.session))
    admin.add_view(ModelView(People, db.session))
=======
    admin.add_view(ModelView(Todo, db.session))
>>>>>>> 2027cc7631155cad1eb81301ac4224d01b944311

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))