from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopementConfig
from flask import g
from flask_migrate import Migrate
import forms

from models import db
from models import Alumnos

app = Flask(__name__)
app.config.from_object(DevelopementConfig)
db.init_app(app)
migrate = Migrate(app, db) # Migración a DB
csrf=CSRFProtect()

@app.route("/")
@app.route("/index")
def index():
	create_form = forms.UserForm(request.form)
	#tem = Alumnos.query('select * from alumnos')
	alumnos = Alumnos.query.all()
	return render_template("index.html", form=create_form, alumno=alumnos)

@app.route("/alumnos", methods=['GET', 'POST'])
def alumno():
	create_form = forms.UserForm(request.form)

	if request.method == 'POST':
		alumn = Alumnos(nombre = create_form.nombre.data,
				  apellidos = create_form.apellidos.data,
				  telefono = create_form.telefono.data,
				  email = create_form.email.data)
		db.session.add(alumn)
		db.session.commit()
		
		return redirect(url_for("index")) 
	return render_template("alumnos.html", form=create_form)

@app.route("/modificar", methods=['GET', 'POST'])
def modificar():
	create_form = forms.UserForm(request.form)

	if request.method == 'GET':
		id = request.args.get('id')

		alumn1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

		create_form.id.data = request.args.get('id')
		create_form.nombre.data = alumn1.nombre
		create_form.apellidos.data = alumn1.apellidos
		create_form.telefono.data = alumn1.telefono
		create_form.email.data = alumn1.email
	
	if request.method == 'POST':
		id = request.args.get('id')
		alumn1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

		alumn1.id = id
		alumn1.nombre = create_form.nombre.data
		alumn1.apellidos = create_form.apellidos.data
		alumn1.telefono = create_form.telefono.data
		alumn1.email = create_form.email.data
		
		db.session.add(alumn1)
		db.session.commit()
		
		return redirect(url_for("index")) 
	return render_template("modificar.html", form=create_form)

@app.route("/eliminar", methods=['GET', 'POST'])
def eliminar():
	create_form = forms.UserForm(request.form)

	if request.method == 'GET':
		id = request.args.get('id')

		alumn1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

		create_form.id.data = request.args.get('id')
		create_form.nombre.data = alumn1.nombre
		create_form.apellidos.data = alumn1.apellidos
		create_form.telefono.data = alumn1.telefono
		create_form.email.data = alumn1.email
	
	if request.method == 'POST':
		id = create_form.id.data
		alumn1 = Alumnos.query.get(id)

		db.session.delete(alumn1)
		db.session.commit()
		
		return redirect(url_for("index")) 
	return render_template("eliminar.html", form=create_form)

@app.route("/detalles", methods=['GET', 'POST'])
def detalles():
	create_form = forms.UserForm(request.form)

	if request.method == 'GET':
		id = request.args.get('id')

		alumn1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
		id = request.args.get('id')

		nombre = alumn1.nombre
		apellidos = alumn1.apellidos
		telefono = alumn1.telefono
		email = alumn1.email
		
	return render_template("detalles.html", id=id, nombre=nombre, apellidos=apellidos, telefono=telefono, email=email)

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"),404

if __name__ == '__main__':
	csrf.init_app(app)
	
	with app.app_context():
		db.create_all()

	app.run()