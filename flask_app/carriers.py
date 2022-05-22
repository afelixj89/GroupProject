from flask_app import app
from flask import render_template, redirect, request, session 

# Import your models
from flask_app.models import carrier # Create Carries by doing carrier.Carrier()


#Define our routes! 
@app.route("/")
def index():
    return redirect("/carriers")

# Route that shows all the carriers on one page. 
@app.route("/carriers")
def all_carriers():
    # Grab all the carriers, then give it to the HTML file
    return render_template("all_carriers.html", all_carriers = carrier.Carrier.grab_all_carriers())
        # all_carriers(came from grab_all_carriers classmethod) = carrier(file).Carrier(class).grab_all_carrier(classmethod function name)

    #grab_all_carrier method is in teh carrier model 

"""
    return render_template("all_carriers.html", all_carriers = carrier.Carrier.grab_all_carriers())
        - grabs all the data from the database
        - gives it to the html doc listed below. 
    - all_carriers.html
"""


# Route that shows an individual carrier 
@app.route("/carriers/<int:id>/view")  # <int:id> = path variable - the id of the individual item
def view_carrier_page(id):
        # Dictionary needed since we need to know which carrier were grabbing - use the ID
    data = {
        "id": id,
    }
    return render_template("view_carrier.html", one_carrier = carrier.Carrier.grab_one_carrier_with_flights(data))
    # Originally carrier.Carrier.grab_one_carrier(data)


# Route that shows the new carrier form  
# showing the form /carrier/new = it is a get request 
@app.route("/carriers/new")
def new_carriers():
    return render_template("add_carrier.html")


# always redirect a POST request
# Route that adds the carrier in the database 
# create carrier = insert carrier into database = POST request
# Why do we need a data dicitonary?
    # allows you  to pass input from the user to the database; also because of security. 
    # when you make the querys, we call it the prepared statements, preventing for the most part getting deatl a sql attack injection 
@app.route("/carriers/add", methods=["POST"])
def add_carrier_to_database():
    #create a data dicitonary that holds the values from our form 
    data = {
        "name": request.form["name"],
        "hq_city": request.form["hq_city"],
        "year_founded": request.form["year_founded"],
        "total_workers": request.form["total_workers"],
    }
    carrier.Carrier.add_carrier(data)
    # modelfilename.classname.classmethod_function_name(data)
    return redirect("/carriers")
    # always redirect a POST request


# Route that DISPLAYS the edit form for a single carrier 
@app.route("/carriers/<int:id>/edit")
def edit_carrier_page(id):
    # Need to grab the carrier from the database
    data = {
        "id": id,
    }
    return render_template("edit_carrier.html", one_carrier = carrier.Carrier.grab_one_carrier(data))

# Route that EDITS a specific carrier in the database 
# create carrier = insert carrier into database = POST request
@app.route("/carriers/<int:id>/edit_in_db", methods=["POST"])
def edit_carrier_to_database(id):
    data = {
        "name": request.form["name"],
        "hq_city": request.form["hq_city"],
        "year_founded": request.form["year_founded"],
        "total_workers": request.form["total_workers"],
        "id": id # Need id of the item we're editing! VERY IMPORTANT 
    }
    carrier.Carrier.edit_carrier(data)
    # modelfilename.classname.classmethod_function_name(data)
    return redirect(f"/carriers/{id}/view") # Always redirect with POST routes! 



# Route that deletes a carrier
@app.route("/carriers/<int:id>/delete")
def delete_carriers(id):
    data = {
        "id": id,
    }
    carrier.Carrier.delete_carrier(data)
    return redirect("/carriers")

    
# If you have a view, edit, delete route,the number is the id of that individual item


