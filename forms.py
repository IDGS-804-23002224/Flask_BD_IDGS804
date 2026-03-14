from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, IntegerField, SelectField
from wtforms import validators

class UserForm(FlaskForm):
    id = IntegerField('id', [
        validators.Optional(), # <-- Permite que el ID venga vacío al agregar
        validators.NumberRange(min=1, message='Valor no válido')
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

class MaestroForm(FlaskForm):
    matricula = IntegerField('matricula', [
        validators.Optional(), # <-- Permite que la matrícula venga vacía si es autogenerada
        validators.NumberRange(min=1, message='Valor no válido')
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

class CursoForm(FlaskForm):
    id = IntegerField('id', [
        validators.Optional(),
        validators.NumberRange(min=1, message='Valor no válido')
    ])
    nombre = StringField('nombre', [
        validators.DataRequired(message="El nombre es requerido"),
        validators.Length(min=4, max=20, message='Requiere min=4 max=20')
    ])
    descripcion = StringField("descripcion", [
        validators.DataRequired(message="La descripcion es requerida")
    ])
    maestro_id = SelectField('Profesor Asignado', coerce=int, validators=[
        validators.DataRequired(message="El maestro es requerido")
    ])

class InscripcionForm(FlaskForm):
    id = IntegerField('ID', [validators.Optional()])
        
    alumno_id = SelectField('Seleccionar Alumno', coerce=int, validators=[
        validators.DataRequired(message="Debes seleccionar un alumno para la inscripción")
    ])
    
    curso_id = SelectField('Seleccionar Curso', coerce=int, validators=[
        validators.DataRequired(message="Debes seleccionar un curso")
    ])