
#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request ,redirect, url_for

import logging
from logging import Formatter, FileHandler
from forms import *
import os
from flask_dance.contrib.github import make_github_blueprint, github
import json
from github import Github
import requests
from pprint import pprint
import subprocess
import shutil
import pygit2

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')





#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return redirect(url_for('search'))


@app.route('/search',methods=['GET', 'POST'])
def search():
        if request.method == "POST": 
                form = SearchForm(request.form)          
                username = request.form.get('username') 
                
                url = 'https://api.github.com/users/{}/repos'.format(username)                
                repos = requests.get(url).json()   
                return  render_template('pages/placeholder.forky.html',repos=repos)
            
        if request.method == "GET":
                form = SearchForm(request.form)
                return  render_template('pages/placeholder.forky.html')   
            #'<h1>Your Github name is {}'.format(account_info_json['login'])

        return '<h1>Request failed!</h1>'

@app.route('/clone',methods=['GET','POST'])
def clone(): 
    if request.method == 'POST': 
       url = request.form.get('url')
       reponame = request.form.get('reponame')
       username = request.form.get('username')
       password = request.form.get('password')
       email = request.form.get('email')
       name = request.form.get('name')
       
       CloneRepo(username,password,reponame,url,name,email,"first commit")
       return redirect('https://github.com/{}/{}'.format(username,reponame))
   
    if request.method == 'GET': 
        form = CloneForm(request.form) 
        url = request.args.get('url')
        reponame  = request.args.get('name')       
        return render_template('pages/placeholder.results.html',form = form, url = url, reponame= reponame)
   


def CloneRepo(username,password,repo_name,repo_clone_url,signature_name,signature_email, first_commit_msg):    
        g = Github(username, password)
        user = g.get_user()
        repo = user.create_repo(repo_name)
        
        if os.path.exists(os.getcwd()+'/tmp/'):           
            shutil.rmtree(os.getcwd()+'/tmp/')        
        file_path = os.path.abspath(os.getcwd()+'/tmp')

        
        #Clone it 
        repoClone = pygit2.clone_repository(repo_clone_url, file_path)
   
        #Commit it
        repoClone.remotes.set_url("origin", repo.clone_url)
        index = repoClone.index
        index.add_all()
        index.write()
        author = pygit2.Signature(signature_name, signature_email)
        commiter = pygit2.Signature(signature_name, signature_email)
        tree = index.write_tree()
        oid = repoClone.create_commit('refs/heads/master', author, commiter, first_commit_msg,tree,[repoClone.head.target])
        remote = repoClone.remotes["origin"]
        credentials = pygit2.UserPass(username, password)
        remote.credentials = credentials

        callbacks=pygit2.RemoteCallbacks(credentials=credentials)

        remote.push(['refs/heads/master'],callbacks=callbacks)

        if os.path.exists(os.getcwd()+'/tmp/'):           
            shutil.rmtree(os.getcwd()+'/tmp/')        


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()