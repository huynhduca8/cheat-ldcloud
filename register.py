import requests
from file import read_file, write_file
from login_controler import send_email, verify_register
from mail import get_email, get_message
from encrypt import get_mid
def run():
    session = requests.Session()
    accs = read_file('accounts.json')
    while True:
        pw = get_mid()
        email = get_email()
        if not email:
            continue
        print(email, "Registering")
        if send_email(session, email):
            otp = get_message(email)
            if not otp:
                print(email, "cant get OTP")
                continue
            print(email, "OTP", otp)
            if(verify_register(session, email, pw, otp)):
                accs.append({
                    "email": email,
                    "password": pw
                })
                write_file("accounts.json", accs)
run()