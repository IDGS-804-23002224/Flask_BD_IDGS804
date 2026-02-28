from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, IntegerField
from wtforms import validators

class UserForm(Form):
    id=IntegerField('id', [
        validators.NumberRange(min=1, max=20, message='valor no válido')
    ])
    nombre = StringField('nombre', [
        validators.DataRequired(message="El nombre es requerido"),
        validators.Length(min=4, max=20, message='Requiere min=4 max=20')
    ])
    apellidos = StringField("apellidos", [
        validators.DataRequired(message="El apellido es requerido")
    ])
    telefono = StringField("telefono", [
        validators.DataRequired(message="El telefono es requerido")
    ])
    email = EmailField("email", [
        validators.DataRequired(message='El email es requerido'),
        validators.Email(message="Ingresa un correo válido")
    ])

class MaestroForm(Form):
    matricula=IntegerField('matricula', [
        validators.NumberRange(min=1, max=20, message='valor no válido')
    ])
    nombre = StringField('nombre', [
        validators.DataRequired(message="El nombre es requerido"),
        validators.Length(min=4, max=20, message='Requiere min=4 max=20')
    ])
    apellidos = StringField("apellidos", [
        validators.DataRequired(message="El apellido es requerido")
    ])
    especialidad = StringField("especialidad", [
        validators.DataRequired(message="La especialidad es requerida")
    ])
    email = EmailField("email", [
        validators.DataRequired(message='El email es requerido'),
        validators.Email(message="Ingresa un correo válido")
    ])

class CursoForm(Form):
    id=IntegerField('id', [
        validators.NumberRange(min=1, max=20, message='valor no válido')
    ])
    nombre = StringField('nombre', [
        validators.DataRequired(message="El nombre es requerido"),
        validators.Length(min=4, max=20, message='Requiere min=4 max=20')
    ])
    descripcion = StringField("descripcion", [
        validators.DataRequired(message="La descripcion es requerido")
    ])
    MaestroForm.matricula=IntegerField('maestro.matricula', [
        validators.NumberRange(min=1, max=20, message='valor no válido')
    ])