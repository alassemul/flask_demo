from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, DateField, FloatField
from wtforms.validators import DataRequired, EqualTo


class RegForm(FlaskForm):
    username = StringField('用户名：', validators=[DataRequired()])
    password = PasswordField('密码：', validators=[DataRequired()])
    password2 = PasswordField('确认密码：', validators=[DataRequired(), EqualTo('password', message='密码不一致')])
    dep = SelectField('部门名称：', validators=[DataRequired()], choices=[('张店区','张店区'),
                                                                     ('淄川区','淄川区'),('博山区','博山区'),('周村区','周村区'),
                                                                     ('临淄区','临淄区'),('高青县','高青县'),('桓台县','桓台县'),
                                                                     ('沂源县', '沂源县'),
                                                                     ('市公司','市公司')])
    phone_num = StringField('手机号：', validators=[DataRequired()])
    submit = SubmitField('注册')


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登陆')


class ArticleForm(FlaskForm):
    create_time = DateField('时间', validators=[DataRequired()])
    project_type = SelectField('分类（抢修/迁改/整改）', validators=[DataRequired()], choices=[('0', '抢修'),
                                                                                     ('1', '迁改'),
                                                                                     ('2', '整改')])
    project_name = StringField('维护项目名称', validators=[DataRequired()])
    reason = StringField('抢修故障/迁改/整改原因')
    fiber_type = SelectField('使用光缆类型', validators=[DataRequired()], choices=[('12芯光缆', '12芯光缆'),
                                                                             ('24芯光缆', '24芯光缆'),
                                                                             ('48芯光缆', '48芯光缆'),
                                                                             ('96芯光缆', '96芯光缆'),
                                                                             ('144芯光缆', '144芯光缆')])
    fiber_length = FloatField('光缆长度（米）', validators=[DataRequired()])
    closure_type = SelectField('使用接头盒类型', validators=[DataRequired()], choices=[('12芯接头盒', '12芯接头盒'),
                                                                               ('24芯接头盒', '24芯接头盒'),
                                                                               ('48芯接头盒', '48芯接头盒'),
                                                                               ('96芯接头盒', '96芯接头盒'),
                                                                               ('144芯接头盒', '144芯接头盒')])

    reason = StringField('原因')
    closure_number = IntegerField('接头盒个数', validators=[DataRequired()])
    other_things = StringField('其他材料用量')
    recycle_fiber_type = SelectField('撤旧光缆类型', choices=[('12芯光缆', '12芯光缆'),
                                                        ('24芯光缆', '24芯光缆'),
                                                        ('48芯光缆', '48芯光缆'),
                                                        ('96芯光缆', '96芯光缆'),
                                                        ('144芯光缆', '144芯光缆')])
    recycle_fiber_length = FloatField('撤旧光缆长度（米）')

    submit = SubmitField('提交')
