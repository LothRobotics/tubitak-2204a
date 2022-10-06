import firebase_admin

from firebase_admin import firestore
from firebase_admin import credentials




class DatabaseHandler():
    def __init__(self, credentials_path: str = '') -> None:
        self.credentials_path = credentials_path
        self.login = credentials.Certificate(self.credentials_path)
        firebase_admin.initialize_app(self.login)

        self.db = firestore.client()


    def __repr__(self): return str(self.db)

    def __str__(self): return str(self.db)

    def get(self, collection_name: str = '', where_clause: str = '') -> list:
        customers = self.db.collection(collection_name) 

        if where_clause != '':
            key, operator, value = (where_clause.split(' '))
            query: list = customers.where(key, operator, value).get()

            return ( 
                query
                if len(query) != 1 
                else query[0].to_dict()  
            )   

        return customers.stream() 

    
    def write(self):
        pass
        

    


instance = DatabaseHandler('db_credentials.json')
print(instance.get('test', 'Name == Furkan'))