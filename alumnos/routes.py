from . import alumnos
from flask import render_template, request, redirect, url_for
from models import Alumnos

from models import db

import forms

@alumnos.route("/alumnos")
def index():
    create_form = forms.UserForm(request.form)
    alumnos = Alumnos.query.all()
    return render_template("alumnos/listadoAlumnos.html", form=create_form, alumno=alumnos)

@alumnos.route("/alumnos/agregar", methods=['GET', 'POST'])
def alumno():
    create_form = forms.UserForm(request.form)

    # CORRECCIÓN: Se agregó 'and create_form.validate()'
    if request.method == 'POST' and create_form.validate():
        alumn = Alumnos(nombre = create_form.nombre.data,
                  apellidos = create_form.apellidos.data,
                  telefono = create_form.telefono.data,
                  email = create_form.email.data)
        db.session.add(alumn)
        db.session.commit()
        
        # CORRECCIÓN: Se cambió "index" por "alumnos.index"
        return redirect(url_for("alumnos.index")) 
    return render_template("alumnos/alumnos.html", form=create_form)

@alumnos.route("/alumnos/modificar", methods=['GET', 'POST'])
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
    
    # CORRECCIÓN: Se agregó 'and create_form.validate()'
    if request.method == 'POST' and create_form.validate():
        id = request.args.get('id')
        alumn1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

        alumn1.id = id
        alumn1.nombre = create_form.nombre.data
        alumn1.apellidos = create_form.apellidos.data
        alumn1.telefono = create_form.telefono.data
        alumn1.email = create_form.email.data
        
        db.session.add(alumn1)
        db.session.commit()
        
        # CORRECCIÓN: Se cambió "index" por "alumnos.index"
        return redirect(url_for("alumnos.index")) 
    return render_template("alumnos/modificar.html", form=create_form)

@alumnos.route("/alumnos/eliminar", methods=['GET', 'POST'])
def eliminar():
    create_form = forms.UserForm(request.form)
    
    id_alumno = request.args.get('id')
    
    if request.method == 'GET':
        alumn1 = db.session.query(Alumnos).filter(Alumnos.id == id_alumno).first()

        if alumn1:
            create_form.id.data = alumn1.id
            create_form.nombre.data = alumn1.nombre
            create_form.apellidos.data = alumn1.apellidos
            create_form.telefono.data = alumn1.telefono
            create_form.email.data = alumn1.email
    
    if request.method == 'POST':
        alumn1 = db.session.query(Alumnos).filter(Alumnos.id == id_alumno).first()
        
        if alumn1:
            alumn1.cursos.clear()
            db.session.delete(alumn1)
            db.session.commit()

        return redirect(url_for('alumnos.index'))
    return render_template("alumnos/eliminar.html", form=create_form)

@alumnos.route("/alumnos/detalles", methods=['GET'])
def detalles():
    id_alumno = request.args.get('id')
    
    alumno_completo = Alumnos.query.get(id_alumno)
    
    return render_template("alumnos/detalles.html", alumno=alumno_completo)

@alumnos.route("/alumnos/listaCursos", methods=['GET'])
def listaCursos():
    create_form = forms.UserForm(request.form)
    alumnos = Alumnos.query.all()
    return render_template("cursos/cursosAlumnos.html", form=create_form, alumno=alumnos)

@alumnos.route("/alumnos/cursos", methods=['GET'])
def cursos_inscritos():
    id_alumno = request.args.get('id')

    alumno_completo = db.session.query(Alumnos).filter(Alumnos.id == id_alumno).first()
    
    if not alumno_completo:
        return redirect(url_for('alumnos.index'))
        
    return render_template("alumnos/cursos.html", alumno=alumno_completo)