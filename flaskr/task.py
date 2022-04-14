from datetime import datetime, timedelta
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('task', __name__)

@bp.route('/')
@login_required
def index():
    return redirect(url_for('task.tasks'))

@bp.route('/tasks')
@login_required
def tasks():
    return redirect(url_for('task.get_list', userid=g.user['id'], firstdate=datetime.now().today().date()))


@bp.route('/<currentdate>/movebackaday')
@login_required
def move_back_a_day(currentdate):
    day_before = datetime.strptime(currentdate, '%Y-%m-%d') - timedelta(days=1)
    return redirect(url_for('task.get_list', userid=g.user['id'], firstdate=day_before.date()))

@bp.route('/<currentdate>/moveforwardaday')
@login_required
def move_forward_a_day(currentdate):
    day_after = datetime.strptime(currentdate, '%Y-%m-%d') + timedelta(days=1)
    return redirect(url_for('task.get_list', userid=g.user['id'], firstdate=day_after.date()))


@bp.route('/<int:userid>/<firstdate>/tasklist', methods=('GET', 'POST'))
@login_required
def get_list(userid, firstdate):
    if request.method == 'POST':
        return redirect(url_for('task.create', currentdate=firstdate, request=request), code=307)

    db = get_db()
    tasks_all = []
    for i in range(5):
        date = datetime.strptime(firstdate, '%Y-%m-%d') + timedelta(days=i)
        tasks = db.execute(
            'SELECT t.id, t.title, t.comment, t.is_completed, t.due_date'
            ' FROM task t JOIN user u ON u.id = t.author_id'
            ' WHERE u.id = ? AND t.due_date = ?'
            ' ORDER BY t.id', (userid, date.date())
        ).fetchall()
        tasks_all.append(tasks)
    return render_template('index.html', tasks=tasks_all, firstdate=firstdate)

@bp.route('/<currentdate>/create', methods=('GET', 'POST'))
@login_required
def create(currentdate):
    title = request.form['title']
    comment = request.form['comment']
    due_date = request.form['due_date']
    repeat = request.form['repeat'].lower()
    error = ""

    if not title:
        error = 'Title is required. '
    if not due_date:
        error += 'Date is required.'

    if error:
        flash(error)
    else:
        db = get_db()
        db.execute(
            "INSERT INTO task (title, author_id, comment, due_date)"
            " VALUES (?, ?, ?, ?)",
            (title, g.user['id'], comment, due_date)
        )
        db.commit()
        days = 0
        if repeat == "every day":
            days = 1
        elif repeat == "every week":
            days = 7
        elif repeat == "every month":
            days = 30
        elif repeat == "every year":
            days = 365

        if days > 0:
            new_date = datetime.strptime(due_date, '%Y-%m-%d')
            for _ in range(10):
                new_date += timedelta(days=days)
                db.execute(
                    "INSERT INTO task (title, author_id, comment, due_date)"
                    " VALUES (?, ?, ?, ?)",
                    (title, g.user['id'], comment, new_date.strftime("%Y-%m-%d"))
                )
                db.commit()

    return redirect(url_for('task.get_list', userid=g.user['id'], firstdate=currentdate))


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

@bp.route('/<int:id>/<currentdate>/<is_completed>/completed', methods=('GET', 'POST'))
@login_required
def completed(id, currentdate, is_completed):
    db = get_db()
    db.execute(
        'UPDATE task SET is_completed = ?'
        ' WHERE id = ?',
        (1 if int(is_completed) == 0 else 0, id)
    )
    db.commit()
    return redirect(url_for('task.get_list', userid=g.user['id'], firstdate=datetime.strptime(currentdate, '%Y-%m-%d').date()))

@bp.route('/<int:id>/<currentdate>/delete', methods=('POST',))
@login_required
def delete(id, currentdate):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM task WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('task.get_list', userid=g.user['id'], firstdate=datetime.strptime(currentdate, '%Y-%m-%d').date()))
