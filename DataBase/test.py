import firebase_admin

from firebase_admin import firestore, credentials

class DatabaseHandler():
    def __init__(self, credentials_path: str = '') -> None:
        self.credentials_path = credentials_path
        self.login = credentials.Certificate(self.credentials_path)
        firebase_admin.initialize_app(self.login)

        self.db = firestore.client()

    def __repr__(self): return str(self.db) 

    def __str__(self): return str(self.db) 

    def get(self, collection_name: str = '', where_clause: str = '', auto_format: bool = True) -> list | dict:
        gathered_collection = self.db.collection(collection_name) 

        if where_clause != '':
            key, operator, value, *_ = (where_clause.split(' ')) # *(where_clause.split(''))
            query: list = gathered_collection.where(key, operator, value).get()

            if auto_format:
                query = self.format_values(query)

            return query

        return gathered_collection.get() 

    def format_values(self, value_list: list) -> list:
        formatted_values: list = [*
            map( 
                lambda x: x.to_dict(),
                value_list
            )]
        
        if len(formatted_values) == 1:
            formatted_values = formatted_values[0].to_dict()
        
        return formatted_values
    
    def write(self):
        pass
        

    


instance = DatabaseHandler('db_credentials.json')
gotten_values = instance.get('test', 'Name == Furkan a', False)
print(gotten_values)
