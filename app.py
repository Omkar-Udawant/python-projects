from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email


app = Flask(__name__)
app.config["SECRET_KEY"] = "replace-this-with-env-secret"
Bootstrap(app)


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Log In")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if (
            form.email.data == "admin@email.com"
            and form.password.data == "12345678"
        ):
            return render_template("success.html")
        return render_template("denied.html")

    return render_template("login.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
