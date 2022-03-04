from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import ninja

class Interest:
    db = 'dojos_ninjas_schema'
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.holds = []
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def select_all(cls):
        query = "SELECT * FROM interests"
        results = connectToMySQL(cls.db).query_db(query)
        print([cls(i) for i in results])
        return [cls(i) for i in results]
    
    @classmethod
    def select_one(cls, data):
        query="SELECT na.interest_id AS id, interests.name, interests.description, interests.created_at, interests.updated_at, na.id AS ninjas_interests_id, ninjas.name AS ninja, na.ninja_id, addresses.city, addresses.state FROM ninjas_interests AS na JOIN interests ON interests.id = na.interest_id JOIN ninjas ON ninjas.id = na.ninja_id JOIN addresses ON addresses.id = ninjas.address_id WHERE interests.id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        #  [{'id': 2, 'name': 'holiday cheer', 'description': 'deliver presents, sing carols, eat cookies!', 'created_at': datetime.datetime(2022, 2, 28, 22, 14, 15), 'updated_at': datetime.datetime(2022, 2, 28, 22, 14, 15), 'ninjas_interests_id': 3, 'ninja': 'xtina.codes', 'ninja_id': 13, 'city': 'Chesapeake', 'state': 'VA'}, {'id': 2, 'name': 'holiday cheer', 'description': 'deliver presents, sing carols, eat cookies!', 'created_at': datetime.datetime(2022, 2, 28, 22, 14, 15), 'updated_at': datetime.datetime(2022, 2, 28, 22, 14, 15), 'ninjas_interests_id': 4, 'ninja': 'Santa', 'ninja_id': 14, 'city': 'North Pole', 'state': 'AL'}]
        x = cls(results[0])
        for i in results:
            e = {
                "ni_id": i["ninjas_interests_id"],
                "ninja":i["ninja"],
                "ninja_id" : i["ninja_id"],
                "city" : i["city"],
                "state" : i["state"],
            }
            x.holds.append(e)
            # {'ni_id': 1, 'ninja': 'xtina.codes', 'ninja_id': 13, 'city': 'Chesapeake', 'state': 'VA'}
            # {'ni_id': 6, 'ninja': 'Grace Hopper', 'ninja_id': 16, 'city': 'Gilroy', 'state': 'CA'}
            # {'ni_id': 7, 'ninja': 'z', 'ninja_id': 18, 'city': 'z', 'state': 'zz'}
        return x
    
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
    def delete_interests_ninjas(cls, data):
        query="DELETE FROM ninjas_interests WHERE id=%(ni_id)s"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_interest(cls, data):
        query="DELETE FROM interests WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query,data)