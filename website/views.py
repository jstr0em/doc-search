from flask import Blueprint, render_template, request, flash, jsonify, redirect, current_app
from flask_login import login_required, current_user
from .models import Document
from . import db
from werkzeug.utils import secure_filename
import json
import os

views = Blueprint('views', __name__)


@views.route('/documents', methods=['GET', 'POST'])
@login_required
def documents():
    if request.method == 'POST':
        if 'document' not in request.files:
            flash('No document included in request')
            return redirect(request.url)

        doc = request.files['document']

        if doc.filename == '':
            flash('No selected file')
            return redirect(request.url)

        doc_name = secure_filename(doc.filename)

        # Query to check if a document with the given name exists for the specified user
        existing_document = db.session.query(Document).filter_by(
            user_id=current_user.id, name=doc_name).first()
        if not existing_document:
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], doc_name)

            # TODO: Might want to add a hash part.
            new_doc = Document(name=doc_name, path=path,
                               user_id=current_user.id)
            db.session.add(new_doc)
            db.session.commit()
            doc.save(path)
            flash("File uploaded succesfully!", category='success')
            return redirect(request.url)
        else:
            flash("File already exists", category='failure')
            return redirect(request.url)

    elif request.method == 'GET':
        return render_template("documents.html", user=current_user)


@views.route('/delete-document', methods=['POST'])
def delete_document():
    # this function expects a JSON from the INDEX.js file
    doc = json.loads(request.data)
    doc_id = doc['docId']
    doc = Document.query.get(doc_id)

    if doc:
        if doc.user_id == current_user.id:
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], doc.name)
            db.session.delete(doc)
            db.session.commit()
            os.remove(path)

    return jsonify({})


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    results = []
    if request.method == 'POST':
        query = request.form.get("query")
        results = ["asd", "dsa", "fgh"]

    return render_template("home.html", user=current_user, results=results)
