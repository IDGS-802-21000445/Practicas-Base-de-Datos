from flask import Flask,request,render_template,Response
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import flash,g
from models import db
from models import Alumnos ,Maestros
import forms

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@app.route("/index", methods=["GET","POST"])
def index():
    alum_form  =forms.UserForm2(request.form)
    
    if request.method == 'POST':
        alum = Alumnos(nombre=alum_form.nombre.data,
                   apaterno=alum_form.apaterno.data,
                   email=alum_form.email.data)
        #insert into alumnos values()
        db.session.add(alum)
        db.session.commit()
    return render_template("index.html",form=alum_form)

@app.route("/maestro", methods=["GET","POST"])
def maestro():
    maestro_form  =forms.UserForm(request.form)
    
    if request.method == 'POST':
        maestro = Maestros(nombre=maestro_form.nombre.data,
                   apaterno=maestro_form.apaterno.data,
                   amaterno=maestro_form.amaterno.data,
                   edad=maestro_form.edad.data,
                   materia=maestro_form.materia.data)
        #insert into alumnos values()
        db.session.add(maestro)
        db.session.commit()
    return render_template("maestro.html",form=maestro_form)

@app.route("/ABC_Completo", methods=["GET","POST"])
def ABCompleto():
    alum_form  =forms.UserForm2(request.form)
    alumno=Alumnos.query.all()


    return render_template("/ABC_Completo.html",alumno=alumno)

@app.route("/ABC_Maestro", methods=["GET","POST"])
def ABCompletoMaestro():
    alum_form  =forms.UserForm(request.form)
    maestros=Maestros.query.all()


    return render_template("/ABC_Maestro.html",maestros=maestros)

@app.route("/alumnos", methods=["GET","POST"])
def alumnos():
    nom =''
    apa=''
    ama=''
    alum_form  =forms.UserForm(request.form)
    if request.method == 'POST':
        nom=alum_form.nombre.data
        apa=alum_form.apaterno.data
        ama=alum_form.amaterno.data
        mensaje = "Bienvenido {}".format(nom)
        flash(mensaje)
        print("nombre: {}".format(nom))
        print("apterno: {}".format(apa))
        print("amaterno: {}".format(ama))
            
#archivo_texto.write('\n datos en el archivo')
    return render_template("alumnos.html", form=alum_form,nom=nom,apa=apa,ama=ama)

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()