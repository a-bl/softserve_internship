from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, SelectField, \
    IntegerField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, Interview, Grade, Question
from datetime import datetime, date


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    password = PasswordField('Password', validators=[DataRequired()])
    is_admin = BooleanField('Admin Status', default=False)
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Edit')

    def __init__(self, original_username, original_name, original_surname, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_name = original_name
        self.original_surname = original_surname

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class UserFrom(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email")
    first_name = StringField("First Name")
    last_name = StringField("Lask Name")
    password = PasswordField("Password", validators=[DataRequired()])
    is_admin = BooleanField("Admin status", default=False)
    submit = SubmitField("Add")


class AddQuestionForm(FlaskForm):
    essence = TextAreaField('Question description', validators=[DataRequired()])
    supposed_answer = StringField('Answer', validators=[DataRequired()])
    max_grade = IntegerField('Max grade', default=10, validators=[DataRequired()])
    short_description = StringField('Short description', validators=[DataRequired()])
    submit = SubmitField('Add')

    # def validate_essence(self, essence):
    #     question = Question.query.filter_by(essence=essence.data).first()
    #     if question is not None:
    #         raise ValidationError('Please use a different essence.')


class EditQuestionForm(FlaskForm):
    essence = StringField('Question', validators=[DataRequired()])
    supposed_answer = StringField('Answer', validators=[DataRequired()])
    max_grade = IntegerField('Max Grade', default=10, validators=[DataRequired()])
    short_description = StringField('Short description', validators=[DataRequired()])
    submit = SubmitField('Edit')

    # def __init__(self, grade, *args, **kwargs):
    #     super(EditQuestionForm, self).__init__(*args, **kwargs)
    #     self.grades = grade
    #
    # def validate_username(self, essence):
    #     if essence.data != self.essence:
    #         question = Question.query.filter_by(essence=self.essence.data).first()
    #         if question is not None:
    #             raise ValidationError('Please use a different essence.')


class AddInterviewForm(FlaskForm):
    candidate = StringField('Candidate Full Name', validators=[DataRequired()])
    questions = SelectMultipleField('Select Questions', coerce=str)
    # date = DateField('Choose date', format='%Y-%m-%d', default=date.today(), validators=[DataRequired()])
    # start_time = SelectField('Choose starting time(in 24hr expression)', coerce=int,
    #                          choices=[(i, i) for i in range(9, 18)], validators=[DataRequired()])
    # end_time = SelectField('Choose starting time(in 24hr expression)', coerce=int,
    #                        choices=[(i, i) for i in range(9, 18)], validators=[DataRequired()])
    interviewers = SelectMultipleField('Select Interviewers', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Add')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def new(cls):
        form = cls()
        form.interviewers.choices = User.get_selection_list()
        form.questions.choices = Question.get_selection_list()
        return form


class GradeForm(FlaskForm):
    questions = SelectField('Question', coerce=int)
    interviewers = SelectField('Interviewer', coerce=str)
    interviews = SelectField('Interview', coerce=int)
    grade = SelectField('Grade', default=1, coerce=int, choices=[i for i in range(0, 11)])
    submit = SubmitField('Add')

    @classmethod
    def new(cls):
        form = cls()
        form.interviewers.choices = User.get_selection_list()
        form.questions.choices = Question.get_selection_list()
        form.interviews.choices = Interview.get_selection_list()
        return form


class EditGradeForm(FlaskForm):
    questions = SelectField('Question', coerce=int)
    interviewers = SelectField('Interviewer', coerce=str)
    interviews = SelectField('Interview', coerce=int)
    submit = SubmitField('Edit')

    @classmethod
    def new(cls):
        form = cls()
        form.interviewers.choices = User.get_selection_list()
        form.questions.choices = Question.get_selection_list()
        form.interviews.choices = Interview.get_selection_list()
        return form
