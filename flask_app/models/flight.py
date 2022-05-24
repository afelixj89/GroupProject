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
        self.carrier = None  


    @classmethod
    def add_flight(cls, data):
        query = "INSERT INTO flights (number, starting_city, ending_city, carrier_id, user_id) VALUES (%(number)s,%(starting_city)s,%(ending_city)s,%(carrier_id)s,%(user_id)s);"
        return connectToMySQL(cls.schema_name).query_db(query, data)


    @classmethod 
    def grab_all_flights_with_carriers(cls):
        query = "SELECT * FROM flights JOIN carriers ON flights.carrier_id = carriers.id;" #query the data from the database 
        results = connectToMySQL(cls.schema_name).query_db(query) 
        all_flights = [] 
        for this_flight in results: 
            flight_instance = cls(this_flight) 

            carrier_data = {
                "id": this_flight['carriers.id'],
                "name": this_flight['name'],
                "hq_city": this_flight['hq_city'],
                "year_founded": this_flight['year_founded'],
                "created_at": this_flight['carriers.created_at'],
                "updated_at": this_flight['carriers.updated_at'],
            }
            this_carrier = carrier.Carrier(carrier_data) 
            flight_instance.carrier = this_carrier 
            all_flights.append(flight_instance) 
        return all_flights 


    @classmethod
    def grab_one_flight_with_carrier(cls, data):
        query = "SELECT * FROM flights JOIN carriers on flights.carrier_id = carriers.id WHERE flights.id = %(id)s;"
        results = connectToMySQL(cls.schema_name).query_db(query, data) 
        if len(results)  == 0:  
            return None
        else: 
            this_flight = cls(results[0])
            carrier_data = {
                "id": results[0]['carriers.id'],
                "name": results[0]['name'],
                "hq_city": results[0]['hq_city'],
                "year_founded": results[0]['year_founded'],
                "created_at": results[0]['carriers.created_at'],
                "updated_at": results[0]['carriers.updated_at'],
            }
            this_carrier = carrier.Carrier(carrier_data) 
            this_flight.carrier = this_carrier 
            return this_flight

    @classmethod
    def edit_flight(cls, data): 
        query = "UPDATE flights SET number=%(number)s, starting_city=%(starting_city)s, ending_city=%(ending_city)s, carrier_id=%(carrier_id)s WHERE id=%(id)s;"
        return connectToMySQL(cls.schema_name).query_db(query, data) 

    @classmethod
    def delete_flight(cls, data):
        query = "DELETE FROM flights WHERE id =%(id)s;"
        return connectToMySQL(cls.schema_name).query_db(query, data) 
