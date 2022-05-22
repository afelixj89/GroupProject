from flask_app import app
from flask import render_template, redirect, request, session 

# Import your models
from flask_app.models import carrier # Create Carries by doing carrier.Carrier()


# Route that shows all the carriers on one page. - dashboard
@app.route("/carriers")
def all_carriers():
    return render_template("all_carriers.html", all_carriers = carrier.Carrier.grab_all_carriers())


# Route that shows an individual carrier 
@app.route("/carriers/<int:id>") 
def view_carrier_page(id):
    data = {
        "id": id,
    }
    return render_template("view_carrier.html", one_carrier = carrier.Carrier.grab_one_carrier_with_flights(data))


# carrier form
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


# Route that DISPLAYS the edit form for a single carrier 
@app.route("/carriers/<int:id>/edit")
def edit_carrier_page(id):
    data = {
        "id": id,
    }
    return render_template("edit_carrier.html", one_carrier = carrier.Carrier.grab_one_carrier(data))

# Route that EDITS a specific carrier in the database 
@app.route("/carriers/<int:id>/edit_in_db", methods=["POST"])
def edit_carrier_to_database(id):
    data = {
        "name": request.form["name"],
        "hq_city": request.form["hq_city"],
        "year_founded": request.form["year_founded"],
        "id": id 
    }
    carrier.Carrier.edit_carrier(data)
    return redirect(f"/carriers/{id}/view")



# Route that deletes a carrier
@app.route("/carriers/<int:id>/delete")
def delete_carriers(id):
    data = {
        "id": id,
    }
    carrier.Carrier.delete_carrier(data)
    return redirect("/carriers")




