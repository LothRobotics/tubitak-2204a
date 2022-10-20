import time

import firebase_admin

from firebase_admin import credentials, firestore


class DatabaseHandler():

    def __init__(self, credentials_path: str) -> None:
        self.credentials_path = credentials_path
        self.login = credentials.Certificate(self.credentials_path)
        firebase_admin.initialize_app(self.login)

        self.db = firestore.client()


    def __repr__(self): return str(self.db) 

    def __str__(self): return str(self.db) 

    def get(self, collection_name: str = '', where_clauses: list [str] = [], auto_format: bool = True) -> list | dict:
        gathered_collection = self.db.collection(collection_name) 

        query = gathered_collection.get()

        if len(where_clauses) >= 1:
            for where_clause in where_clauses:
                key, operator, value, *_ = (where_clause.split(' ')) # *(where_clause.split(''))
                query: list = gathered_collection.where(key, operator, value)
                gathered_collection = query
            query = query.get()


        
        if auto_format:
            query = self.format_values(query)
        return query 

    def format_values(self, value_list: list) -> list:
        formatted_values: list = [*
            map( 
                lambda x: x.to_dict(),
                value_list
            )]
      
        return formatted_values
    
    def create(self, collection_name: str, document_name: str, document_values: dict ) -> bool:
        gathered_collection = self.db.collection(collection_name)


        assert document_values, 'Document values not defined correctly'
        assert not gathered_collection.document(document_name).get().exists, 'There is such a document in the firestore database'

        if not isinstance(document_name, str) or len(document_name) <= 1:
            return gathered_collection.add(document_values)
        else:
            return gathered_collection.document(document_name).set(document_values)

    def update(self, collection_name: str, document_name: str, replaced_document_values: dict ) -> bool:
        gathered_collection = self.db.collection(collection_name)

        assert replaced_document_values, 'Document values not defined correctly'
        assert gathered_collection.document(document_name).get().exists, 'There is not such a document in the firestore database'

        if not isinstance(document_name, str) or len(document_name) <= 1:
            return False
        else:
            return gathered_collection.document(document_name).update(replaced_document_values)

    def truncate_document(self, collection_name: str, document_name: str, delete_document_values: dict ) -> bool:
        document_ref = self.db.collection(collection_name).document(document_name)

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

    def truncate_collection(self, collection_name: str, deleted_documents: list):
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
        
db_conn = DatabaseHandler('db_credentials.json')