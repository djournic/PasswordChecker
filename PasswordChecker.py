#This is to check to see if any of our passwords have been hacked
import requests
import hashlib
import sys

class ReadFile:
    def __init__(self, path):
        self.path = path
    
    

def request_api_data(query_char):
    url = "https://api.pwnedpasswords.com/range/" + query_char #firs 5 characters of hashed password
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Could not retrieve: {res.status_code}, check API and try again')
    return res

def password_leak_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for hash, count in hashes:
        if hash == hash_to_check:
            return count
    return 0

def pwn_check(password):
    #check if password exists in the API response
    sha1_pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    #hashlib.sha1(password.encode('utf-8')).hexdigest().upper())
    first5_char, remain_char = sha1_pass[:5], sha1_pass[5:]
    response = request_api_data(first5_char)
    #print (first5_char, remain_char)
    return password_leak_count(response, remain_char)

#if you want to enter your passwords as part of the file call:
#Ex:'python PasswordChecker.py password1 password2 password3'

# def main(args):
#     for each in args:
#         count = pwn_check(each)
#         if count:
#             print (f'{each} was found {count} times')
#         else:
#             print(f'{each} was not found anywhere. All good')
#     return "Done"

#if you want to run this using a file of passwords, use this block of code:
def main():
    with open("Passwords.txt", mode= 'r') as f:
        #lines = f.readlines()
        lines = [line[:-2] for line in f.readlines() if line.strip()]
        for line in lines:
            count = pwn_check(line)
            if count:
                print (f'{line} was found {count} times')
            else:
                print(f'{line} was not found anywhere. All good')
    f.close()
    return "Done"

if __name__ == '__main__':
    #sys.exit(main(sys.argv[1:])) #This is for the first main, the one with the passwords in the call
    sys.exit(main())    #This is for the file