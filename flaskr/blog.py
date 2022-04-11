from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    posts = db.execute(
        'SELECT id, title, created, created_by, comment, is_completed'
        ' FROM task ORDER BY id'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/<string:username>/tasklist')
@login_required
def get_list(username):
    db = get_db()
    posts = db.execute(
        'SELECT id, title, created, created_by, comment, is_completed'
        ' FROM task WHERE created_by = ?'
        ' ORDER BY id', (username)
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        comment = request.form['comment']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO task (title, created_by, comment)'
                ' VALUES (?, ?, ?)',
                (title, g.user['username'], comment)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT t.id, title, created, created_by, comment'
        ' FROM task t JOIN user u ON t.created_by = u.username'
        ' WHERE t.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Task id {id} doesn't exist.")

    if check_author and post['created_by'] != g.user['username']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        comment = request.form['comment']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE task SET title = ?, comment = ?'
                ' WHERE id = ?',
                (title, comment, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/completed', methods=('GET', 'POST'))
@login_required
def completed(id):
    post = get_post(id)

    if request.method == 'POST':
        completed = request.form['is_done']
        error = None

        if completed == False:
            error = 'Task could not complete yet.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE task SET is_done = ?, completed_date = ?'
                ' WHERE id = ?',
                (1, datetime.utcnow(), id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/completed.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM task WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
