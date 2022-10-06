import firebase_admin

from firebase_admin import credentials, firestore


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

        query = gathered_collection.get()

        if where_clause != '':
            key, operator, value, *_ = (where_clause.split(' ')) # *(where_clause.split(''))
            query: list = gathered_collection.where(key, operator, value).get()
        
        if auto_format:
           query = self.format_values(query)
        return query 

    def format_values(self, value_list: list) -> list:
        formatted_values: list = [*
            map( 
                lambda x: x.to_dict(),
                value_list
            )]
        
        if len(formatted_values) == 1:
            formatted_values = formatted_values[0].to_dict()
        
        return formatted_values
    
    def write(self, collection_name, document_name, answer= "Y"):

        if document_name == " ":
            document_name = "default"

        informations = list()

        while answer == "Y":
            x = input("Enter the information you want\t")
            informations.append(x)

            answer = input("Do you want to add more (Y/n)\t")

        gathered_collection = self.db.collection(collection_name)

        for info in informations:

            name = str(info)
            gathered_collection.document(document_name).set({
                name: info
            })

instance = DatabaseHandler('db_credentials.json')

write = instance.write(collection_name='test', document_name='Deneme')
gotten_values = instance.get(collection_name='test', auto_format=True)
print(gotten_values)
