from wtforms import Form
from wtforms import StringField, TextAreaField, SelectField, RadioField, EmailField
from wtforms import validators
from wtforms import BooleanField 

class UserForm(Form):
    
    nombre = StringField('Nombre',[validators.DataRequired(message='Favor de ingresar el nombre'),
                                   validators.length(min=1,max=40,message='Ingresa nombre valido')
                                   ])
    apaterno = StringField('Apaterno',[validators.DataRequired(message='Favor de ingresar el nombre'),
                                   validators.length(min=1,max=40,message='Ingresa nombre valido')
                                   ])
    amaterno = StringField('materno',[validators.DataRequired(message='Favor de ingresar el nombre'),
                                   validators.length(min=1,max=40,message='Ingresa nombre valido')
                                   ])
    edad = StringField('Edad',[validators.number_range(min=1,max=20,message='Valor no valido')
                               ])
    materia  = StringField('Materia',[validators.DataRequired(message='Favor de ingresar el nombre'),
                                      validators.length(min=1,max=40,message='Ingresa nombre valido')])

class UserForm2(Form):
    id = StringField('Id',{validators.number_range(min=1,max=20,message='Valor no valido')})
    nombre = StringField('Nombre',[validators.DataRequired(message='Favor de ingresar el nombre'),
                                   validators.length(min=1,max=40,message='Ingresa nombre valido')
                                   ])
    
    apaterno = StringField('Apaterno')
    email = EmailField('correo',[validators.Email(message='Correo no valido')
                               ])
    
class PizzaForm(Form):
    nombre = StringField('Nombre',[validators.DataRequired(message='Favor de ingresar el nombre'),
                                   validators.length(min=1,max=40,message='Ingresa nombre valido')
                                   ])
    direccion = StringField('Direccion',[validators.DataRequired(message='Favor de ingresar el nombre'),
                                   validators.length(min=1,max=40,message='Ingresa nombre valido')
                                   ])
    telefono = StringField('Telefono',[validators.DataRequired(message='Favor de ingresar el nombre'),
                                   validators.length(min=1,max=40,message='Ingresa nombre valido')
                                   ])
    tamaño = RadioField('Tamaño Pizza', choices=[
        ('Chica $40', 'Chica $40'),
        ('Mediana $80', 'Mediana $80'),
        ('Grande $120', 'Grande $120')
    ])
    
    pepperoni = BooleanField('Jamon $10')
    champiñones = BooleanField('Piña $10')
    pimientos = BooleanField('Chamiñones $10')

    pizzas = StringField('Numero de Pizzas',[validators.DataRequired(message='Favor de ingresar el nombre'),
                                   validators.length(min=1,max=40,message='Ingresa nombre valido')
                                   ])
    mes = StringField('Mes',[validators.DataRequired(message='Favor de ingresar el nombre'),
                                   validators.length(min=1,max=40,message='Ingresa nombre valido')
                                   ])

class ventasForm(Form):
    mes = StringField('Mes')
    dia = StringField('Dia')