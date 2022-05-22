from flask_app.config.mysqlconnection import connectToMySQL # Allow us to connect to MySQL

from flask_app import app
from flask_app.models import carrier # Create carreriers by doing carrier.Carrier()

class Flight:
    schema_name = "carriers_schema" # Class variable holding the name of the schema we'll use 
    def __init__(self, data):
        self.id = data['id']
        self.number = data['number']
        self.starting_city = data['starting_city']
        self.ending_city = data['ending_city']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.carrier = None  # Place holding one Carrier linked to this flight. One flight can only have one carrier.
        # We are linking this carrier to the flight here. We are linking one carrier so we are not using a list which is why we are using None 
        # Why not include carrier_id? Because we'll link Carriers in a different way 


    # Use classmethods to interact with our database - where our queries will go
        # Adding a flight 
    @classmethod
    def add_flight(cls, data): # data needed if you're passing in a data dictionary
        query = "INSERT INTO flights (number, starting_city, ending_city, carrier_id) VALUES (%(number)s,%(starting_city)s,%(ending_city)s,%(carrier_id)s);"
        return connectToMySQL(cls.schema_name).query_db(query, data)


    # Grab all flights WITH their carriers
    @classmethod 
    def grab_all_flights_with_carriers(cls):
        query = "SELECT * FROM flights JOIN carriers ON flights.carrier_id = carriers.id;" #query the data from the database 
        results = connectToMySQL(cls.schema_name).query_db(query) 
        all_flights = [] # List that will hold Flights WITH Carriers 
        for this_flight in results: 
            flight_instance = cls(this_flight) # This creates the flight instance 
            # Create the Carrier
            # Create a new data dictionary for the carrier only 
            carrier_data = {
                "id": this_flight['carriers.id'],
                "name": this_flight['name'],
                "hq_city": this_flight['hq_city'],
                "year_founded": this_flight['year_founded'],
                "total_workers": this_flight['total_workers'],
                "created_at": this_flight['carriers.created_at'],
                "updated_at": this_flight['carriers.updated_at'],
            }
            # Create the Carrier instance
            this_carrier = carrier.Carrier(carrier_data) 
            # Links teh Carrier and Flight together 
            flight_instance.carrier = this_carrier 
            all_flights.append(flight_instance) # Add to list 
        return all_flights 

    # Grab one flights WITH a carrier
    @classmethod
    def grab_one_flight_with_carrier(cls, data):
        query = "SELECT * FROM flights JOIN carriers on flights.carrier_id = carriers.id WHERE flights.id = %(id)s;"
        results = connectToMySQL(cls.schema_name).query_db(query, data) 
        if len(results)  == 0:  #No information  return none, else return data
            return None
        else: 
            this_flight = cls(results[0])
            carrier_data = {
                "id": results[0]['carriers.id'],
                "name": results[0]['name'],
                "hq_city": results[0]['hq_city'],
                "year_founded": results[0]['year_founded'],
                "total_workers": results[0]['total_workers'],
                "created_at": results[0]['carriers.created_at'],
                "updated_at": results[0]['carriers.updated_at'],
            }
            # We need results[0] here because remember results variable is a list and to get that dictionary we have to go to index 0 
            this_carrier = carrier.Carrier(carrier_data) 
            # Links teh Carrier and Flight together 
            this_flight.carrier = this_carrier 
            return this_flight

    # Edit a flight 
    @classmethod
    def edit_flight(cls, data): 
        query = "UPDATE flights SET number=%(number)s, starting_city=%(starting_city)s, ending_city=%(ending_city)s, carrier_id=%(carrier_id)s WHERE id=%(id)s;"
        return connectToMySQL(cls.schema_name).query_db(query, data) 

    # Delete a flight 
    @classmethod
    def delete_flight(cls, data):
        query = "DELETE FROM flights WHERE id =%(id)s;"
        return connectToMySQL(cls.schema_name).query_db(query, data) 
