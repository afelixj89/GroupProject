from flask_app.config.mysqlconnection import connectToMySQL # Allow us to connect to MySQL
from flask_app import app # to display flash messages
# Import other models as needed:
from flask import flash
import re	
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')  
# PASSWORD REGEX = re.compile() # https://www.ocpsoft.org/tutorials/regular-expressions/password-regular-expression/
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

class User:
    schema_name = "carriers_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod 
    def register_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.schema_name).query_db(query, data)


    @classmethod 
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.schema_name).query_db(query, data)
        print(results)
        if len(results) == 0:
            return None
        else: 
            return cls(results[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.schema_name).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])



    @staticmethod 
    def validate_registration(form_data):
        is_valid = True # Assume for now everything in the form is good 
        if len(form_data['first_name']) < 2:
            is_valid = False  #if its less than 2 characters long, it's no good
            flash("First name must be atleast 2 characters.", "register") #import flash message(so import flash model)
        if len(form_data['last_name']) < 2:
            is_valid = False 
            flash("Last name must be atleast 2 characters.", "register")
        if not EMAIL_REGEX.match(form_data['email']): # if email pattern doesn't match ???@????..
            is_valid = False
            flash("Email is invalid!", "register")
        data = {
            "email": form_data["email"]
        }
        found_user_or_false = User.get_by_email(data)
        if found_user_or_false != False: 
            is_valid = False 
            flash("Email is aready registered.", "register")
        if len(form_data['password']) < 8:
            is_valid = False 
            flash("Password must be atleast 8 characters.", "register") 
        if form_data["password"] != form_data["confirm_password"]:
            is_valid = False
            flash("Passwords must agree.", "register")
        return is_valid 

    @staticmethod
    def validate_login(form_data):
        is_valid = True # Assume for now everything in the form is good 
        email_data = {
            "email": form_data["email"]
        }
        found_user_or_false = User.get_by_email(email_data)
        if found_user_or_false == False:
            is_valid = False
            flash("Invalid login credentials.", "login")
            return is_valid 
        if not bcrypt.check_password_hash(found_user_or_false.password, form_data['password']):
            is_valid = False 
            flash("Invalid login credentials.", "login")
        return is_valid
        


