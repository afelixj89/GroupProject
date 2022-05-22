#the connection to your schema will be done in your models file 

from flask_app.config.mysqlconnection import connectToMySQL # Allow us to connect to MySQL
# Might need to import your app in the future:
from flask_app import app

# Import other models as needed:
from flask_app.models import flight # Create Flight by doing flight.Flight()

class Carrier:
    schema_name = "carriers_schema" # Class variable holding the name of the schema we'll use 
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.hq_city = data['hq_city']
        self.year_founded = data['year_founded']
        self.total_workers = data['total_workers']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.flights = [] # Place holding Many Flights linked to this carrier. We have a list here because one carrier can hold many flights

    # Use classmethods to interact with our database - where our queries will go
    
    # Adding a carrier 
    @classmethod
    def add_carrier(cls, data): # data needed if you're passing in a data dictionary
        query = "INSERT INTO carriers (name, hq_city, year_founded, total_workers) VALUES (%(name)s,%(hq_city)s,%(year_founded)s,%(total_workers)s);"
        return connectToMySQL(cls.schema_name).query_db(query, data)

    # Show all the carriers
    @classmethod
    def grab_all_carriers(cls):
        query = "SELECT * FROM carriers;"
        results = connectToMySQL(cls.schema_name).query_db(query) # No data parameter needed - nothing needed to query
        print(results)
        # list that holds instances of the Carrier class 
        all_carriers = []
        # Loop through each dictionary
        for one_carrier in results:
            #Create the Carrier
            carrier_instance = cls(one_carrier) # Creating an instance of the class you're in. Think of cls as a palceholder of your Class.
            #carrier_instance = Carrier(one_carrier)
            all_carriers.append(carrier_instance) # Add to the list of carrier_instances 
        return all_carriers # Returning the all_carriers list back


    # Grab one carrier
    @classmethod
    def grab_one_carrier(cls, data): # Data needed - we need the ID of the specific carrier
        query = "SELECT * FROM carriers WHERE id= %(id)s;"
        results = connectToMySQL(cls.schema_name).query_db(query, data) 
        # To prevent error in case we grab a carrier that does not exist. 
        print(results)
        if len(results)==0:
            return None 
        else: 
            return cls(results[0]) # We need a zero here [0] because its the first dictionary

    # Grab one carrier WITH all it's flights
    @classmethod
    def grab_one_carrier_with_flights(cls, data):
        query = "SELECT * FROM carriers LEFT JOIN flights ON carriers.id = flights.carrier_id  WHERE carriers.id = %(id)s;"  #grab the data
        results = connectToMySQL(cls.schema_name).query_db(query, data) 
        print(results)
        if len(results)==0: # if no carrier info found return None, otherwise you will get an error message  if you have an empty list 
            return None  
        else: 
            carrier_instance = cls(results[0]) # Create the carrier, we want to make sure we have atleast one item, if your list has one item, you're always going to get something at index zero, thats why you select 0.you don't know how many items are going to be at that list.   
            # Loop through all the flights link to this carrier. 
            for this_flight in results: 
                # Run ONLY if there is at least ONE flight 
                if this_flight['flights.id'] != None: # in the webpage, if there is no flight, it will not show anything on the page. 

                # Create dictionary that holds flight info 
                # since we're joining the flights table, inside the bracket, you have to include the table_name.column name since both created_at,updated_at and id is also the same in the carriers table. 
                    flight_dictionary = {   #grab the information from flight
                        "id": this_flight["flights.id"],
                        "number": this_flight["number"],
                        "starting_city": this_flight["starting_city"],
                        "ending_city": this_flight["ending_city"],
                        "created_at": this_flight["flights.created_at"],
                        "updated_at": this_flight["flights.updated_at"],
                    }
                    # Create a Flight
                    flight_instance = flight.Flight(flight_dictionary) #create the flight
                    # Add this Flight to this carrier 
                    carrier_instance.flights.append(flight_instance) #link the flight to the carrier
            return carrier_instance # Return this Carrier 



    # Edit one carrier 
    @classmethod 
    def edit_carrier(cls, data):
        query = "UPDATE carriers SET name=%(name)s, hq_city=%(hq_city)s, year_founded=%(year_founded)s, total_workers=%(total_workers)s WHERE id=%(id)s;"
        return connectToMySQL(cls.schema_name).query_db(query, data) 
        

    # Delete a carrier 
    @classmethod
    def delete_carrier(cls, data):
        query = "DELETE FROM carriers WHERE id =%(id)s;"    
        return connectToMySQL(cls.schema_name).query_db(query, data) 
