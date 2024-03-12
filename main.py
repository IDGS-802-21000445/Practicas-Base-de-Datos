from flask import Flask,request,render_template,Response , redirect, jsonify, url_for
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import flash,g
from models import db
from models import Alumnos ,Maestros, Orden, Ingrediente
import forms
import datetime
from sqlalchemy import func
import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

ordenes=[]


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

datosform = forms.PizzaForm()

@app.route("/pizzas", methods=["GET", "POST"])
def pizzas():
    nombre = ''
    direccion = ''
    telefono = ''
    tamaño = ''
    pizzas = ''
    ingredientes_seleccionados = []
    SubTotal = 0
    dia = ''
    mes = ''
    fecha_seleccionada = ''
    pizza_form = forms.PizzaForm(request.form)
    global ordenes ,datosform
    

    if request.method == 'POST':
            nombre = pizza_form.nombre.data
            direccion = pizza_form.direccion.data
            telefono = pizza_form.telefono.data
            tamaño = pizza_form.tamaño.data
            pizzas = pizza_form.pizzas.data

            fecha_seleccionada = request.form['dia']
            print("FECHA ",fecha_seleccionada)
            fecha_obj = datetime.datetime.strptime(fecha_seleccionada, '%Y-%m-%d')
            print(fecha_obj)
            dia = fecha_obj.day
            mes = fecha_obj.month

            dias_semana = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
            meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

            dia_nombre = dias_semana[fecha_obj.weekday()]
            mes_nombre = meses[mes - 1] 

            if tamaño == 'Chica $40':
                SubTotal = 40 * int(pizzas)
            elif tamaño == 'Mediana $80':
                SubTotal = 80 * int(pizzas)
            elif tamaño == 'Grande $120':
                SubTotal = 120 * int(pizzas)

            costo_ingredientes = 0
            if 'jamon' in request.form:
                ingredientes_seleccionados.append('- Jamón')
                costo_ingredientes += (int(pizzas)*10)
            if 'Piña' in request.form:
                ingredientes_seleccionados.append('- Piña')
                costo_ingredientes += (int(pizzas)*10)
            if 'Champiñones' in request.form:
                ingredientes_seleccionados.append('- Champiñones')
                costo_ingredientes += (int(pizzas)*10)

            SubTotal += costo_ingredientes
            orden = {
                'id': len(ordenes) + 1,
                'nombre': nombre,
                'direccion': direccion,
                'telefono': telefono,
                'tamaño': tamaño,
                'ingredientes': ingredientes_seleccionados,
                'pizzas': pizzas,
                'dia_nombre':dia_nombre,
                'mes_nombre':mes_nombre,
                'subtotal': SubTotal
            }
            ordenes.append(orden)
            datosform = pizza_form

            with open('datos_pizzas.txt', 'a') as file:
                file.write(f"{nombre}\n")
                file.write(f"{direccion}\n")
                file.write(f"{telefono}\n")
                file.write(f"{tamaño}\n")
                for ingrediente in ingredientes_seleccionados:
                    file.write(f"{ingrediente}\n")
                file.write(f"{pizzas}\n")
                file.write(f"{dia_nombre}\n")
                file.write(f"{mes_nombre}\n")
                file.write(f"{SubTotal}\n")
                file.write('\n')

            mensaje = "Orden guardada exitosamente"
            flash(mensaje)
            if "venta_id" in request.form:
                id = int(request.form['venta_id'])

                for orden in ordenes:
                    if orden['id'] == id:
                        ordenes.remove(orden)
                        mensaje = "Orden eliminada correctamente"
                        flash(mensaje)
                        break
        
    return render_template("pizzasDominos.html", ordenes=ordenes, fecha_seleccionada=fecha_seleccionada, form=pizza_form, nombre=nombre, direccion=direccion, telefono=telefono, tamaño=tamaño, pizzas=pizzas, ingredientes_seleccionados=ingredientes_seleccionados, SubTotal=SubTotal)
@app.route("/quitar", methods=["GET", "POST"])
def quitar():
    if request.method == 'POST':
        id = int(request.form['venta_id'])

        for orden in ordenes:
            if orden['id'] == id:
                ordenes.remove(orden)
                mensaje = "Orden eliminada correctamente"
                flash(mensaje)
                break
        
    return render_template("pizzasDominos.html", ordenes=ordenes, form=datosform)

dias_semana = {
    '01': 'Lunes',
    '02': 'Martes',
    '03': 'Miercoles',
    '04': 'Jueves',
    '05': 'Viernes',
    '06': 'Sábado',
    '07': 'Domingo'
}

meses = {
    '01': 'Enero',
    '02': 'Febrero',
    '03': 'Marzo',
    '04': 'Abril',
    '05': 'Mayo',
    '06': 'Junio',
    '07': 'Julio',
    '08': 'Agosto',
    '09': 'Septiembre',
    '10': 'Octubre',
    '11': 'Noviembre',
    '12': 'Diciembre'
}

@app.route("/ventas", methods=["GET", "POST"])
def ventas():
    dia = ""
    mes = ""
    total_ventas = 0
    ventas_filtradas = []
    venta_form = forms.ventasForm(request.form)

    if request.method == 'POST' and venta_form.validate():
        dia = venta_form.dia.data
        mes = venta_form.mes.data
        
        if dia.isdigit():
            dia_texto = dias_semana.get(dia, "")
        else:
            dia_texto = dia
            
        if mes.isdigit():
            mes_texto = meses.get(mes, "")
        else:
            mes_texto = mes

        if dia_texto or mes_texto:
            query = Orden.query.with_entities(
                Orden.nombre,
                func.sum(Orden.subtotal).label('total_subtotal')
            )
            if dia_texto:
                query = query.filter(Orden.dia == dia_texto)
            elif mes_texto:
                query = query.filter(Orden.mes == mes_texto)
            
            ventas_filtradas = query.group_by(Orden.nombre).all()
            
            ventas_filtradas = [{
                'nombre': venta.nombre,
                'total_subtotal': venta.total_subtotal
            } for venta in ventas_filtradas]

            total_ventas = sum(venta['total_subtotal'] for venta in ventas_filtradas)

            mensaje = "Venta filtrada"
            flash(mensaje)

    return render_template("ventas.html", ventas=ventas_filtradas, total_ventas=total_ventas, dia=dia, mes=mes, form=venta_form)

@app.route("/confirmar_basedatos", methods=["GET", "POST"])
def confirmar_basedatos():
    if request.method == 'POST':
        nombre = request.form.get("nombre")
        direccion = request.form.get("direccion")
        telefono = request.form.get("telefono")
        tamaño = request.form.get("tamaño")
        pizzas = request.form.get("pizzas")
        dia_nombre = request.form.get("dia_nombre")
        mes_nombre = request.form.get("mes_nombre")
        SubTotal = request.form.get("subtotal")
        ingredientes_seleccionados = request.form.getlist("ingredientes")
        if "guardar" in request.form:

            for orden in ordenes:
                nombre = orden['nombre']
                direccion = orden['direccion']
                telefono = orden['telefono']
                tamaño = orden['tamaño']
                pizzas = orden['pizzas']
                dia = orden['dia_nombre']
                mes = orden['mes_nombre']
                SubTotal = orden['subtotal']
                ingredientes_seleccionados = orden['ingredientes']

                #dia = datetime.now().strftime('%A')
                #mes = datetime.now().strftime('%B')

                orden_bd = Orden(
                    nombre=nombre,
                    direccion=direccion,
                    telefono=telefono,
                    tamaño=tamaño,
                    pizzas=pizzas,
                    subtotal=SubTotal,
                    dia=dia,
                    mes=mes
                )
                db.session.add(orden_bd)
                db.session.commit()

                for ingrediente_nombre in ingredientes_seleccionados:
                    ingrediente = Ingrediente(nombre=ingrediente_nombre, orden=orden_bd)
                    db.session.add(ingrediente)
                    db.session.commit()

            mensaje = "Ordenes guardadas en la base de datos exitosamente"
            flash(mensaje)
            ordenes.clear()
            return redirect(url_for('pizzas'))
        elif "editar" in request.form:
            return render_template("pizzasDominos.html", ordenes=ordenes, form=datosform)

    return render_template("confirmacion.html", ordenes=ordenes, form=datosform)

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