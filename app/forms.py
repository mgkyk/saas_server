from wtforms import TextField, Form ,BooleanField, PasswordField, validators

### web Form ############################################################################
class SignUpForm(Form):
    username = TextField('Username', [validators.Length(min=3, max=25)])
    passwd = TextField('Passwd', [validators.Length(min=4, max=25)])
    retype_passwd = TextField('Retype Passwd', [validators.Length(min=4, max=25)])


class SignInForm(Form):
    username = TextField('Username', [validators.Length(min=3, max=25)])
    passwd = TextField('Passwd', [validators.Length(min=4, max=25)])


class GetSingleSource(Form):
    pass


class GetClusterSource(Form):
    node = TextField('number of the node', [validators.Length(min=1, max=4)])
