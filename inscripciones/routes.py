from . import inscripciones
from flask import render_template, request, redirect, url_for, flash # ¡No olvides importar flash aquí!
from models import Inscripcion, Alumnos, Curso, db
import forms

@inscripciones.route("/inscripciones", methods=['GET'])
def index():
    todos_los_alumnos = Alumnos.query.all()
    return render_template("inscripciones/listadoInscripciones.html", alumnos=todos_los_alumnos)

@inscripciones.route("/inscripciones/agregar", methods=['GET', 'POST'])
def inscribir_alumno():
    form = forms.InscripcionForm(request.form)

    alumnos_db = Alumnos.query.all()
    cursos_db = Curso.query.all()
    
    form.alumno_id.choices = [(a.id, f"{a.nombre} {a.apellidos}") for a in alumnos_db]
    form.curso_id.choices = [(c.id, c.nombre) for c in cursos_db]

    if request.method == 'POST' and form.validate():
        
        alumno_seleccionado = Alumnos.query.get(form.alumno_id.data)
        curso_seleccionado = Curso.query.get(form.curso_id.data)

        if alumno_seleccionado in curso_seleccionado.alumnos:

            flash("Error: El alumno ya está inscrito en este curso.", "error")
        else:
            curso_seleccionado.alumnos.append(alumno_seleccionado)
            db.session.commit()
            
            
            return redirect(url_for('cursos.index')) 

    return render_template("inscripciones/agregar.html", form=form)
