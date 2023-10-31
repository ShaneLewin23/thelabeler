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
        ''' check if a user email is already in the db '''

        con = self.create_connection()
        cur = con.cursor()

        # check if there's a user in the DB
        sqlstr = "select count(*) from users where email='{email}'".format(
            email=email.lower())
        cur.execute(sqlstr)
        cnt = cur.fetchone()[0]
        con.close()

        if cnt > 0:
            return True
        return False 

    def add_user(self, email, role=None, metadata=None):
        '''
        Add a new user to the DB. Default role is user.
        '''

        # check that this user is unique
        if self.check_if_email_exists(email.lower()): 
            raise Exception("%s is already in the database"%email)
        
        con = self.create_connection()
        cur = con.cursor()

        # assign defaults 
        user_id = str(uuid4())
        if role == None:
            role = "user"
        status= "active"

        # format sql
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
        
        # load
        cur.execute(sqlstr)
        r = con.commit()
        con.close()
        return r
    
    def add_user_group(self, name):
        raise Exception(NotImplemented)
    
    def assign_user_to_group(self, email, group_name):
        raise Exception(NotImplemented)
    
    def remove_user_from_group(self, email, group_name):
        raise Exception(NotImplemented)
    
    def create_program(self, name, data, appliation, user_group, overlap, priority=None):
        raise Exception(NotImplemented)
    
    def start_program(self, program_name):
        raise Exception(NotImplemented)
    
    def pause_program(self, program_name):
        raise Exception(NotImplemented)
    
    

if __name__ == '__main__': 

    dbi = DataBackendInterface()
    x = dbi.check_if_email_exists("john.s.lewin@gmail.com")
    print(x)

    dbi.addUser("john.s.lewin@gmail.com")
    x = dbi.check_if_email_exists("john.s.lewin@gsk.com")
    print(x)
    bp = True