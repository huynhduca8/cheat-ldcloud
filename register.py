import requests
from file import read_file, write_file
from login_controler import send_email, verify_register
from mail import get_email, get_message
from encrypt import get_mid
from multiprocessing.pool import ThreadPool

session = requests.Session()
accs = read_file('acc.json')
def run(a):
    while True:
        pw = get_mid()
        email = get_email()
        if not email:
            continue
        print('%-30s' % email, "Registering")
        if send_email(session, email):
            otp = get_message(email)
            if not otp:
                print('%-30s' % email, "cant get OTP")
                continue
            print('%-30s' % email, "OTP", otp)
            acc = verify_register(session, email, pw, otp)
            if(acc):
                accs.append({
                    "email": email,
                    "password": pw
                })
                write_file("acc.json", accs)
        else:
            print('%-30s' % email, "Send message failed")
pool = ThreadPool(100)
results = pool.map(run, [0] * 50)
# print(len(accs))