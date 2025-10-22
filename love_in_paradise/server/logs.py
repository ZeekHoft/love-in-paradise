import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
from dotenv import load_dotenv



try:
    load_dotenv()
    FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")

    if FIREBASE_CREDENTIALS is None:
        raise ValueError("Credentials is not found")
except Exception as e:
    print(f"Error Loading Credentials: {e}")


current_dir = os.path.dirname(os.path.abspath(__file__))



class DocumentLogs:

    def __init__(self):

        self.cred_path = os.path.join(current_dir, FIREBASE_CREDENTIALS)
        self.cred = credentials.Certificate(self.cred_path)
        #initialize firebase app if not already done
        if not firebase_admin._apps:
            firebase_admin.initialize_app(self.cred)

        #now safely create the firestore client
        self.db = firestore.client()




    def paradise_logs(self, input, valid, searches ):
        doc_ref = self.db.collection('love-in-paradise-logs').document()
        data = {
            'input': input,
            'searches': searches,
            'valid cliam': valid,
            'log id': doc_ref.id
        }
        doc_ref.set(data)

    
    def user_input(self, user_input):
        return user_input
    def valid_claim(self, valid_claim):
        return valid_claim
    def search_log(self, search_log):
        return search_log

    
# logs = DocumentLogs()
# print(logs.paradise_logs(logs.tokens()))


# firebase_admin.initialize_app(cred)


# db = firestore.client()
# doc_ref = db.collection('love-in-paradise-logs').document()

# data = {
#     'logs': 'wash hands',
#     'log id': doc_ref.id
    
# }
# doc_ref.set(data)
