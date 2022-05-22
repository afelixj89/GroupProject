from flask_app import app
from flask import render_template, redirect, request, session 


from flask_app.models import flight, carrier  



@app.route("/flights")
def all_flights():
    return render_template("all_flights.html", all_flights = flight.Flight.grab_all_flights_with_carriers())


@app.route("/flights/new")
def new_flights():
    return render_template("add_flight.html", all_carriers = carrier.Carrier.grab_all_carriers())


@app.route("/flights/add", methods=["POST"])
def add_flight_to_database():
    data = {
        "number": request.form["number"],
        "starting_city": request.form["starting_city"],
        "ending_city": request.form["ending_city"],
        "carrier_id": request.form["carrier_id"],
    }
    flight.Flight.add_flight(data)
    return redirect("/flights")


@app.route("/flights/<int:id>")  
def view_flight_page(id):
    data = {
        "id": id,
    }
    return render_template("view_flight.html", one_flight = flight.Flight.grab_one_flight_with_carrier(data))




@app.route("/flights/<int:id>/edit")
def edit_flight_page(id):
    data = {
        "id": id,
    }
 
    return render_template("edit_flight.html", one_flight = flight.Flight.grab_one_flight_with_carrier(data), all_carriers = carrier.Carrier.grab_all_carriers())


@app.route("/flights/<int:id>/edit_in_db", methods=["POST"])
def edit_flight_to_database(id):
    data = {
        "number": request.form["number"],
        "starting_city": request.form["starting_city"],
        "ending_city": request.form["ending_city"],
        "carrier_id": request.form["carrier_id"], 
        "id": id 
    }

    flight.Flight.edit_flight(data)
    return redirect(f"/flights/{id}/view") 


@app.route("/flights/<int:id>/delete")
def delete_flights(id):
    data = {
        "id": id,
    }
    flight.Flight.delete_flight(data)
    return redirect("/flights")
    

