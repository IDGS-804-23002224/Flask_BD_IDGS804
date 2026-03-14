from . import cursos
from flask import render_template, request, redirect, url_for
from models import Curso, Maestros, Alumnos

from models import db

import forms

@cursos.route("/cursos", methods=['GET', 'POST'])
def index():
    create_form = forms.CursoForm(request.form)
    cursos = Curso.query.all()

    return render_template("cursos/listadoCursos.html", form=create_form, cursos=cursos)

@cursos.route("/cursos/agregar", methods=['GET', 'POST'])
def curso():
    create_form = forms.CursoForm(request.form)

    maestros_db = Maestros.query.all()
    create_form.maestro_id.choices = [
        (m.matricula, f"{m.nombre} {m.apellidos} - {m.especialidad}") for m in maestros_db
    ]

    # CORRECCIÓN: Se agregó la validación 'and create_form.validate()'
    if request.method == 'POST' and create_form.validate():
        cur = Curso(
            nombre = create_form.nombre.data,
            descripcion = create_form.descripcion.data,
            maestro_id = create_form.maestro_id.data 
        )
        
        db.session.add(cur)
        db.session.commit()
        
        return redirect(url_for("cursos.index")) 
    
    return render_template("cursos/cursos.html", form=create_form)


@cursos.route("/cursos/detalles", methods=['GET', 'POST'])
def detalles():

    if request.method == 'GET':
        id = request.args.get('id')

        curso_completo = Curso.query.get(id) 
        
        return render_template("cursos/detalles.html", curso=curso_completo)

@cursos.route("/cursos/modificar", methods=['GET', 'POST'])
def modificar():
    create_form = forms.CursoForm(request.form)
    
    maestros_db = Maestros.query.all()
    create_form.maestro_id.choices = [
        (m.matricula, f"{m.nombre} {m.apellidos} - {m.especialidad}") for m in maestros_db
    ]

    if request.method == 'GET':
        id = request.args.get('id')

        cur1 = db.session.query(Curso).filter(Curso.id == id).first()
    
        create_form.id.data = request.args.get('id')
        create_form.nombre.data = cur1.nombre
        create_form.descripcion.data = cur1.descripcion
        create_form.maestro_id.data = cur1.maestro_id
    
    # CORRECCIÓN: Se agregó la validación 'and create_form.validate()'
    if request.method == 'POST' and create_form.validate():
        id = request.args.get('id')
        cur1 = db.session.query(Curso).filter(Curso.id == id).first()

        cur1.id = id
        cur1.nombre = create_form.nombre.data
        cur1.descripcion = create_form.descripcion.data
        cur1.maestro_id = create_form.maestro_id.data
        
        db.session.add(cur1)
        db.session.commit()
        
        return redirect(url_for("cursos.index")) 
    return render_template("cursos/modificar.html", form=create_form)

@cursos.route("/cursos/eliminar", methods=['GET', 'POST'])
def eliminar():
    create_form = forms.CursoForm(request.form)
    
    maestros_db = Maestros.query.all()
    create_form.maestro_id.choices = [
        (m.matricula, f"{m.nombre} {m.apellidos} - {m.especialidad}") for m in maestros_db
    ]

    id_curso = request.args.get('id')

    if request.method == 'GET':
        cur1 = db.session.query(Curso).filter(Curso.id == id_curso).first()
    
        if cur1:
            create_form.id.data = cur1.id
            create_form.nombre.data = cur1.nombre
            create_form.descripcion.data = cur1.descripcion
            create_form.maestro_id.data = cur1.maestro_id
    
    if request.method == 'POST':
        cur1 = db.session.query(Curso).filter(Curso.id == id_curso).first()

        if cur1:
            cur1.alumnos.clear()
            
            db.session.delete(cur1)
            db.session.commit()
        
        return redirect(url_for("cursos.index")) 
    return render_template("cursos/eliminar.html", form=create_form)


# --- VISTA 1: ALUMNOS Y CURSOS ---
@cursos.route("/cursos/alumnos_cursos", methods=['GET', 'POST'])
def alumnos_cursos():
    alumnos = Alumnos.query.all()
    cursos_encontrados = []
    alumno_seleccionado = None

    if request.method == 'POST':
        # Capturamos lo que el usuario seleccionó/escribió en el combobox
        busqueda = request.form.get('alumno_busqueda')
        if busqueda:
            try:
                # Extraemos solo el ID numérico (ej. de "5 - Juan Perez" sacamos el "5")
                alumno_id = int(busqueda.split(' - ')[0])
                alumno_seleccionado = Alumnos.query.get(alumno_id)
                
                if alumno_seleccionado:
                    # Obtenemos los cursos a través de la relación configurada en models.py
                    cursos_encontrados = alumno_seleccionado.cursos
            except:
                pass # Evita que el sistema falle si escriben algo que no está en la lista
                
    return render_template("cursos/alumnos_cursos.html", alumnos=alumnos, cursos=cursos_encontrados, alumno=alumno_seleccionado)


# --- VISTA 2: MAESTROS Y CURSOS ---
@cursos.route("/cursos/maestros_cursos", methods=['GET', 'POST'])
def maestros_cursos():
    maestros = Maestros.query.all()
    cursos_encontrados = []
    maestro_seleccionado = None

    if request.method == 'POST':
        busqueda = request.form.get('maestro_busqueda')
        if busqueda:
            try:
                maestro_id = int(busqueda.split(' - ')[0])
                maestro_seleccionado = Maestros.query.get(maestro_id)
                
                if maestro_seleccionado:
                    # Obtenemos los cursos a través de la relación
                    cursos_encontrados = maestro_seleccionado.cursos
            except:
                pass
                
    return render_template("cursos/maestros_cursos.html", maestros=maestros, cursos=cursos_encontrados, maestro=maestro_seleccionado)