from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import abort

from data import db_session, books
from data.add_book import AddBookForm
from data.login_form import LoginForm
from data.users import User
from data.books import Books
from data.register import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неверный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    books = db_sess.query(Books).all()
    users = db_sess.query(User).all()
    name = {name.id: (name.surname, name.name) for name in users}
    return render_template("index.html", books=books, name=name, title='Список книг')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Этот пользователь уже существует")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            sex=form.sex.data,
            email=form.email.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/addbook', methods=['GET', 'POST'])
def addbook():
    add_form = AddBookForm()
    if add_form.validate_on_submit():
        db_sess = db_session.create_session()
        books = Books(
            name=add_form.name.data,
            author=add_form.author.data,
            genre=add_form.genre.data,
            price=add_form.price.data,
            end_date=add_form.end_date.data,
            bought=add_form.bought.data
        )
        db_sess.add(books)
        db_sess.commit()
        return redirect('/')
    return render_template('addbook.html', title='Добавить книгу', form=add_form)


@app.route('/books/<int:id>', methods=['GET', 'POST'])
@login_required
def book_edit(id):
    form = AddBookForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        books = db_sess.query(Books).filter(Books.id == id,
                                           (Books.author == current_user.id) | (
                                                   current_user.id == 1)).first()
        if books:
            form.books.data = books.book
            form.author.data = books.author
            form.genre.data = books.genre
            form.price.data = books.price
            form.bought.data = books.bought
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        books = db_sess.query(Books).filter(Books.id == id,
                                            (Books.author == current_user.id) | (
                                                    current_user.id == 1)).first()
        if books:
            books.book = form.books.data
            books.author = form.author.data
            books.genre = form.genre.data
            books.price = form.price.data
            books.bought = form.bought.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('addbook.html', title='Редактировать книгу', form=form)


@app.route('/book_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Books).filter(Books.id == id,
                                       (Books.author == current_user.id) | (
                                               current_user.id == 1)).first()

    if books:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


def main():
    db_session.global_init("db/mars_explorer.sqlite")

    app.run()


if __name__ == '__main__':
    main()
