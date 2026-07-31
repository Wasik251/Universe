import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from models import (db, User, Post, PostLike, ChatMessage, Movie, MovieReview, Watchlist, Game,
                    GameReview, UserGameLibrary, LfgPost, Department, Course,
                    AcademicNote, PastQuestion, MCQ, DiscussionThread, DiscussionReply)
from seed import seed

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
if os.environ.get('VERCEL'):
    db_path = 'sqlite:////tmp/universe.db'
else:
    db_path = 'sqlite:///' + os.path.join(BASE_DIR, 'universe.db')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', db_path)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


with app.app_context():
    db.create_all()
    seed()


# ---------- AUTH ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        display = request.form.get('display_name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        try:
            age = int(request.form.get('age', 0) or 0)
        except ValueError:
            age = 0

        errors = []
        if not username or not display or not email:
            errors.append('Please fill in all fields')
        if User.query.filter_by(username=username).first():
            errors.append('Username already taken')
        if email and User.query.filter_by(email=email).first():
            errors.append('Email already registered')
        if not email or '@' not in email or '.' not in email:
            errors.append('Enter a valid email address')
        if len(password) < 4:
            errors.append('Password must be at least 4 characters')
        if password != confirm:
            errors.append('Passwords do not match')
        if age < 10:
            errors.append('You must be at least 10 years old to join UniVerse')

        if errors:
            for e in errors:
                flash(e, 'error')
        else:
            user = User(username=username, email=email,
                        password_hash=generate_password_hash(password),
                        display_name=display, age=age)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Welcome to UniVerse!', 'success')
            return redirect(url_for('feed'))
    return render_template('auth/register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first() or User.query.filter_by(email=username).first()
        if user and user.password_hash and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('feed'))
        flash('Invalid username or password', 'error')
    return render_template('auth/login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# ---------- LANDING ----------
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    return render_template('welcome.html')


@app.route('/feed')
@login_required
def feed():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('feed.html', posts=posts)


@app.route('/post', methods=['POST'])
@login_required
def create_post():
    content = request.form.get('content', '').strip()
    if content:
        post = Post(user_id=current_user.id, content=content)
        db.session.add(post)
        db.session.commit()
    return redirect(url_for('feed'))


@app.route('/post/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = db.session.get(Post, post_id)
    if post:
        existing = PostLike.query.filter_by(post_id=post_id, user_id=current_user.id).first()
        if existing:
            db.session.delete(existing)
        else:
            db.session.add(PostLike(post_id=post_id, user_id=current_user.id))
        db.session.commit()
    return redirect(request.referrer or url_for('feed'))


# ---------- MOVIES ----------
@app.route('/movies')
@login_required
def movies():
    movies = Movie.query.all()
    watchlist_ids = {w.movie_id for w in Watchlist.query.filter_by(user_id=current_user.id)}
    return render_template('movies/list.html', movies=movies, watchlist_ids=watchlist_ids)


@app.route('/movies/<int:movie_id>')
@login_required
def movie_detail(movie_id):
    movie = db.session.get(Movie, movie_id)
    if not movie:
        flash('Movie not found', 'error')
        return redirect(url_for('movies'))
    reviews = movie.reviews.all()
    in_watchlist = Watchlist.query.filter_by(user_id=current_user.id, movie_id=movie_id).first() is not None
    return render_template('movies/detail.html', movie=movie, reviews=reviews, in_watchlist=in_watchlist)


@app.route('/movies/<int:movie_id>/review', methods=['POST'])
@login_required
def movie_review(movie_id):
    rating = int(request.form.get('rating', 5))
    comment = request.form.get('comment', '').strip()
    review = MovieReview(movie_id=movie_id, user_id=current_user.id, rating=rating, comment=comment)
    db.session.add(review)
    db.session.commit()
    return redirect(url_for('movie_detail', movie_id=movie_id))


@app.route('/movies/<int:movie_id>/watchlist', methods=['POST'])
@login_required
def toggle_watchlist(movie_id):
    existing = Watchlist.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
    if existing:
        db.session.delete(existing)
    else:
        db.session.add(Watchlist(user_id=current_user.id, movie_id=movie_id))
    db.session.commit()
    return redirect(request.referrer or url_for('movie_detail', movie_id=movie_id))


@app.route('/watchlist')
@login_required
def watchlist():
    entries = Watchlist.query.filter_by(user_id=current_user.id).all()
    return render_template('movies/watchlist.html', entries=entries)


# ---------- GAMES ----------
@app.route('/games')
@login_required
def games():
    games = Game.query.all()
    return render_template('games/list.html', games=games)


@app.route('/games/<int:game_id>')
@login_required
def game_detail(game_id):
    game = db.session.get(Game, game_id)
    if not game:
        flash('Game not found', 'error')
        return redirect(url_for('games'))
    reviews = game.reviews.all()
    lib = UserGameLibrary.query.filter_by(user_id=current_user.id, game_id=game_id).first()
    return render_template('games/detail.html', game=game, reviews=reviews, lib=lib)


@app.route('/games/<int:game_id>/review', methods=['POST'])
@login_required
def game_review(game_id):
    rating = int(request.form.get('rating', 5))
    comment = request.form.get('comment', '').strip()
    review = GameReview(game_id=game_id, user_id=current_user.id, rating=rating, comment=comment)
    db.session.add(review)
    db.session.commit()
    return redirect(url_for('game_detail', game_id=game_id))


@app.route('/games/<int:game_id>/library', methods=['POST'])
@login_required
def toggle_library(game_id):
    status = request.form.get('status', 'playing')
    existing = UserGameLibrary.query.filter_by(user_id=current_user.id, game_id=game_id).first()
    if existing:
        if existing.status == status:
            db.session.delete(existing)
        else:
            existing.status = status
    else:
        db.session.add(UserGameLibrary(user_id=current_user.id, game_id=game_id, status=status))
    db.session.commit()
    return redirect(request.referrer or url_for('game_detail', game_id=game_id))


@app.route('/library')
@login_required
def library():
    entries = UserGameLibrary.query.filter_by(user_id=current_user.id).all()
    return render_template('games/library.html', entries=entries)


@app.route('/lfg')
@login_required
def lfg():
    posts = LfgPost.query.order_by(LfgPost.created_at.desc()).all()
    games = Game.query.all()
    return render_template('games/lfg.html', posts=posts, games=games)


@app.route('/lfg/create', methods=['POST'])
@login_required
def lfg_create():
    game_id = int(request.form.get('game_id', 0))
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    players = int(request.form.get('players_needed', 1) or 1)
    if title and game_id:
        post = LfgPost(user_id=current_user.id, game_id=game_id, title=title,
                       description=description, players_needed=players)
        db.session.add(post)
        db.session.commit()
        flash('LFG post created!', 'success')
    return redirect(url_for('lfg'))


# ---------- ACADEMIC ----------
@app.route('/academic')
@login_required
def academic():
    departments = Department.query.all()
    courses = Course.query.all()
    return render_template('academic/hub.html', departments=departments, courses=courses)


@app.route('/academic/departments/<int:dept_id>')
@login_required
def department(dept_id):
    dept = db.session.get(Department, dept_id)
    if not dept:
        flash('Department not found', 'error')
        return redirect(url_for('academic'))
    return render_template('academic/department.html', dept=dept, courses=dept.courses.all())


@app.route('/academic/courses/<int:course_id>')
@login_required
def course(course_id):
    course = db.session.get(Course, course_id)
    if not course:
        flash('Course not found', 'error')
        return redirect(url_for('academic'))
    notes = AcademicNote.query.filter_by(course_id=course_id).all()
    past_questions = PastQuestion.query.filter_by(course_id=course_id).all()
    mcqs = MCQ.query.filter_by(course_id=course_id).all()
    threads = DiscussionThread.query.filter_by(course_id=course_id).all()
    return render_template('academic/course.html', course=course, notes=notes,
                           past_questions=past_questions, mcqs=mcqs, threads=threads)


@app.route('/academic/courses/<int:course_id>/note', methods=['POST'])
@login_required
def add_note(course_id):
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    if title and content:
        db.session.add(AcademicNote(course_id=course_id, title=title, content=content, uploaded_by=current_user.id))
        db.session.commit()
        flash('Note added!', 'success')
    return redirect(url_for('course', course_id=course_id))


@app.route('/academic/courses/<int:course_id>/mcq', methods=['POST'])
@login_required
def add_mcq(course_id):
    q = request.form.get('question', '').strip()
    a = request.form.get('option_a', '').strip()
    b = request.form.get('option_b', '').strip()
    c = request.form.get('option_c', '').strip()
    d = request.form.get('option_d', '').strip()
    correct = request.form.get('correct_answer', '').strip().upper()
    if q and a and b and c and d and correct in 'ABCD':
        db.session.add(MCQ(course_id=course_id, question=q, option_a=a, option_b=b, option_c=c, option_d=d, correct_answer=correct))
        db.session.commit()
        flash('MCQ added!', 'success')
    return redirect(url_for('course', course_id=course_id))


@app.route('/academic/courses/<int:course_id>/thread', methods=['POST'])
@login_required
def create_thread(course_id):
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    if title:
        db.session.add(DiscussionThread(course_id=course_id, title=title, content=content, author_id=current_user.id))
        db.session.commit()
        flash('Thread created!', 'success')
    return redirect(url_for('course', course_id=course_id))


@app.route('/academic/threads/<int:thread_id>')
@login_required
def thread(thread_id):
    thread = db.session.get(DiscussionThread, thread_id)
    if not thread:
        flash('Thread not found', 'error')
        return redirect(url_for('academic'))
    replies = thread.replies.order_by(DiscussionReply.created_at.asc()).all()
    return render_template('academic/thread.html', thread=thread, replies=replies)


@app.route('/academic/threads/<int:thread_id>/reply', methods=['POST'])
@login_required
def reply_thread(thread_id):
    content = request.form.get('content', '').strip()
    if content:
        db.session.add(DiscussionReply(thread_id=thread_id, content=content, author_id=current_user.id))
        db.session.commit()
    return redirect(url_for('thread', thread_id=thread_id))


# ---------- PROFILE ----------
@app.route('/users')
@login_required
def users():
    users = User.query.order_by(User.created_at.asc()).all()
    return render_template('users.html', users=users, total=len(users))


@app.route('/profile')
@login_required
def profile():
    posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.created_at.desc()).all()
    return render_template('profile.html', user=current_user, posts=posts)


@app.route('/profile/<int:user_id>')
@login_required
def profile_view(user_id):
    user = db.session.get(User, user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('feed'))
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at.desc()).all()
    return render_template('profile.html', user=user, posts=posts)


@app.route('/profile/follow/<int:user_id>', methods=['POST'])
@login_required
def toggle_follow(user_id):
    target = db.session.get(User, user_id)
    if target and target.id != current_user.id:
        if current_user.following.filter_by(id=target.id).first():
            current_user.following.remove(target)
        else:
            current_user.following.add(target)
        db.session.commit()
    return redirect(request.referrer or url_for('profile_view', user_id=user_id))


@app.route('/profile/edit', methods=['POST'])
@login_required
def profile_edit():
    current_user.display_name = request.form.get('display_name', '').strip() or current_user.username
    current_user.bio = request.form.get('bio', '').strip()
    db.session.commit()
    flash('Profile updated!', 'success')
    return redirect(url_for('profile'))


# ---------- CHAT ----------
@app.route('/chat')
@login_required
def chat():
    messages = ChatMessage.query.order_by(ChatMessage.created_at.asc()).limit(200).all()
    return render_template('chat.html', messages=messages)


@app.route('/chat/send', methods=['POST'])
@login_required
def chat_send():
    content = request.form.get('content', '').strip()
    if content:
        db.session.add(ChatMessage(user_id=current_user.id, content=content))
        db.session.commit()
    return redirect(url_for('chat'))


# ---------- ADMIN / MANAGE ----------
@app.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    if current_user.is_admin:
        return _manage_panel()
    if request.method == 'POST':
        if request.form.get('admin_pass') == '313121':
            current_user.is_admin = True
            db.session.commit()
            flash('Admin access granted!', 'success')
            return _manage_panel()
        flash('Incorrect admin password', 'error')
    return render_template('manage.html', locked=True)


@app.route('/manage/movie/add', methods=['POST'])
@login_required
def manage_add_movie():
    if not current_user.is_admin:
        flash('Admin access required', 'error')
        return redirect(url_for('manage'))
    title = request.form.get('title', '').strip()
    year = request.form.get('release_year', type=int, default=0)
    genre = request.form.get('genre', '').strip()
    rating = request.form.get('rating', type=float, default=0)
    description = request.form.get('description', '').strip()
    image_url = request.form.get('image_url', '').strip()
    if title:
        db.session.add(Movie(title=title, release_year=year or 0, genre=genre or 'Unknown',
                             rating=rating, description=description, image_url=image_url))
        db.session.commit()
        flash(f'Movie "{title}" added!', 'success')
    return redirect(url_for('manage'))


@app.route('/manage/movie/<int:movie_id>/delete', methods=['POST'])
@login_required
def manage_delete_movie(movie_id):
    if not current_user.is_admin:
        flash('Admin access required', 'error')
        return redirect(url_for('manage'))
    movie = db.session.get(Movie, movie_id)
    if movie:
        db.session.delete(movie)
        db.session.commit()
        flash(f'Movie "{movie.title}" deleted', 'success')
    return redirect(url_for('manage'))


@app.route('/manage/post/<int:post_id>/delete', methods=['POST'])
@login_required
def manage_delete_post(post_id):
    if not current_user.is_admin:
        flash('Admin access required', 'error')
        return redirect(url_for('manage'))
    post = db.session.get(Post, post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', 'success')
    return redirect(url_for('manage'))


def _manage_panel():
    movies = Movie.query.all()
    users = User.query.all()
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('manage.html', locked=False, movies=movies, users=users, posts=posts)


# ---------- TEMPLATE HELPERS ----------
@app.context_processor
def inject_globals():
    def can_like(post):
        return PostLike.query.filter_by(post_id=post.id, user_id=current_user.id).first() is not None if current_user.is_authenticated else False
    return {'current_year': datetime.utcnow().year, 'can_like': can_like}


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
