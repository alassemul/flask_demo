from flask import Flask, render_template, request, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://alass:open0930@127.0.0.1:3306/fibersupport'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'alass'
db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(16), unique=True)
    users = db.relationship('User', backref='Role')

    def __repr__(self) -> str:
        return '<Role: %s %s>' % (self.id, self.role_name)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(16))
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
    fiber_type = db.Column(db.Integer, nullable=False)
    fiber_length = db.Column(db.Integer)
    closure_type = db.Column(db.Integer)
    closure_number = db.Column(db.Integer)
    other_things = db.Column(db.String(16))
    recycle_fiber_type = db.Column(db.String(16))
    recycle_fiber_length = db.Column(db.Integer)
    create_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    approver_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self) -> str:
        return '<Article: %s %s %s %s %s>' % (self.id, self.create_time, self.project_name,
                                              self.fiber_type, self.fiber_length)


class RegForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password', message='密码不一致')])
    submit = SubmitField('注册')


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登陆')


class ArticleForm(FlaskForm):
    create_time = DateField('时间', validators=[DataRequired()])
    project_type = StringField('分类（抢修/迁改/整改）', validators=[DataRequired()])
    project_name = StringField('维护项目名称', validators=[DataRequired()])
    reason = StringField('抢修故障/迁改/整改原因')
    fiber_type = SelectField('使用光缆类型', validators=[DataRequired()], choices=[('0', '12芯光缆'),
                                                                             ('1', '24芯光缆'),
                                                                             ('2', '48芯光缆'),
                                                                             ('3', '96芯光缆'),
                                                                             ('4', '144芯光缆')])
    fiber_length = IntegerField('光缆长度（米）', validators=[DataRequired()])
    closure_type = SelectField('使用接头盒类型', validators=[DataRequired()], choices=[('0', '12芯光缆'),
                                                                               ('1', '24芯光缆'),
                                                                               ('2', '48芯光缆'),
                                                                               ('3', '96芯光缆'),
                                                                               ('4', '144芯光缆')])

    closure_number = IntegerField('接头盒个数', validators=[DataRequired()])
    other_things = StringField('其他材料用量')
    recycle_fiber_type = SelectField('撤旧光缆类型', choices=[('0', '12芯光缆'),
                                                        ('1', '24芯光缆'),
                                                        ('2', '48芯光缆'),
                                                        ('3', '96芯光缆'),
                                                        ('4', '144芯光缆')])
    recycle_fiber_length = IntegerField('撤旧光缆长度（米）')

    submit = SubmitField('提交')


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if form.validate_on_submit():

            return render_template("main.html")
    return render_template("login.html", form=form)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegForm()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if form.validate_on_submit():
            a = User()  # type: User
            a.user_name = username
            a.password = password
            a.role_id = 2
            db.session.add(a)
            db.session.commit()
            flash('注册成功')
            return redirect('/')
    else:
            flash('参数有误')

    return render_template("reg.html", form=form)


if __name__ == '__main__':
    app.run()
