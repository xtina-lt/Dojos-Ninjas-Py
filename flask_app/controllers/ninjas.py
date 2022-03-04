from flask import Flask, render_template, request, redirect
# 1) import extentions
from flask_app import app
# 2) import application
from flask_app.models.ninja import Ninja
from flask_app.models.dojo import Dojo
# 3) import models

@app.route('/')
def index():
    return render_template("index.html")


'''READ'''
@app.route('/read/ninjas')
def read_all():
    dojos = Dojo.select_all()
    # 1) select * from dojos
    results = Ninja.select_all()
    # 2) select * from ninjas
    return render_template("read_ninjas.html", output = results, dojos = dojos)

@app.route("/read/ninja/<id>")
def read_ninja(id):
# 1) take in id parameter
    data={"id": id}
    # 2) save to data dict
    output = Ninja.select_one(data)
    # 3) get info for one ninja using data dict
    elements = Ninja.get_interests(data)
    print(elements)
    # 4) get interests per ninja using data dict
    dojos = Dojo.select_all()
    # 5) select * from dojos - for update select dropdown
    address_id = Ninja.get_address_id(data)
    # 6) select address_id where ninjas.id=data
    return render_template("read_ninja.html", output = output, elements = elements, dojos = dojos, address_id = address_id)

'''CREATE'''
@app.route("/process/ninja", methods=["POST"])
def create_ninja():
    address = {k:v for k,v in request.form.items() if k != "name" and k !="dojo"}
    # address = {'address': 't', 'city': 't', 'state': 'tt', 'zip': '00000'}
    # 1) generate address information dictionary
    data = {k:v for k,v in request.form.items() if k=="name" or k=="dojo"}
    # data = {'name': 't', 'dojo': '1'}
    # 2) generate ninja data
    data["address_id"] = Ninja.insert_address(address)
    # 3) insert into addresses id value(address)
    # 3) save the address id from insert
    # 3) USE AS FOREIN KEY FOR NINJA DATA
    Ninja.insert_ninja(data)
    # 4) insert values(name, dojo_id, address_id)
    return redirect("/read/ninjas")

'''UPDATE'''
@app.route("/change/ninja", methods=["POST"])
def change_ninja():
    address = {
    # 1) get address from form
        "address_id": request.form["address_id"],
        "street": request.form["street"],
        "city": request.form["city"],
        "state": request.form["state"],
        "zip": request.form["zip"]
    }
    data={
    # 2) get ninja info from form
        "id": request.form["id"],
        "name": request.form["name"],
        "dojo": request.form["dojo"]
    }
    Ninja.update_address(address)
    # 3) address and dojo are foregn keys
    # 3) good practice to do those first
    # 3) cannot be updated at the same time
    Ninja.update_ninja(data)
    # 4) update ninjas set name, dojo_id WHERE id=data['id']
    return redirect(f"/read/ninja/{data['id']}")

'''DELETE'''
@app.route("/delete/ninja/<id>")
def delete_ninja(id):
    data={"id":id}
    # 1) get ninja id from url
    address_id = Ninja.get_address_id(data)
    # 2) obtain address id by SQL query using data from url
    # 2) select address_id from addresses where id=id
    data["address_id"] = address_id
    # 3) save address id from query to data dictionary
    # 3) data{"address_id" : Ninja.get_daddress_id()}

    Ninja.delete_address(data)
    # 4) deleteing address cascades to deleting ninja
    # 4) use data dictionary
    # 4) delete from addresses where id=id
    return redirect("/read/ninjas")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch(path):
    return render_template("catchall.html")