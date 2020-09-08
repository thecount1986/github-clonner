from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length

# Set your classes here.


class CloneForm(Form):
   name = TextField('Github', [DataRequired()])
   password = PasswordField('Password', [DataRequired()])
   reponame =  TextField('Name your cloned repo', [DataRequired()])
   url =  TextField('Clone repo url', [DataRequired()])

class SearchForm(Form):
    search = TextField('Search term', [DataRequired()])
