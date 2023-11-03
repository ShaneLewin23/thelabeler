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
    
    def clean_input(self, s):
        '''
        TODO: this is for demo purposes only and neither secure nor useful. 
        Update this with standard scrubbing library that escapes characters properly.
        '''
        s = s.lower().strip()
        allowed = 'abcdefghijklmnopqrstuvwxyz-@. '
        for c in s: 
            if c not in allowed:
                s.replace(c, "\%s"%c)
        return s

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
        sqlstr = '''insert into users(user_id, email, role, status, metadata)
        values("{user_id}", 
                "{email}", 
                "{role}",
                "{status}",
                "{metadata}");
                '''.format(
                    user_id=user_id,
                    email=self.clean_input(email),
                    role=self.clean_input(role),
                    status=self.clean_input(status),
                    metadata=metadata
                )
        
        # load
        cur.execute(sqlstr)
        r = con.commit()
        con.close()
        return r
    
    def add_user_group(self, name):

        con = self.create_connection()
        cur = con.cursor()

        # clean inputs
        group_id = str(uuid4())
        name = self.clean_input(name)
        status = "active"
        metadata = None

        # process sqlstr
        sqlstr = ''' insert into user_groups(group_id, name, status, metadata)
        vaues("
            "{group_id}", 
            "{name}",
            "{status}",
            "{metadata}"
            )
        )'''.format(
            group_id=group_id,
            name=name,
            status = status,
            metadata = metadata
        )

        # insert
        try: 
            cur.execute(sqlstr)
            con.commit()
        except Exception as e:
            print(e)
        print("successfully added group: %s"%name)
    
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