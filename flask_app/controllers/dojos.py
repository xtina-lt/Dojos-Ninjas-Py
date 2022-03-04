from flask import Flask, render_template, request, redirect
from flask_app import app
from flask_app.models.dojo import Dojo


'''READ'''
@app.route('/read/dojos')
def read_dojos():
    results = Dojo.select_all()
    # Dojo.update({'id':18})
    # [<flask_app.models.dojo.Dojo object at 0x0000024C3ECD6410>, <flask_app.models.dojo.Dojo object at 0x0000024C3ECD63B0>, <flask_app.models.dojo.Dojo object at 0x0000024C3ECD5FF0>, <flask_app.models.dojo.Dojo object at 0x0000024C3ECD6050>, <flask_app.models.dojo.Dojo object at 0x0000024C3ECD5F00>, <flask_app.models.dojo.Dojo object at 0x0000024C3ECD5F60>]
    return render_template("read_dojos.html", output = results)

@app.route("/read/dojo/<id>")
def read_dojo(id):
    data = {"id": id}
    print(Dojo.select_one(data))
    address_id = Dojo.get_address_id(data)
    return render_template("read_dojo.html", output=Dojo.select_one(data), address_id=address_id)

'''CREATE'''
@app.route('/process_new/dojo', methods=["POST"])
def procees_new_dojo():
    # # CAVEMAN
    # for k,v in request.form.items():
    #     if k == 'name':
    #         dojo = {k : v}
    #     else:
    #         address = {k : v}
    # dojo['name'] = test
    # address = {'street': 'test', 'city': 'test', 'state': 'test', 'zip': 'test'}

    # # SUPERWOMAN
    address={k:v for k,v in request.form.items() if k != 'name'}
    # 1) get all form information that isn't dojo name
    # 1) use the form to create a dictionary
    new = Dojo.insert_address(address)
    # 2) use address dict to insert address
    # 2) save id
    # 2) need for a foreign key to create a dojo
    data = {'name':request.form["name"]}
    data['address_id'] = new
    # 3) use form name to save as data for dojo
    # 3) add ADDRESS_ID key : NEW value from insert address 
    #    to data dictionary
    Dojo.insert_dojo(data)
    # 4)insert into dojos values(name, address_id)

    return redirect("/read/dojos")

'''UPDATE'''
@app.route("/change/dojo", methods=["POST"])
def change_dojo():
    print('change dojo')
    print('change dojo')
    print('change dojo')
    address={k:v for k,v in request.form.items() if k !="name" and k !="id"}
    print(address)
    # 1) get address info from form
    data = {"name":request.form["name"], "id":request.form["id"]}
    # 2) get dojo name and id from form
    Dojo.update_address(address)
    # 3) update address using address_id from form and inputs from form
    Dojo.update_dojo(data)
    # 4) update ninja name
    # 4) don't need to update address id,
    #       just changed it in step 3
    return redirect(f"/read/dojo/{data['id']}")

@app.route("/delete/dojo/<id>")
def delete_dojo(id):
    data={"id":id}
    Dojo.delete_dojo(data)
    return redirect("/read/dojos")