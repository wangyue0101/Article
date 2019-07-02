from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class UserLoginForm(FlaskForm):
    username = StringField(label="用户名", validators=[DataRequired()])
    password = PasswordField(label="密码", validators=[DataRequired()])
    submit = SubmitField(label="登录")


class AddArticleForm(FlaskForm):
    username = StringField(label="用户名", validators=[DataRequired()])
    title = StringField(label="文章标题", validators=[DataRequired()])
    content = TextAreaField(label="文章内容", validators=[DataRequired()])
    submit = SubmitField(label="添加")


class UserRegisterForm(FlaskForm):
    username = StringField(label="用户名", validators=[
        DataRequired(), Length(2, 6)
    ])
    email = StringField(label="邮箱", validators=[DataRequired(), Email()])
    password = PasswordField(label="密码", validators=[
        DataRequired(), Length(8, 16, message="password length must be 8..17"), EqualTo("password_2", message="The two passwords must be identical")
    ])
    password_2 = PasswordField(label="密码", validators=[
        DataRequired(),
    ])
    submit = SubmitField(label="注册")


class ArticleComments(FlaskForm):
    title = StringField(label="评论标题", validators=[DataRequired(), Length(1)])
    comment = TextAreaField(label="评论内容", validators=[DataRequired(), Length(6)])
    submit = SubmitField(label="提交")
