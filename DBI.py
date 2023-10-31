import sqlite3
from uuid import uuid4

class DataBackendInterface: 
    ''' IO for labeler applications'''


    def __init__(self) -> None:
        
        self.dbstring = 'LabelerDB.db'
    

    def create_connection(self):
        '''
        Change this function to connect to another
        database.
        '''
        con = None
        try:
            con = sqlite3.connect(self.dbstring)
        except Exception as e:
            print(e)
        return con
        
    def check_if_email_exists(self, email):
        ''' check that this email is not already in the db '''

        
        con = self.create_connection()
        cur = con.cursor()
        sqlstr = "select count(*) from users where email='{email}'".format(
            email=email.lower())
        cur.execute(sqlstr)
        cnt = cur.fetchone()[0]
        if cnt > 0:
            return True
        return False 
        

    def addUser(self, email, role=None, metadata=None):
        '''
        Add a new user to the DB. Default role is user.
        '''
        con = self.get_connection_object()
        cur = con.cursor()

        
        

        # assign defaults 
        user_id = str(uuid4())
        if role == None:
            role = "user"
        status= "active"

        sqlstr = '''insert into Users(user_id, email, role, status, metadata)
        values("{user_id}", 
                "{email}", 
                "{role}",
                "{status}",
                "{metadata}");
                '''.format(
                    user_id=user_id,
                    email=email.lower(),
                    role=role.lower(),
                    status=status.lower(),
                    metadata=metadata
                )
        
        
if __name__ == '__main__': 

    dbi = DataBackendInterface()
    x = dbi.check_if_email_exists("john.s.lewin@gmail.com")
    print(x)
    bp = True