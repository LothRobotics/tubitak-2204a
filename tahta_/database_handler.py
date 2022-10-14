import firebase_admin
import datetime
from firebase_admin import credentials, firestore
from datetime import datetime
from timeit import default_timer as timer

class DatabaseHandler():
    def __init__(self, credentials_path: str) -> None:
        self.start_time = timer()
        
        self.now = datetime.now()
        self.last_operation = self.now.strftime("%d/%m/%Y %H:%M:%S")
        
        self.credentials_path = credentials_path
        self.login = credentials.Certificate(self.credentials_path)
        firebase_admin.initialize_app(self.login)

        self.db = firestore.client()
        self.connection = "Bağlantı stabil" 
            
    def __repr__(self): return str(self.db) 

    def __str__(self): return str(self.db)
    
    def update_date(self):
        self.now = datetime.now()
        self.last_operation = self.now.strftime("%d/%m/%Y %H:%M:%S")
        return self.last_operation
    
    def run_time(self):
        self.elapsed_time = timer() - self.start_time
    
        return self.elapsed_time
    def connection(self) -> str:
        return self.connection

    def get(self, collection_name: str = '', where_clause: str = '', auto_format: bool = True) -> list | dict:
        gathered_collection = self.db.collection(collection_name) 

        query = gathered_collection.get()

        if where_clause != '':
            key, operator, value, *_ = (where_clause.split(' ')) # *(where_clause.split(''))
            query: list = gathered_collection.where(key, operator, value).get()

        if auto_format:
           query = self.format_values(query)
        self.update_date()
        return query 

    def format_values(self, value_list: list) -> list:
        formatted_values: list = [*
            map( 
                lambda x: x.to_dict(),
                value_list
            )]

        if len(formatted_values) == 1:
            formatted_values = formatted_values[0].to_dict()
            
        self.update_date()
        return formatted_values

    def create(self, collection_name: str, document_name: str, document_values: dict ) -> bool:
        gathered_collection = self.db.collection(collection_name)
        self.update_date()

        assert document_values, 'Document values not defined correctly'
        assert not gathered_collection.document(document_name).get().exists, 'There is such a document in the firestore database'

        if not isinstance(document_name, str) or len(document_name) <= 1:
            return gathered_collection.add(document_values)
        else:
            return gathered_collection.document(document_name).set(document_values)

    def update(self, collection_name: str, document_name: str, replaced_document_values: dict ) -> bool:
        gathered_collection = self.db.collection(collection_name)
        self.update_date()

        assert replaced_document_values, 'Document values not defined correctly'
        assert gathered_collection.document(document_name).get().exists, 'There is not such a document in the firestore database'

        if not isinstance(document_name, str) or len(document_name) <= 1:
            return gathered_collection.add(replaced_document_values)
        else:
            return gathered_collection.document(document_name).set(replaced_document_values)

    def truncate_document(self, collection_name: str, document_name: str, delete_document_values: dict ) -> bool:
        document_ref = self.db.collection(collection_name).document(document_name)
        self.update_date()

        if not delete_document_values:
            delete_document_values = [*document_ref.get().to_dict().keys()]

        deleted_values = map(
                lambda x: document_ref.update({
                    x: firestore.DELETE_FIELD
                }), delete_document_values
            )
        return [*deleted_values]

    def delete_document(self, collection_name: str, document_name: str ) -> bool:
        self.db.collection(collection_name).document(document_name).delete()
        self.update_date()

    def truncate_collection(self, collection_name: str, deleted_documents: list):
        self.update_date()
        """Empties the collection"""
        docs: list 

        if not deleted_documents:
            docs = [document.reference for document in self.db.collection(collection_name).stream()]
        else:
            docs = [self.db.collection(collection_name).document(document_name) for document_name in deleted_documents]

        return [*
            map(
                lambda x: x.delete(),
                docs
            )
        ]

if __name__ == '__main__':
    db = DatabaseHandler('db_credentials.json')
