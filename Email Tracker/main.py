import imaplib, email, os, subprocess,time, argparse
from tkinter import *
from tkinter import messagebox

parser = argparse.ArgumentParser(description='Email Notifier')
parser.add_argument('-a', help='type of account')
parser.add_argument('-e', help='e-mail')
parser.add_argument('-p', help='password')
parser.add_argument('-r', help= 'recipients e-mail address')

args = parser.parse_args()

window = Tk()
window.eval('tk::PlaceWindow %s center'% window.winfo_toplevel())
window.withdraw()


def askAccountType():
    account = input("Do you have a gmail or a yahoo account? ")
    return account.lower()

def askEmail():
    email = input("Enter your e-mail: ")
    return email

def askPassword():
    password = input("Enter your password: ")
    return password

def askRecipientEmail():
    recipemail = input("Enter the email address of the recipient you want to track: ")
    return recipemail



# #search for a particular email
# def search(key,value,con):
#     result, data  = con.search(None,key,'"{}"'.format(value))
#     return data


def emailUpdate(account, email, password, recipemail):

    if account == 'gmail':
        imap_url = 'imap.gmail.com'
    else:
        imap_url = "imap.mail.yahoo.com"     

# sets up the auth
    con = imaplib.IMAP4_SSL(imap_url)
    con.login(email, password)
    con.select('Inbox')


    status, response = con.search(None, '(UNSEEN)', '(FROM "%s")' % (recipemail))
    unread_msg_nums = response[0].split()


    encoding = 'utf-8'
    m = b','.join(unread_msg_nums).decode(encoding)
    listofUnreadEmails = m.split(",")
    last_Email = listofUnreadEmails[-1]

    return last_Email, listofUnreadEmails


def notifier():
        global temp_last
        while True:
            last_Email, listofUnreadEmails = emailUpdate(account, email, password, recipemail)
            if last_Email != temp_last and last_Email>temp_last:
                temp_last = last_Email
                messagebox.showinfo('MESSAGE!', 'You\'ve got a message. Total unread messages:%s' %len(listofUnreadEmails))
            else:	
                print('Checking Inbox... No updates yet')
                time.sleep(5)




# if args.a == None:
    account = askAccountType()
else:
    account = args.a.lower()

if args.e == None:
    email = askEmail()
else:
    email = args.e   

if args.p == None:
    password = askPassword()
else:
    password = args.p 

if args.r == None:
    recipemail = askRecipientEmail()
else:
    recipemail = args.r            


messagebox.showinfo('','You have enabled e-mail tracking')

last_Email, listofUnreadEmails = emailUpdate(account, email, password, recipemail)
temp_last = last_Email
print (listofUnreadEmails)
print(temp_last)


notifier()


window.deiconify()
window.destroy()
window.quit()





