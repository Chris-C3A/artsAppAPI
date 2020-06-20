from app import app, bcrypt, db
from flask import request, render_template, send_file, abort
from app.src.models import User, Art
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from datetime import date
import json, re, random, os, pickle, ast
import click

ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpg', 'jpeg', 'jfif'}
UPLOAD_DIR = "uploads"

def allowed_to_upload(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def list_to_json(lst):
    return json.dumps([obj.toJSON() for obj in lst])

def nanoid(n):
    code = ''
    # asci codes
    lst = [(48, 57), (65, 90), (97, 122)]
    for i in range(n):
        rng = random.choice(lst)
        asc = random.randint(*rng)
        code += chr(asc)
    return code


@app.route('/')
def home():
    print(nanoid(10))
    arts = Art.query.order_by(Art.date_posted.desc())
    return {"data": list_to_json(arts)}

@app.cli.command('initdb')
def sayname(name):
    db.drop_all()
    db.create_all()
    print("initialized database")

@app.route('/viewart/',methods=['POST'])
@login_required
def view_art():
    data = request.json
    img_id = data["img_id"]

    try:
        r = Art.query.filter_by(img_id=img_id).first()
        # if r is None:
        #     return json.dumps({"msg": "art not found"})
        return r.toJSON()
    except Exception as e:
        print(e)
        return json.dumps({"msg": "art not found"})


@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    data = request.json
    file = request.files['file']
    if file.filename == '':
        return json.dumps({'error':'no file selected'})
    if file and allowed_to_upload(file.filename):
        filename = secure_filename(file.filename)
        image_id = random.randint(1111111111111111,9999999999999999)
        extension = filename.rsplit('.', 1)[1].lower()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f"{image_id}.{extension}"))
        title = data["title"]
        description = data["description"]
        new_piece = Art(title=title,
                        description=description,
                        img_id = image_id,
                        img_extension=extension,
                        author = current_user)
        db.session.add(new_piece)
        db.session.commit()
        print(f"################################\n image id: {image_id}\n#################################")
        return json.dumps({'image_id':image_id})



@app.route('/register', methods=['POST'])
def register():
    data = request.json
    print(data)
    username = User.query.filter_by(username=data["username"]).first()
    if username:
        return json.dumps({"error": "username taken"})
    hashed_pass = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
    newUser = User(username=data["username"], type_of_account=data["type_of_account"], password=hashed_pass)
    db.session.add(newUser)
    db.session.commit()
    return newUser.toJSON()

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    user = User.query.filter_by(username=data["username"]).first()
    if user and bcrypt.check_password_hash(user.password, data["password"]):
        login_user(user)
        return user.toJSON()

    return json.dumps({"error": "Incorrect Username or Password"})

@app.route('/logout')
def logout():
    logout_user()
    return json.dumps({"ok": "logged out"})

@app.route('/user/<string:username>')
def user_arts(username):
    user = User.query.filter_by(username=username).first_or_404()
    arts = Art.query.filter_by(author=user).order_by(Art.date_posted.desc())

    return json.dumps({
        "data": {
            "user": user.toJSON(),
            "arts": list_to_json(arts),
            "liked_arts": list_to_json(user.liked_arts),
            "disliked_arts": list_to_json(user.disliked_arts)
        }
    })

@app.route('/art', methods=['GET'])
def art_search():
    search = request.args.get('search')
    arts = Art.query.filter(Art.title.like(search+'%')).all()
    return list_to_json(arts)


@app.route('/art/<int:art_id>/update', methods=['POST'])
@login_required
def update_art(art_id):
    art = Art.query.get_or_404(art_id)
    if art.author != current_user:
        abort(403)
    data = request.json
    # update img data
        # check if received file
        # delete old img from uploads
        # save new img with new img_id
        # save new id in db with ext
    art.title = data['title'] if 'title' in data else art.title
    art.description = data['description'] if 'description' in data else art.description
    db.session.commit()
    return art.toJSON()


@app.route('/art/<int:art_id>/delete', methods=['POST'])
@login_required
def delete_art(art_id):
    art = Art.query.get_or_404(art_id)
    if art.author != current_user:
        abort(403)
    db.session.delete(art)
    db.session.commit()
    return json.dumps({"ok": "deleted"})

@app.route('/art/<int:art_id>/like', methods=['POST'])
@login_required
def like_art(art_id):
    art = Art.query.get_or_404(art_id)
    if current_user in art.likes:
        art.likes.remove(current_user)
        db.session.commit()
        return json.dumps({"ok": "removed like"})
    if current_user in art.dislikes:
        art.dislikes.remove(current_user)

    art.likes.append(current_user)
    db.session.commit()
    return json.dumps({"ok": "liked"})

@app.route('/art/<int:art_id>/dislike', methods=['POST'])
@login_required
def dislike_art(art_id):
    art = Art.query.get_or_404(art_id)
    if current_user in art.dislikes:
        art.dislikes.remove(current_user)
        db.session.commit()
        return json.dumps({"ok": "removed dislike"})
    if current_user in art.likes:
        art.likes.remove(current_user)

    art.dislikes.append(current_user)
    db.session.commit()
    return json.dumps({"ok": "disliked"})

@app.route('/get_image', methods=['POST'])
def get_image():
    img_id = request.json['img_id']
    img_ext = request.json['img_ext']
    img_path = f"{UPLOAD_DIR}/{img_id}.{img_ext}"
    return send_file(img_path, mimetype='image/gif')

@app.route('/test')
@login_required
def test():
    return f"hello there {current_user.username}"
