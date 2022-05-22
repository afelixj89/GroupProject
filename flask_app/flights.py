from flask_app import app
from flask import render_template, redirect, request, session 

# Import your models
from flask_app.models import flight, carrier  # Create Flights by doing flight.Flight()


#Define our routes! 
#Route that shows all the flights on one page
@app.route("/flights")
def all_flights():
    return render_template("all_flights.html", all_flights = flight.Flight.grab_all_flights_with_carriers())

# Route that shows the new flight form
@app.route("/flights/new")
def new_flights():
    return render_template("add_flight.html", all_carriers = carrier.Carrier.grab_all_carriers())

# Route that adds flight to the database - POST 
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

# Route that shows an individual flight
@app.route("/flights/<int:id>/view")  
def view_flight_page(id):
    # Grab one flight with its carrier 
    data = {
        "id": id,
    }
    return render_template("view_flight.html", one_flight = flight.Flight.grab_one_flight_with_carrier(data))
    #grab_one_flight_with_carrier is coming from method 


# Route that DISPLAYS the edit form for a single flight 
@app.route("/flights/<int:id>/edit")
def edit_flight_page(id):
    data = {
        "id": id,
    }
    # Grab the flight with its carrier and all carriers for the dropdown menu
    return render_template("edit_flight.html", one_flight = flight.Flight.grab_one_flight_with_carrier(data), all_carriers = carrier.Carrier.grab_all_carriers())


# Route that EDITS a specific flight in the database 
# create flight = insert flight into database = POST request
@app.route("/flights/<int:id>/edit_in_db", methods=["POST"])
def edit_flight_to_database(id):
    data = {
        "number": request.form["number"],
        "starting_city": request.form["starting_city"],
        "ending_city": request.form["ending_city"],
        "carrier_id": request.form["carrier_id"], # The Carrier we want to link to this Flight
        "id": id # Need id of the Flight as well, VERY IMPORTANT 
    }
    # call on edit flight method to add the database 
    flight.Flight.edit_flight(data)
    # modelfilename.classname.classmethod_function_name(data)
    return redirect(f"/flights/{id}/view") # Always redirect with POST routes! 


# Route that deletes a flight
@app.route("/flights/<int:id>/delete")
def delete_flights(id):
    data = {
        "id": id,
    }
    flight.Flight.delete_flight(data)
    return redirect("/flights")
    
# If you have a view, edit, delete route,the number is the id of that individual item
