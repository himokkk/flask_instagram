from flask import Flask, request, render_template, url_for, redirect, session, jsonify, g, send_from_directory, make_response
from sqlalchemy import create_engine, Column, Integer, String, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from PIL import Image
import datetime, time
import copy
import re
import os
from email_validator import validate_email, EmailNotValidError
xd
app = Flask(__name__)

db = declarative_base()
app.config["FOLDER"] = 'D:\Programowanie\Instagram'
app.config["UPLOAD_FOLDER"] = app.config["FOLDER"]+"/static//images"
app.config["EDITED_FOLDER"] = app.config["FOLDER"]+"/static//edited_images"
app.config["PROFILE_IMAGES"] = app.config["FOLDER"]+"/static//profile_images"
app.secret_key = os.urandom(50)

class User(db):
    __tablename__ = "user"
    id = Column('id', Integer, primary_key=True)
    email = Column('email', String, unique=True)
    name = Column('name', String)
    username = Column('username', String, unique=True)
    password = Column('password', String)
    image = Column('image', String, default="default.jpg")
    description = Column('description', String, default="")
    followed = Column('followed', ARRAY(Integer), default=[])
    followed_count = Column('followed_count', Integer, default=0)
    followed_by = Column('followed_by', ARRAY(Integer), default=[])
    followed_by_count = Column('followed_by_count', Integer, default=0)
    posts = Column('posts', ARRAY(Integer), default=[])
    posts_count = Column('posts_count', Integer, default=0)
    saved = Column('saved', ARRAY(Integer), default=[])

class Post(db):
    __tablename__ = "post"
    id = Column('id', Integer, primary_key=True)
    str_id = Column('str_id', String)
    author_id = Column('author_id', Integer)
    description = Column('description', String)
    likes = Column('likes', ARRAY(Integer), default=[])
    likes_counter = Column('likes_counter', Integer, default=0)
    date = Column('date', String)
    comments = Column('comments', ARRAY(String), default=[])

polish = {'lang':'pl','username': 'Nazwa użytkownika', 'password': 'Hasło', 'login': 'Zaloguj się', 'forgot': 'Nie pamiętasz hasła?', 'noacc': 'Nie masz konta?', 'register': 'Zarejestruj się', 'name': 'Imię i nazwisko', 'haveacc': 'Masz konto?', 'likedby': 'Liczba polubień:', 'addcom': 'Dodaj komentarz', 'post': 'Dodaj', 'search': 'Szukaj', 'profile': 'Profil', 'saved': 'Zapisane', 'settings': 'Ustawienia', 'switch': 'Zmień konto', 'logout': 'Wyloguj się', 'follow': 'Obserwuj', 'posts': 'Posty:', 'followers': 'Liczba obserwujących:', 'followed': 'Liczba obserwowanych:', 'newpost': 'Nowy post'}
english = {'lang':'en','username': 'Username', 'password': 'Password', 'login': 'Log in', 'forgot': 'Forgot password?', 'noacc': "Dont't have an account?", 'register': 'Sign in', 'name': 'Name and surname', 'haveacc': 'Have an account?', 'likedby': 'Likes count:', 'addcom': 'Add comment', 'post': 'Add', 'search': 'Search', 'profile': 'Profile', 'saved': 'Saved', 'settings': 'Settings', 'switch': 'Switch an account', 'logout': 'Log out', 'follow': 'Follow', 'posts': 'Posts:', 'followers': 'Followers count:', 'followed': 'Followed count:', 'newpost': 'New Post'}

#engine = create_engine('postgresql://ynaenxxh:Z4z7Q9m1B7oA6YuCDGeTNwFM99N7DMlZ@chunee.db.elephantsql.com/ynaenxxh')
engine = create_engine('postgresql://postgres:1234@localhost/postgres')
db.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session1 = Session()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.before_request
def before_request():
    global lang_dict
    if request.cookies.get('language')!=None:
        lan=request.cookies.get('language')
        lang_dict = english
        if lan=='en':
            lang_dict=english
        elif lan=='pl':
            lang_dict=polish
    g.user = None
    if 'user' in session:
        users = session1.query(User).all()
        user = [x for x in users if x.id == session['user']][0]
        g.user = user
    global logged
    logged=False
    if g.user:
        logged=True


coms=[]
@app.route('/')
def home():
    if g.user:
        posts = session1.query(Post).all()
        users = session1.query(User).all()
        posts_temp = copy.copy(posts)
        posts_temp = sorted(posts_temp, key=lambda x: x.id)
        if request.args.get('like') != None:
            for post in posts:
                if post.id==int(request.args.get('like')):
                    temp = False
                    for like in post.likes:
                        if g.user.id==like:
                            temp = True
                    if temp:
                        temp = copy.copy(post.likes)
                        temp.remove(g.user.id)
                        post.likes = temp
                    elif not temp:
                        temp = copy.copy(post.likes)
                        temp.append(g.user.id)
                        post.likes = temp
                    post.likes_counter = len(temp)
                    session1.commit()
        if request.args.get('like_dbl') != None:
            for post in posts:
                if post.id==int(request.args.get('like_dbl')):
                    temp = False
                    for like in post.likes:
                        if g.user.id==like:
                            temp = True
                    if not temp:
                        temp = copy.copy(post.likes)
                        temp.append(g.user.id)
                        post.likes = temp
                        post.likes_counter = len(temp)
                    session1.commit()
        if request.args.get('jsdata')!=None:
            id, comment = request.args.get('jsdata').split(' ', 1)
            comment=comment.replace('<','')
            d = time.time()
            for_js = str(int(d))
            string="<div class='com'><div style='float:left;'><a class='underline' style='float:left;' href='/user/"+g.user.username+"'><b>"+g.user.username+"</b></a><div class='select comment_content' style='float:left;'> "+comment +" "+" </div></div><div class='date' onload='date1()'> "+ for_js+"</div></div>"
            for post in posts:
                if int(post.id)==int(id):
                    copy1 = copy.copy(post.comments)
                    copy1.append(string)
                    post.comments=copy1
                    session1.commit()
        return render_template('home.html', lang=lang_dict,posts=posts_temp, users1=users,username=g.user.username, id=g.user.id, logged=logged)
    else:
        return redirect('/login')

@app.route('/user/<username>')
def profile(username):
    owner = False
    posts = session1.query(Post).all()
    users = session1.query(User).all()
    user1=users[0]
    if request.args.get('id') != None:
        id = int(request.args.get('id'))
        for user in users:
            if user.id == id:
                following = False
                for follower in user.followed_by:
                    if follower == id:
                        following = True
                temp = copy.copy(user.followed_by)
                temp1 = copy.copy(g.user.followed)
                if following:
                    temp.remove(id)
                    temp1.remove(id)
                else:
                    temp.append(id)
                    temp1.append(id)
                user.followed_by_count = len(temp)
                user.followed_by = temp
                g.user.followed = temp1
                g.user.followed_count = len(temp1)
                session1.commit()
    for user in users:
        if user.username==username:
            user1=user
    if g.user:
        if username==g.user.username:
            owner=True
    user1.posts = user1.posts[::-1]
    if request.method == 'GET':
        if g.user:
            followed=False
            for following in g.user.followed:
                if following==user1.id:
                    followed=True
            return render_template('profile.html', lang=lang_dict, posts=posts, users1=users, user=user1, followed=followed,username=g.user.username, id=g.user.id, owner=owner, logged=logged)
        else:
            return render_template('profile.html', lang=lang_dict, posts=posts, users1=users, user=user1, owner=owner, logged=logged)

@app.route('/signup', methods=['GET','POST'])
def signup():
    if g.user:
        return redirect('/')
    if request.method == 'POST':
        can_add = True
        users = session1.query(User).all()
        user = User()
        email = request.form['email']
        lang = request.cookies.get('language')
        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError:
            if lang=='en':
                message='Email not correct.'
            if lang=='pl':
                message='Niepoprawny email.'
            return render_template('signup.html', lang=lang_dict, message=message)
        user.email = email
        user.name = request.form['name']
        user.username = request.form['username']
        user.password = request.form['password']
        for user1 in users:
            if user1.email==user.email:
                if lang == 'en':
                    message = 'This email is taken.'
                if lang == 'pl':
                    message = 'Ten email jest zajęty.'
                return render_template('signup.html', lang=lang_dict, message=message)
            if user1.username == user.username:
                if lang == 'en':
                    message = 'This username is taken.'
                if lang == 'pl':
                    message = 'Ta nazwa użytkownika jest zajęta.'
                return render_template('signup.html', lang=lang_dict, message=message)
        if len(user.username)<5:
            if lang == 'en':
                message = 'Username not correct.'
            if lang == 'pl':
                message = 'Niepoprawna nazwa użytkownika.'
            can_add = False
        if len(user.password)<8:
            if lang == 'en':
                message = 'Name not correct.'
            if lang == 'pl':
                message = 'Niepoprawne imię.'
            can_add = False
        if len(user.name)<3:
            if lang == 'en':
                message = 'Name not correct.'
            if lang == 'pl':
                message = 'Niepoprawne imię.'
            can_add = False
        if bool(re.search(r'\d', user.name)):
            if lang == 'en':
                message = 'Name not correct.'
            if lang == 'pl':
                message = 'Niepoprawne imię.'
            can_add = False
        if can_add:
            session1.add(user)
            session1.commit()
            return redirect('/login')
        return render_template('signup.html', lang=lang_dict, message=message)
    if request.method == 'GET':
        language = request.accept_languages.best_match(['pl','en'])
        if request.cookies.get('language')==None:
            resp = make_response(render_template('signup.html', lang=lang_dict))
            resp.set_cookie('language', language)
            return resp
        return render_template('signup.html', lang=lang_dict)
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user:
        return redirect('/')
    if request.method == 'POST':
        session.pop('user', None)
        username = request.form['username']
        password = request.form['password']
        users = session1.query(User).all()
        if len(username)>1 and len(password)>1: #should be 5/8
            user = [x for x in users if x.username == username]
            if user:
                if user[0].password == password:
                    session['user'] = user[0].id
                    return redirect('/')
        return redirect('/login')
    if request.method == 'GET':
        language = request.accept_languages.best_match(['pl', 'en'])
        if request.cookies.get('language') == None:
            resp = make_response(render_template('login.html', lang=lang_dict))
            resp.set_cookie('language', language)
            return resp
        return render_template('login.html', lang=lang_dict)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/newpost', methods=['GET','POST'])
def new_post():
    if g.user:
        if request.method == 'POST':
            post = Post()
            image = request.files['image']
            if image.filename == '':
                redirect('/newpost')
            else:
                post.description = request.form['description']
                post.author_id = g.user.id
                post.date = str(datetime.datetime.now())
                session1.add(post)
                session1.commit()
                extension = os.path.splitext(image.filename)[1]
                post.str_id = str(post.id)+extension
                path = os.path.join(app.config['UPLOAD_FOLDER'], str(post.id)+extension)
                path1 = os.path.join(app.config['EDITED_FOLDER'], str(post.id)+extension)
                image.save(path)
                im = Image.open(path)
                ratio=im.width/im.height
                if im.width<=600 and im.height<=600:
                    if ratio > 0.8:
                        new_height = 600
                        new_width = int(new_height * ratio)
                    else:
                        new_width = 600
                        new_height = int(new_width / ratio)
                elif im.width<=600:
                    new_width = 600
                    new_height = int(new_width/ratio)
                elif im.height<=600:
                    new_height = 600
                    new_width = int(new_height * ratio)
                elif im.height>600 and im.width>600:
                    if ratio<=1.25:
                        new_height = 800
                        new_width = int(new_height * ratio)
                    else:
                        new_width = 1000
                        new_height = int(new_width / ratio)
                im=im.resize((new_width,new_height))
                x1=(im.width-600)/2+int(request.form['moved_x'])
                y1=(im.height-600)/2-int(request.form['moved_y'])
                im = im.crop((x1, y1, x1 + 600, y1 + 600))
                im.save(path1)
                users = session1.query(User).all()
                user = [x for x in users if x.id == g.user.id]
                if user:
                    user=user[0]
                    temp = copy.copy(user.posts)
                    temp.append(post.id)
                    user.posts_count = len(temp)
                    user.posts=temp
            session1.commit()
            return redirect('/')
        return render_template('newpost.html', lang=lang_dict, logged=logged)
    else:
        return redirect('/login')

@app.route('/add_avatar', methods=['GET', 'POST'])
def add_avatar():
    if g.user:
        if request.method == 'POST':
            image=request.files['image']
            extension=os.path.splitext(image.filename)[1]
            name=str(g.user.id)+extension
            path= os.path.join(app.config["PROFILE_IMAGES"], name)
            image.save(path)
            g.user.image=name
            return redirect('/user/'+str(g.user.username))
        return redirect('/')
    return redirect('/login')


@app.route('/search/<search>')
def search(search):
    return render_template('home.html', lang=lang_dict, logged=logged)

@app.route('/language/<link>')
def change_language(link):
    resp = make_response(redirect('/'+link[2:]))
    resp.set_cookie('language', link[:2])
    return resp

if __name__ == '__main__':
    app.run(debug=True)