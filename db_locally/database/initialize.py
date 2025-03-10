import random, string

import database.main as db


def generate_email():
    email = ""
    characters = string.ascii_lowercase
    
    for _ in range( random.randint(8,20) ):
        index = random.randrange(0, len(characters))
        email += characters[index]
        
    email += "@example.com"
    
    return email


def load_database():
    emails : list = []
    
    #
    #   Generate noise 
    #
    for _ in range( 1000 ):
        emails.append( generate_email() )
        
    #
    #   Add known emails from wordlist
    #
    
    with open( "./wordlists/in_database.txt", "r" ) as file:
        for line in file.readlines():
            email = line.strip("\n")
            emails.append( email )
            
    #
    #   Insert emails into database.
    #
    
    db.initialize_db()
    
    db.create_tables( { 
        "Emails" : """
            CREATE TABLE Emails ( 
                id    INTEGER PRIMARY KEY AUTOINCREMENT, 
                email TEXT NOT NULL --
            );""" 
    })
    
    insert_query =  """
       INSERT INTO Emails (
           email
       ) VALUES (?);           
    """
    
    db.insert_data(
        insert_query,
        [ (email,) for email in emails ]
    )
