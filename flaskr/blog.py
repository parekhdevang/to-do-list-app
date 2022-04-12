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
        'SELECT t.id, t.title, t.created, u.username, t.comment, t.is_completed'
        ' FROM task t JOIN user u ON u.id = t.author_id'
        ' ORDER BY t.id'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/<int:userid>/tasklist')
@login_required
def get_list(userid):
    db = get_db()
    posts = db.execute(
        'SELECT t.id, t.title, t.created, t.comment, t.is_completed, u.username'
        ' FROM task t JOIN user u ON u.id = t.author_id'
        ' WHERE u.id = ?'
        ' ORDER BY t.id', (userid)
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
                'INSERT INTO task (title, author_id, comment)'
                ' VALUES (?, ?, ?)',
                (title, g.user['id'], comment)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT t.id, t.title, t.created, u.username, t.comment'
        ' FROM task t JOIN user u ON t.author_id = u.id'
        ' WHERE t.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Task id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
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
                'UPDATE task SET is_done = ?'
                ' WHERE id = ?',
                (1, id)
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
