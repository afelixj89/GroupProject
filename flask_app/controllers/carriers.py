from flask_app import app
from flask import render_template, redirect, request, session 


from flask_app.models import carrier 



@app.route("/carriers")
def all_carriers():
    return render_template("all_carriers.html", all_carriers = carrier.Carrier.grab_all_carriers())



@app.route("/carriers/<int:id>") 
def view_carrier_page(id):
    data = {
        "id": id,
    }
    return render_template("view_carrier.html", one_carrier = carrier.Carrier.grab_one_carrier_with_flights(data))



@app.route("/carriers/new")
def new_carriers():
    return render_template("add_carrier.html")


@app.route("/carriers/add", methods=["POST"])
def add_carrier_to_database():
    data = {
        "name": request.form["name"],
        "hq_city": request.form["hq_city"],
        "year_founded": request.form["year_founded"],
    }
    carrier.Carrier.add_carrier(data)
    return redirect("/carriers")



@app.route("/carriers/<int:id>/edit")
def edit_carrier_page(id):
    data = {
        "id": id,
    }
    return render_template("edit_carrier.html", one_carrier = carrier.Carrier.grab_one_carrier(data))


@app.route("/carriers/<int:id>/edit_in_db", methods=["POST"])
def edit_carrier_to_database(id):
    data = {
        "name": request.form["name"],
        "hq_city": request.form["hq_city"],
        "year_founded": request.form["year_founded"],
        "id": id 
    }
    carrier.Carrier.edit_carrier(data)
    return redirect("/carriers")



@app.route("/carriers/<int:id>/delete")
def delete_carriers(id):
    data = {
        "id": id,
    }
    carrier.Carrier.delete_carrier(data)
    return redirect("/carriers")

#Backlog: Carrier Validation