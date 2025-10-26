# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 
from urllib.parse import quote_plus

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, USER="aacuser", PASS="Orbit911!", HOST="localhost", PORT=27017, DB="aac", COL="animals"): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # Connection Variables 
        # 
        # USER = 'aacuser' 
        # PASS = 'Orbit911!' 
        # HOST = 'localhost' 
        # PORT = 27017 
        # DB = 'aac' 
        # COL = 'animals' 
        
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 

    # Create a method to return the next available record number for use in the create method
    def get_next_record_number(self):
        # Returns the next available record number using the document count.
        count = self.database.animals.count_documents({})
        return count + 1
            
    # Create method
    def create(self, data):
        """
        Inserts a new document.
        Returns True if successful.
        """
        if data is not None: 
            try:
                data["record_number"] = self.get_next_record_number()
                self.database.animals.insert_one(data)  # data should be dictionary    
                return True
            except Exception as e:
                print("Error inserting document:", e)
                return False
        else: 
            return False

    # Read method
    def read(self, query):
        """
        Pulls documents that match the query.
        Returns as a list, or empty if not matches.
        """
        try:
            results = self.database.animals.find(query)
            return list(results)
        except Exception as e:
            print("Error reading documents:", e)
            return []
    
    # Update method
    def update(self, query, update_data):
        """
        Updates documents that match the query.
        Returns the number of documents modified.
        """
        if query is not None and update_data is not None:
            try:
                result = self.database.animals.update_many(query, {"$set": update_data})
                return result.modified_count
            except Exception as e:
                print("Error updating documents:", e)
                return 0
        else:
            return 0
    
    # Delete method
    def delete(self, query):
        """
        Deletes documents that match the query.
        Returns the number of documents deleted.
        """
        if query is not None:
            try:
                result = self.database.animals.delete_many(query)
                return result.deleted_count
            except Exception as e:
                print("Error deleting documents:", e)
                return 0
        else:
            return 0