from flask_app import app
from flask import render_template, redirect, request
from flask_app.models.dojo_and_ninja import Dojo , Ninja

@app.route('/')
def index():
    return redirect('/dojos')

@app.route('/dojos')
def dojos():
    dojos = Dojo.get_all()
    return render_template('dojos.html',dojos=dojos)

@app.route('/dojos/create',methods=['POST'])
def create_dojo():
    Dojo.save(request.form)
    return redirect('/dojos')

@app.route('/dojos/<int:id>') #show dojo and ninjas
def show_dojo_and_ninjas(id):
    data = {
        'id':id
    }
    dojo = Dojo.get_ninjas(data)
    return render_template('dojo_info.html',dojo=dojo)

@app.route('/dojos/<int:id>/update',methods=['POST'])
def update_dojo(id):
    data = {
        'id':id,
        'name':request.form['name']
    }
    Dojo.update(data)
    return redirect('/dojos')

@app.route('/dojos/<int:id>/delete')
def delete_dojo(id):
    data = {
        'id': id
    }
    Dojo.delete(data)  # Deletes the dojo and associated ninjas
    return redirect('/dojos')

# start of ninja stuff
@app.route('/ninjas')
def ninjas():
    

    return render_template('new_ninja.html' , dojos = Dojo.get_all())

@app.route('/ninjas/create', methods=['POST'])
def create_ninja():
    ninja_data = request.form.to_dict()
    print(ninja_data)
    try:
        Ninja.save(ninja_data)
    except Exception as e:
        print(e)
    return redirect('/dojos/' + str(request.form['dojo_id']))

@app.route('/ninjas/<int:id>')
def show_ninja(id):
    data = {
        'id':id
    }
    ninja = Ninja.get_one(data)
    return render_template('ninja.html',ninja=ninja)

@app.route('/ninjas/<int:id>/edit')
def edit_ninja(id):
    data = {
        'id':id,
    }
    ninja = Ninja.get_one(data)
    return render_template('edit_ninja.html',ninja=ninja)

@app.route('/ninjas/<int:id>/update',methods=['POST'])
def update_ninja(id):
    data = {
        'id':id,
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'age':request.form['age'],
        'dojos_id':request.form['dojos_id']
    }
    Ninja.update(data)
    print(str(data))
    return redirect('/dojos/' + str(request.form['dojo_id']))


@app.route('/ninjas/<int:id>/delete')
def delete_ninja(id):
    data = {
        'id':id
    }
    referer=request.headers.get("Referer") #gets the url of the page that sent the request
    Ninja.delete(data)
    return redirect(referer)


