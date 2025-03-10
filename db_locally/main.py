from flask import Flask, request

import database.main as db
import database.initialize as prepare


app = Flask( __name__ )


def send_password_reset_link( email : str ): 
    import time; time.sleep( 0.2 ) # Simulate sending out an email.


#
#   Reset password if email exists in the database
#
@app.route( "/reset", methods = [ "GET" ] )
def reset():
    # reset?email=
    email = request.args.get("email")
    
    email_exists = db.query_database(
        """ SELECT EXISTS (SELECT 1 FROM Emails WHERE email = ?);""",
        (email,)
    )[ 0 ][ 0 ]
    
    if int(email_exists) == 1:    
        send_password_reset_link(email)
  
    return "If an account was registered with this email, we've sent you a password request link.", 200


#
#   Just searching for if an email exists
#
@app.route( "/search", methods = [ "GET" ] )
def search():
    # search?email=
    email = request.args.get("email")
    
    db.query_database(
        """ SELECT * From Emails WHERE email = ?;""",
        (email,)
    ) # result not used.
        
    return "Might be, might not be!", 200



if __name__ == "__main__":
    prepare.load_database()  
    app.run( host="0.0.0.0", port=5500 )