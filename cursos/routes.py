from . import cursos
from flask import render_template, request, redirect, url_for
from models import Curso

from models import db

import forms

@cursos.route("/cursos", methods=['GET', 'POST'])
def index():
    create_form = forms.MaestroForm(request.form)
    cursos = Curso.query.all()

    return render_template("cursos/listadoCursos.html", form=create_form, cursos=cursos)