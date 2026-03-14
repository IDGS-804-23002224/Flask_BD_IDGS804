from . import maestros
from flask import render_template, request, redirect, url_for
from models import Maestros

from models import db

import forms

@maestros.route('/perfil/<nombre>')
def perfil(nombre):
    return f"Perfil de {nombre}"

@maestros.route("/maestros", methods=['GET', 'POST'])
def index():
    create_form = forms.MaestroForm(request.form)
    maestros = Maestros.query.all()

    return render_template("maestros/listadoMaes.html", form=create_form, maestros=maestros)

@maestros.route("/maestros/agregar", methods=['GET', 'POST'])
def maestro():
    create_form = forms.MaestroForm(request.form)

    if request.method == 'POST' and create_form.validate():
        maes = Maestros(nombre = create_form.nombre.data,
                  apellidos = create_form.apellidos.data,
                  especialidad = create_form.especialidad.data,
                  email = create_form.email.data)
        db.session.add(maes)
        db.session.commit()
        
        return redirect(url_for("maestros.index")) 
    return render_template("maestros/maestros.html", form=create_form)


#@maestros.route("/maestros", methods=['GET', 'POST'])
@maestros.route("/maestros/detalles", methods=['GET'])
def detalles():
    matricula_id = request.args.get('matricula')

    maestro_completo = db.session.query(Maestros).filter(Maestros.matricula == matricula_id).first()

    return render_template("maestros/detalles.html", maestro=maestro_completo)

#@maestros.route("/maestros", methods=['GET', 'POST'])
@maestros.route("/maestros/modificar", methods=['GET', 'POST'])
def modificar():
    create_form = forms.MaestroForm(request.form)

    if request.method == 'GET':
        matricula = request.args.get('matricula')

        maes1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()

        create_form.matricula.data = request.args.get('matricula')
        create_form.nombre.data = maes1.nombre
        create_form.apellidos.data = maes1.apellidos
        create_form.especialidad.data = maes1.especialidad
        create_form.email.data = maes1.email
    
    # CORRECCIÓN: Se agregó la validación para modificar solo si los nuevos datos son correctos
    if request.method == 'POST' and create_form.validate():
        matricula = request.args.get('matricula')
        maes1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()

        maes1.matricula = matricula
        maes1.nombre = create_form.nombre.data
        maes1.apellidos = create_form.apellidos.data
        maes1.especialidad = create_form.especialidad.data
        maes1.email = create_form.email.data
        
        db.session.add(maes1)
        db.session.commit()
        
        return redirect(url_for("maestros.index")) 
    return render_template("maestros/modificar.html", form=create_form)

#@maestros.route("/maestros", methods=['GET', 'POST'])
@maestros.route("/maestros/eliminar", methods=['GET', 'POST'])
def eliminar():
    create_form = forms.MaestroForm(request.form)

    matricula_url = request.args.get('matricula')

    if request.method == 'GET':
        maes1 = db.session.query(Maestros).filter(Maestros.matricula == matricula_url).first()

        if maes1:
            create_form.matricula.data = maes1.matricula
            create_form.nombre.data = maes1.nombre
            create_form.apellidos.data = maes1.apellidos
            create_form.especialidad.data = maes1.especialidad
            create_form.email.data = maes1.email
    
    if request.method == 'POST':
        maes1 = db.session.query(Maestros).filter(Maestros.matricula == matricula_url).first()

        if maes1:
            db.session.delete(maes1)
            db.session.commit()
        
        return redirect(url_for("maestros.index")) 
    return render_template("maestros/eliminar.html", form=create_form)

@maestros.route("/maestros/cursos", methods=['GET'])
def cursos_impartidos():
    matricula = request.args.get('matricula')
    maestro_completo = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
    
    if not maestro_completo:
        return redirect(url_for('maestros.index'))
        
    return render_template("maestros/cursos.html", maestro=maestro_completo)

@maestros.route("/maestros/listaCursos", methods=['GET', 'POST'])
def listaCursos():
    create_form = forms.MaestroForm(request.form)
    maestros = Maestros.query.all()

    return render_template("cursos/cursosMaestros.html", form=create_form, maestros=maestros)