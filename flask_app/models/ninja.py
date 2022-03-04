from flask_app.config.mysqlconnection import connectToMySQL
# 1) IMPORT CONNECTION FROM CONFIG FOLDER

class Ninja:
    db = 'dojos_ninjas_schema'
    # 1) CONSTRUCT CLASS
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.dojo_id = data["dojo_id"]
        self.dojo = data["dojo"]
        self.street = data["street"]
        self.city  = data["city"]
        self.state = data["state"]
        self.zip = data["zip"]
    
    '''READ'''
    @classmethod
    def select_all(cls):
        query = "SELECT ninjas.id, ninjas.name AS name, dojos.id AS dojo_id, dojos.name AS dojo, street, city, state, zip, ninjas.created_at, ninjas.updated_at  FROM ninjas JOIN addresses ON addresses.id = ninjas.address_id JOIN dojos ON dojos.id = ninjas.dojo_id"
        results = connectToMySQL(cls.db).query_db(query)
        return [cls(i) for i in results]
        # return a list of classes in results
        # [{'id': 13, 'name': 'xtina.codes', 'dojo_id': 1, 'dojo': 'Online', 'street': '1605 Cullen Ave', 'city': 'Chesapeake', 'state': 'VA', 'zip': 23325, 'created_at': datetime.datetime(2022, 2, 28, 22, 17, 56), 'updated_at': datetime.datetime(2022, 2, 28, 22, 17, 56)}, {'id': 14, 'name': 'Santa', 'dojo_id': 1, 'dojo': 'Online', 'street': '3945 Reindeer Way', 'city': 'North Pole', 'state': 'AL', 'zip': 99502, 'created_at': datetime.datetime(2022, 2, 28, 22, 17, 56), 'updated_at': datetime.datetime(2022, 2, 28, 22, 17, 56)}, {'id': 15, 'name': 'Stitch', 'dojo_id': 1, 'dojo': 'Online', 'street': '593 Lilo Street', 'city': 'Ocean View', 'state': 'HI', 'zip': 96737, 'created_at': datetime.datetime(2022, 2, 28, 22, 17, 56), 'updated_at': datetime.datetime(2022, 2, 28, 22, 17, 56)}, {'id': 16, 'name': 'Grace Hopper', 'dojo_id': 1, 'dojo': 'Online', 'street': '92 Programming Way', 'city': 'New York', 'state': 'NY', 'zip': 10001, 'created_at': datetime.datetime(2022, 2, 28, 22, 17, 56), 'updated_at': datetime.datetime(2022, 2, 28, 22, 17, 56)}]
    
    '''READ'''
    @classmethod
    def select_one(cls, data):
        query = "SELECT ninjas.id, ninjas.name AS name, dojos.id AS dojo_id, dojos.name AS dojo, street, city, state, zip, ninjas.created_at, ninjas.updated_at  FROM ninjas JOIN addresses ON addresses.id = ninjas.address_id JOIN dojos ON dojos.id = ninjas.dojo_id WHERE ninjas.id=%(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])
        # returns first dictionary converted to a class
        # rather than a list of dicitonaries

    @classmethod
    def get_interests(cls, data):
        query="SELECT * FROM ninjas_interests JOIN interests ON interests.id = ninjas_interests.interest_id WHERE ninja_id = %(id)s"
        return connectToMySQL(cls.db).query_db(query, data)
        # HTML : for i in elements:

    '''CREATE'''
    @classmethod
    def insert_address(cls, data):
        query = "INSERT INTO addresses(street, city, state, zip) VALUES(%(street)s, %(city)s, %(state)s, %(zip)s)"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def insert_ninja(cls, data):
        query="INSERT INTO ninjas(name, address_id, dojo_id) VALUES(%(name)s, %(address_id)s, %(dojo)s)"
        return connectToMySQL(cls.db).query_db(query, data)

    '''UPDATE'''
    @classmethod
    def get_address_id(cls, data):
        query="SELECT address_id FROM ninjas WHERE ninjas.id = %(id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result[0]['address_id']
        # return the value for 'address_id' key
        # in the first dictionary from result list
        # IN READ_NINJA.HTML
    
    @classmethod
    def update_address(cls, data):
        query="UPDATE addresses SET street=%(street)s, city=%(city)s, state=%(state)s, zip=%(zip)s WHERE id=%(address_id)s"
        return connectToMySQL(cls.db).query_db(query, data)
        # use address id from get_address_id()> send to form
        # > from form from read_ninja.html
        # returns noithing
    
    @classmethod
    def update_ninja(cls, data):
        query="UPDATE ninjas SET name=%(name)s, dojo_id=%(dojo)s WHERE id = %(id)s"
        return connectToMySQL(cls.db).query_db(query, data)
        # don't need to update address id, update for that happens in update_address()
        # from form from read_ninja.html
        # returns noithing
    
    '''DELETE'''
    # must delete forein key=addreess
    # before deleting parent=ninja
    @classmethod
    def delete_address(cls,data):
        query="DELETE FROM addresses WHERE addresses.id=%(address_id)s"
        return connectToMySQL(cls.db).query_db(query, data)