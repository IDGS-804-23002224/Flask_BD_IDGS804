from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopementConfig
from flask import g
import forms

from models import db
from models import Alumnos

app = Flask(__name__)
app.config.from_object(DevelopementConfig)
csrf=CSRFProtect()

@app.route("/")
@app.route("/index")
def index():
	create_form = forms.UserForm(request.form)
	#tem = Alumnos.query('select * from alumnos')
	alumnos = Alumnos.query.all()
	return render_template("index.html", form=create_form, alumno=alumnos)

@app.route("/Alumnos")
def alumno():
	return render_template("alumnos.html")

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"),404

if __name__ == '__main__':
	csrf.init_app(app)
	db.init_app(app)
	
	with app.app_context():
		db.create_all()

	app.run()