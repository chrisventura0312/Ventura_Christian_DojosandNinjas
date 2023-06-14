from flask_app.config.mysqlconnection import connectToMySQL

class Dojo:
    def __init__(self,data): # setting up the attributes and values for each dojo
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at= data['updated_at']
        self.ninjas = []
    @classmethod
    def get_all(cls): # getting all the dojos from the database
        query = "SELECT * FROM dojos;"
        results = connectToMySQL('dojos_and_ninjas').query_db(query)
        dojos = []
        for dojo in results:
            dojos.append(cls(dojo))
        return dojos
    @classmethod
    def save(cls,data): # saving a new dojo to the database
        query = "INSERT INTO dojos (name,created_at,updated_at) VALUES (%(name)s,NOW(),NOW());"
        return connectToMySQL('dojos_and_ninjas').query_db(query,data)
    @classmethod
    def get_one(cls,data): # getting one dojo from the database
        query = "SELECT * FROM dojos WHERE id = %(id)s;"
        results = connectToMySQL('dojos_and_ninjas').query_db(query,data)
        return cls(results[0])
    @classmethod
    def update(cls,data): #adding a new dojo to the database
        query = "UPDATE dojos SET name = %(name)s,updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('dojos_and_ninjas').query_db(query,data)
    @classmethod
    def delete(cls,data): # deleting a dojo from the database
        query = "DELETE FROM dojos WHERE id = %(id)s;"
        return connectToMySQL('dojos_and_ninjas').query_db(query,data)
    @classmethod
    def get_ninjas(cls,data): # getting all the ninjas from the database
        query = "SELECT * FROM dojos LEFT JOIN ninjas ON dojos.id = ninjas.dojos_id WHERE dojos.id = %(id)s;" # this is the query to get all the ninjas from a specific dojo
        results = connectToMySQL('dojos_and_ninjas').query_db(query,data) 
        dojo = cls(results[0]) # this is the dojo that we are getting the ninjas from
        for row in results: # this is looping through all the ninjas that we got from the database
            data = {
                'id':row['ninjas.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],   # this is creating a dictionary for each ninja
                'age':row['age'],
                'dojos_id':row['dojos_id'],
                'created_at':row['ninjas.created_at'],
                'updated_at':row['ninjas.updated_at']
            }
            dojo.ninjas.append(Ninja(data)) # this is appending the ninja to the dojo
        return dojo # this is returning the dojo with all the ninjas

class Ninja:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name= data['last_name']
        self.age = data['age']
        self.dojos_id = data['dojos_id']
        self.created_at = data['created_at']
        self.updated_at= data['updated_at']
    @classmethod
    def save(cls,data): # saving a new ninja to the database
        data['dojos_id'] = data['dojo_id']
        query = "INSERT INTO ninjas (first_name,last_name,age,dojos_id,created_at,updated_at) VALUES (%(first_name)s,%(last_name)s,%(age)s,%(dojos_id)s,NOW(),NOW());"
        return connectToMySQL('dojos_and_ninjas').query_db(query,data)
    @classmethod
    def get_one(cls,data): # getting one ninja from the database
        query = "SELECT * FROM ninjas WHERE id = %(id)s;"
        results = connectToMySQL('dojos_and_ninjas').query_db(query,data)
        return cls(results[0])
    @classmethod
    def update(cls, data):
        query = "UPDATE ninjas SET first_name = %(first_name)s, last_name = %(last_name)s, age = %(age)s, dojos_id = %(dojo_id)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('dojos_and_ninjas').query_db(query, data)
    @classmethod
    def delete(cls,data): # deleting a ninja from the database
        query = "DELETE FROM ninjas WHERE id = %(id)s;"
        return connectToMySQL('dojos_and_ninjas').query_db(query,data)
    @classmethod
    def get_all(cls): # getting all the ninjas from the database
        query = "SELECT * FROM ninjas;"
        results = connectToMySQL('dojos_and_ninjas').query_db(query)
        ninjas = []
        for ninja in results:
            ninjas.append(cls(ninja))
        return ninjas
    @classmethod
    def get_ninjas(cls,data): # getting all the ninjas from a specific dojo
        query = "SELECT * FROM dojos LEFT JOIN ninjas ON dojos.id = ninjas.dojos_id WHERE dojos.id = %(id)s;"
        results = connectToMySQL('dojos_and_ninjas').query_db(query,data)
        dojo = Dojo(results[0])
        for row in results:
            data = {
                'id':row['ninjas.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'age':row['age'],
                'dojos_id':row['dojos_id'],
                'created_at':row['ninjas.created_at'],
                'updated_at':row['ninjas.updated_at']
            }
            dojo.ninjas.append(Ninja(data))
        return dojo
        
    
