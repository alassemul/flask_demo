from flask import Flask, render_template, request, flash, redirect,url_for
from form import RegForm, LoginForm, ArticleForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://alass:open0930@127.0.0.1:3306/fibersupport'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'alass'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(16), unique=True)
    users = db.relationship('User', backref='Role')

    def __repr__(self) -> str:
        return '<Role: %s %s>' % (self.id, self.role_name)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))
    password = db.Column(db.String(16))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    dep = db.Column(db.String(16))
    phone_num = db.Column(db.String(16))

    def __repr__(self) -> str:
        return '<User: %s %s>' % (self.user_name, self.dep)


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.Date, nullable=False)
    project_type = db.Column(db.String(16))
    project_name = db.Column(db.String(96))
    reason = db.Column(db.String(256))
    fiber_type = db.Column(db.String(16), nullable=False)
    fiber_length = db.Column(db.Float)
    closure_type = db.Column(db.String(16))
    closure_number = db.Column(db.Integer)
    other_things = db.Column(db.String(16))
    recycle_fiber_type = db.Column(db.String(16))
    recycle_fiber_length = db.Column(db.Float)
    create_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    approver_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self) -> str:
        return '<Article: %s %s %s %s %s>' % (self.id, self.create_time, self.project_name,
                                              self.fiber_type, self.fiber_length)


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if form.validate_on_submit():
            user = User.query.filter_by(name=username).first()
            if user is None:
                flash('用户名或密码不正确')
            else:
                if user.password == password:
                    login_user(user)
                    return redirect('/newarti')
                else:
                    flash('用户名或密码不正确')
    return render_template("login.html", form=form)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegForm()
    if request.method == 'POST':
        user = User()
        user.name = request.form.get('username')
        user.password = request.form.get('password')
        user.dep = request.form.get('dep')
        user.phone_num = request.form.get('phone_num')
        if form.validate_on_submit():
            user.role_id = 5
            db.session.add(user)
            db.session.commit()
            flash('注册成功')
            return redirect('/')
    else:
            flash('参数有误')

    return render_template("reg.html", form=form)


@app.route('/newarti', methods=['GET', 'POST'])
@login_required
def newarti():
    form = ArticleForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            ar = Article()
            ar.create_time = request.form.get('create_time')
            ar.project_type = request.form.get('project_type')
            ar.project_name = request.form.get('project_name')
            ar.fiber_type = request.form.get('fiber_type')
            ar.fiber_length = request.form.get('fiber_length')
            ar.closure_type = request.form.get('closure_type')
            ar.closure_number = request.form.get('closure_number')
            ar.other_things = request.form.get('other_things')
            ar.reason = request.form.get('reason')
            ar.recycle_fiber_type = request.form.get('recycle_fiber_type')
            ar.recycle_fiber_length = request.form.get('recycle_fiber_length')
            ar.create_user_id = current_user.id
            ar.approver_id = current_user.id
            db.session.add(ar)
            db.session.commit()
            return redirect('/newarti')

    articles = Article.query.filter_by(create_user_id=current_user.id)
    return render_template("createArti.html", form=form, articles=articles)


@app.route('/delete/<article_id>', methods=['GET', 'POST'])
def delete(article_id):
    ar = Article.query.get(article_id)
    if ar:
        try:
            db.session.delete(ar)
            db.session.commit()
        except Exception as e:
            print(e)
            flash('删除失败')
            db.session.rollback()
    else:
        flash('无此纪录')

    return redirect(url_for('newarti'))


if __name__ == '__main__':
    app.run()
