from flask import Flask, render_template, redirect, request
from flask_app import app
from flask_app.models.interest import Interest
from flask_app.models.ninja import Ninja

'''READ'''
@app.route('/read/interests')
def read_interests():
    # 1) select * interests
    return render_template("read_interests.html", output = Interest.select_all())

@app.route('/read/interest/<id>')
def read_one(id):
    data={"id": id}
    # 1) get interest id from url
    output = Interest.select_one(data)
    # 2) save interest class data
    elements = Ninja.select_all()
    # 3) show all ninjas as classes for form select
    return render_template("read_interest.html", output=output, elements=elements)


'''CREATE'''
@app.route("/process/new/interest", methods=["post"])
def process_interest():
    data={k:v for k,v in request.form.items()}
    # 1) get name and descriotion frm form
    Interest.insert_interest(data)
    # 2) insert into interests(name, description) VALUES(data)
    return redirect("/read/interests")

@app.route("/process/new/ninjas_interest", methods=["POST"])
def process_ninjas_interests():
    data={k:v for k,v in request.form.items()}
    # 1) get form data values(ninja_id, interest_id)
    Interest.insert_ninjas_interests(data)
    # 2) insert into ninjas_interests values(data)
    return redirect(f"/read/interest/{data['interest_id']}")


'''UPDATE'''
@app.route("/change/interest", methods=["post"])
def change_interest():
    data={k:v for k,v in request.form.items()}
    # 1) get id, name, description from form
    Interest.update_interest(data)
    # 2) update interests values(data) where id=data['id']
    return redirect(f"/read/interest/{data['id']}")


'''DELETE'''
@app.route("/delete/ninjas_interests/<interest_id>/<ni_id>")
def delete_ninjas_interests(ni_id, interest_id):
    data={"ni_id": ni_id}
    Interest.delete_interests_ninjas(data)
    return redirect(f"/read/interest/{interest_id}")

@app.route("/delete/interest/<id>")
def delete_interest(id):
    data={"id":id}
    Interest.delete_interest(data)
    return redirect("/read/interests")