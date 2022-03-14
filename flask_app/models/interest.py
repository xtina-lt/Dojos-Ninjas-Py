from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.ninja import Ninja
from flask_app.models.address import Address

class Interest:
    db = 'dojos_ninjas_schema'
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.holds = []
    
    @classmethod
    def select_all(cls):
        query = "SELECT * FROM interests"
        results = connectToMySQL(cls.db).query_db(query)
        return [cls(i) for i in results]
    
    @classmethod
    def select_one(cls, data):
        query = "SELECT * FROM ninjas_interests LEFT JOIN interests ON interests.id = ninjas_interests.interest_id LEFT JOIN ninjas ON ninjas.id = ninjas_interests.ninja_id WHERE interest_id = %(interest_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        if results: 
            interest = {
                    "id": results[0]["interest_id"],
                    "name": results[0]["name"],
                    "description": results[0]["description"]
                }
            x = cls( interest )
            print(x.id)
            print(x.name)
            print(x.description)
            for i in results:
                dictionary = {"id" : i["ninjas.id"]}
                x.holds.append( Ninja.select_one(dictionary) )
            return x
        else:
            return False
    
    @classmethod
    def select_one_ninja(cls, data):
        query = "SELECT * FROM ninjas_interests LEFT JOIN interests ON interests.id = ninjas_interests.interest_id WHERE ninja_id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        return [cls(i) for i in results]
    
    '''CREATE'''
    @classmethod
    def insert_interest(cls, data):
        query="INSERT INTO interests(name, description) VALUES(%(name)s, %(description)s)"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def insert_ninjas_interests(cls, data):
        query="INSERT INTO ninjas_interests(ninja_id, interest_id) VALUES(%(ninja_id)s, %(interest_id)s)"
        return connectToMySQL(cls.db).query_db(query, data)
    
    '''UPDATE'''
    # can only update interest
    # to update we need interest name, interest description, interest id
    @classmethod
    def update_interest(cls, data):
        query="UPDATE interests SET name=%(name)s, description=%(description)s WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    '''DELETE'''
    @classmethod
    def delete_interest_ninja(cls, data):
        query="DELETE FROM ninjas_interests WHERE ninja_id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_interest(cls, data):
        query="DELETE FROM interests WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query,data)