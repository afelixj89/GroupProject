#the connection to your schema will be done in your models file 

from flask_app.config.mysqlconnection import connectToMySQL # Allow us to connect to MySQL
# Might need to import your app in the future:
from flask_app import app


from flask_app.models import flight 

class Carrier:
    schema_name = "carriers_schema" 
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.hq_city = data['hq_city']
        self.year_founded = data['year_founded']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.flights = [] 


    @classmethod
    def add_carrier(cls, data): 
        query = "INSERT INTO carriers (name, hq_city, year_founded) VALUES (%(name)s,%(hq_city)s,%(year_founded)s);"
        return connectToMySQL(cls.schema_name).query_db(query, data)


    @classmethod
    def grab_all_carriers(cls):
        query = "SELECT * FROM carriers;"
        results = connectToMySQL(cls.schema_name).query_db(query) 
        print(results)
        all_carriers = []
        for one_carrier in results:
            carrier_instance = cls(one_carrier) 
            all_carriers.append(carrier_instance) 
        return all_carriers 


    @classmethod
    def grab_one_carrier(cls, data): 
        query = "SELECT * FROM carriers WHERE id= %(id)s;"
        results = connectToMySQL(cls.schema_name).query_db(query, data) 
        print(results)
        if len(results)==0:
            return None 
        else: 
            return cls(results[0]) 

    @classmethod
    def grab_one_carrier_with_flights(cls, data):
        query = "SELECT * FROM carriers LEFT JOIN flights ON carriers.id = flights.carrier_id  WHERE carriers.id = %(id)s;"  #grab the data
        results = connectToMySQL(cls.schema_name).query_db(query, data) 
        print(results)
        if len(results)==0:
            return None  
        else: 
            carrier_instance = cls(results[0])
            for this_flight in results: 
                if this_flight['flights.id'] != None: 
                    flight_dictionary = {   
                        "id": this_flight["flights.id"],
                        "number": this_flight["number"],
                        "starting_city": this_flight["starting_city"],
                        "ending_city": this_flight["ending_city"],
                        "created_at": this_flight["flights.created_at"],
                        "updated_at": this_flight["flights.updated_at"],
                    }
                    flight_instance = flight.Flight(flight_dictionary)
                    carrier_instance.flights.append(flight_instance) 
            return carrier_instance 


    @classmethod 
    def edit_carrier(cls, data):
        query = "UPDATE carriers SET name=%(name)s, hq_city=%(hq_city)s, year_founded=%(year_founded)s WHERE id=%(id)s;"
        return connectToMySQL(cls.schema_name).query_db(query, data) 
        

    @classmethod
    def delete_carrier(cls, data):
        query = "DELETE FROM carriers WHERE id =%(id)s;"    
        return connectToMySQL(cls.schema_name).query_db(query, data) 
