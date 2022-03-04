from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import ninja

class Dojo:
    db = 'dojos_ninjas_schema'
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.street = data["street"]
        self.city = data["city"]
        self.state = data["state"]
        self.zip = data["zip"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.holds = []
    
    '''READ'''
    @classmethod
    def select_all(cls):
        query = "SELECT dojos.id, name, street, city, state, zip, dojos.created_at, dojos.updated_at FROM dojos JOIN addresses ON addresses.id = dojos.address_id"
        results = connectToMySQL(cls.db).query_db(query)
        return [cls(i) for i in results]
        # [<flask_app.models.dojo.Dojo object at 0x0000024C3ECD6410>, <flask_app.models.dojo.Dojo object at 0x0000024C3ECD63B0>, <flask_app.models.dojo.Dojo object at 0x0000024C3ECD5FF0>, <flask_app.models.dojo.Dojo object at 0x0000024C3ECD6050>, <flask_app.models.dojo.Dojo object at 0x0000024C3ECD5F00>, <flask_app.models.dojo.Dojo object at 0x0000024C3ECD5F60>]
    
    @classmethod
    def select_one(cls, data):
        query = "SELECT dojos.id, dojos.name, dojos.created_at, dojos.updated_at, a2.street, a2.city, a2.state, a2.zip, ninjas.name AS ninja, ninjas.id AS nid, a1.street AS nst, a1.city AS ncit, a1.state AS nsta, a1.zip AS nzip, ninjas.created_at AS ncr, ninjas.updated_at AS nup FROM ninjas JOIN addresses AS a1 ON a1.id = ninjas.address_id JOIN dojos ON dojos.id = ninjas.dojo_id JOIN addresses AS a2 ON a2.id = dojos.address_id WHERE dojos.id=%(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        # {'id': 9, 'name': 'xtina.codes', 'dojo_id': 7, 'dojo': 'Online', 'street': '1605 Cullen Ave', 'city': 'Chesapeake', 'state': 'VA', 'created_at': datetime.datetime(2022, 2, 27, 13, 47, 25), 'updated_at': datetime.datetime(2022, 2, 27, 13, 47, 25)}, {'ninja_id': 10, 'name': 'Santa', 'dojo_id': 7, 'dojo': 'Online', 'street': '3945 Reindeer Way', 'city': 'North Pole', 'state': 'AL', 'created_at': datetime.datetime(2022, 2, 27, 13, 47, 25), 'updated_at': datetime.datetime(2022, 2, 27, 13, 47, 25)}, {'ninja_id': 11, 'name': 'Stitch', 'dojo_id': 7, 'dojo': 'Online', 'street': '593 Lilo Street', 'city': 'Ocean View', 'state': 'HI', 'created_at': datetime.datetime(2022, 2, 27, 13, 47, 25), 'updated_at': datetime.datetime(2022, 2, 27, 13, 47, 25)}, {'ninja_id': 12, 'name': 'Grace Hopper', 'dojo_id': 7, 'dojo': 'Online', 'street': '92 Programming Way', 'city': 'New York', 'state': 'NY', 'created_at': datetime.datetime(2022, 2, 27, 13, 47, 25), 'updated_at': datetime.datetime(2022, 2, 27, 13, 47, 25)}
        if results:
        # if there is ninjas in the dojo
            x = cls(results[0]) # <flask_app.models.dojo.Dojo object at 0x00000209B0A78550>
            # create a class with the selected ONE dojo
            # resuts[0]
            print(x)
            for i in results:
            # use the results
            # adds each result to cls(x).holds 
                e = {
                    "id" : i ["nid"],
                    "name" : i["ninja"],
                    "dojo_id": i["id"],
                    "dojo":i["name"],
                    "created_at" : i["ncr"],
                    "updated_at" : i["nup"],
                    "street" : i["nst"],
                    "city": i["ncit"],
                    "state": i["nsta"],
                    "zip": i["nzip"]
                }
                x.holds.append(ninja.Ninja(e))
            # print(e) <flask_app.models.dojo.Dojo object at 0x000001FC8627B520>
            return x
            # return cls(results[0]) with all appended holds attributes
        else:
            return False
    
    '''CREATE'''
    @classmethod
    def insert_address(cls, data):
        query = "INSERT INTO addresses(street, city, state, zip) VALUES( %(street)s , %(city)s , %(state)s , %(zip)s );"
        return connectToMySQL(cls.db).query_db(query, data)
        # returns id

    @classmethod
    def insert_dojo(cls, data):
        query="INSERT INTO dojos(name, address_id) VALUES(%(name)s, %(address_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    '''UPDATE'''
    @classmethod
    def get_address_id(cls, data):
        query = "SELECT address_id FROM dojos JOIN addresses ON addresses.id = dojos.address_id WHERE dojos.id = %(id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        # [{'address_id': 1}]
        # result[0]["address_id"] == 1
        return result[0]["address_id"]
    
    @classmethod
    def update_address(cls, data):
        query= "UPDATE addresses SET street=%(street)s, city=%(city)s, state=%(state)s, zip=%(zip)s WHERE id = %(address_id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update_dojo(cls, data):
        query="UPDATE dojos SET name=%(name)s WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    '''DELETE'''
    @classmethod
    def delete_dojo(cls,data):
        query="DELETE FROM dojos WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)
        
