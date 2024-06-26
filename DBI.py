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
        TODO: this is for demo purposes only and is not secure. 
        Update this with standard scrubbing library that escapes characters properly.
        '''
        s = s.lower().strip().strip('.')
        allowed = 'abcdefghijklmnopqrstuvwxyz1234567890_@. '
        for c in s: 
            if c not in allowed:
                s.replace(c, "\%s"%c)
        return s
    
    def check_if_email_exists(self, email):

        con = self.create_connection()
        cur = con.cursor()

        # check if there's a user in the DB
        sqlstr = "select count(*) from users where email='{email}'".format(
            email=self.clean_input(email))
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
        try: 
            cur.execute(sqlstr)
            r = con.commit()
        except Exception as e:
            print(e)
            return False;

        # close 
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
        sqlstr = ''' insert into user_groups (group_id, name, status, metadata)
        values(
            "{group_id}", 
            "{name}",
            "{status}",
            "{metadata}"
            )'''.format(
            group_id=group_id,
            name=name,
            status=status,
            metadata=metadata
        )

        cur.execute(sqlstr)
        con.commit()
        con.close()
        print("successfully added group: %s"%name)
    
    def get_user_id_from_email(self, email):

        con = self.create_connection()
        cur = con.cursor()

        sqlstr = "select user_id from users where email = '{email}'".format(email=self.clean_input(email))
        cur.execute(sqlstr)
        user_id = cur.fetchone()[0]
        con.close()
        return user_id



    def assign_user_to_group(self, email, group_name):

        con = self.create_connection()
        cur = con.cursor()

        # map sql 
        assignment_id = str(uuid4())
        user_email = self.clean_input(email)
        group_name = self.clean_input(group_name)
        sqlstr = "insert into group_assignment('assignment_id', 'user_email', 'group_name', 'metadata')\
            values('{assignment_id}', '{user_email}', '{group_name}', '{metadata}')".format(
            assignment_id=assignment_id,
            user_email=user_email,
            group_name=group_name,
            metadata=None
        )

        cur.execute(sqlstr)
        con.commit()
        con.close()
        return True
    
    def remove_user_from_group(self, email, group_name):

        con = self.create_connection()
        cur = con.cursor()

        sqlstr = "delete from group_assignment where email='{email}' and group_name='{group_name}'".format(
            email=self.clean_input(email),
            group_name=self.clean_input(group_name)
        )

        cur.execute(sqlstr)
        con.commit()
        con.close()

    def get_users_in_group(self, group_name):

        con = self.create_connection()
        cur = con.cursor()
        sqlstr = "select user_email from group_assignment where group_name='{group_name}'".format(
            group_name=self.clean_input(group_name))
        
        cur.execute(sqlstr)
        data = cur.fetchall()
        con.close()
        users = []
        for row in data: 
            users.append(row[0])
        return users

    
    def create_program(self, name, data, application, user_group, overlap, priority=None):
        '''
        INPUT: 
            Overlap: in the format: x%a,y%b, which can be interpreted as x% gets a overlap and y% gets b overlap
            E.G. 75%3,25%1 would have 75% of annotations with an overlap of 3 and 25% 1 overlap
        '''
        # split out the overlap into x,y,a,b components (see input in the doc/function definition)
        olparts = overlap.split(',')
        ox = olparts[0].split('%')[0]
        oa = olparts[0].split('%')[1]
        oy = olparts[1].split('%')[0]
        ob = olparts[1].split('%')[1]

        # get all the users that will be assigned work in this application 
        users = self.get_users_in_group(user_group)

        
        # process data for the LLM SBS application
        if application == "LLM_sbs_v0.1":
            pass

        raise Exception(NotImplemented)
    
    def start_program(self, program_name):
        raise Exception(NotImplemented)
    
    def pause_program(self, program_name):
        raise Exception(NotImplemented)
    
    

if __name__ == '__main__': 

    dbi = DataBackendInterface()
    # x = dbi.check_if_email_exists("john.s.lewin@gmail.com")
    # print(x)

    # x = dbi.check_if_email_exists("john.s.lewin@gsk.com")
    # if x is False:
    #     y = dbi.add_user(email="john.s.lewin@gsk.com")
    #     print(y)

    #dbi.assign_user_to_group('john.lewin@gmail.com', "internal_test")
    # dbi.add_user_group("internal_test")
    #dbi.assign_user_to_group("john.s.lewin@gsk.com", "internal_test")
    x = dbi.get_users_in_group('internal_test')
    print(x)
    bp = True

