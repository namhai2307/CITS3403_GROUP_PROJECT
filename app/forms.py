
from flask_wtf import FlaskForm
from wtforms import DateField, StringField, TextAreaField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed

#Corresponding to the "Add Data to Calendar" form on the left
class EventForm(FlaskForm):
    date = DateField('Select Date', 
                    format='%d/%m/%Y',  #Accurately correspond to the dd/mm/yyyy format in the image
                    validators=[DataRequired(),DateRange(min=date(2024,1,1), max=date(2026,12,31))],
                    render_kw={"placeholder": "dd/mm/yyyy"})
    title = StringField('Title', 
                       validators=[
                           DataRequired(),
                           Length(max=100, message="Maximum 100 characters")  #Match image title length
                       ])
    description = TextAreaField('Description')
    attachment = FileField('Attach File (optional)', 
                         validators=[FileAllowed(['pdf', 'docx', 'jpg'], 
                                               'Only PDF/DOCX/JPG allowed')])
    sharing = RadioField('Sharing', 
                        choices=[('private', 'Private'), 
                                 ('public', 'Public'),
                                 ('friends', 'Selected Friends')],
                        default='private')  #Default Private option 
    submit = SubmitField('Add to Calendar', 
                        render_kw={"class": "btn-primary"})  

#Friend Request Form
class FriendRequestForm(FlaskForm):
    username = StringField("Friend's Username", 
                          validators=[DataRequired()],
                          render_kw={"placeholder": "Enter username"})
    message = TextAreaField("Personal Message (optional)")
    send = SubmitField("Send Request")