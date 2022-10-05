import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

creadpath = r"C:\Users\Engin ORHAN\Desktop\Tübitak\tubitak-2204a-firebase-adminsdk-ddgzc-c44c06eede.json"
login = credentials.Certificate(creadpath)
firebase_admin.initialize_app(login)

db = firestore.client()

class Commands():
    def __init__(self) -> None:
        pass

    def get():
        customers = db.collection("test").stream()

        for customer in customers:
            for customer2, var in customer.to_dict().items():
                print(customer2,":" ,var)
                print("-"*25)

            #print("{}".format(customer.to_dict()))
            #person = customer.to_dict("Special Information")


    def write(Name, Surname, Age):

        customers = db.collection("test")

        #Adding new Folder to main Collection
        customers.document(Name).set({

            #Entering the information that Folder will need
            "Age": Age,
            "Surname": Surname,
            "Name": Name,
        })

#Input for write

Name = input("Name")
Surname = input("Surname")
Age = input("Age")


r = Commands.write(Name, Surname, Age)
e = Commands.get() 
print(e)
