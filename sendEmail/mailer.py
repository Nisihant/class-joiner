import smtplib
from class_joiner.settings import EMAIL_ADDRESS, EMAIL_PASSWORD

def send_mail(subject, body, emailList, html=False):
    '''send email to all the email addresses in emailList (which is a list of emails)'''
    ob = smtplib.SMTP("smtp.gmail.com", 587)
    ob.starttls()
    ob.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    message = "Subject:{}\n\n{}".format(subject, body)
    ob.sendmail(EMAIL_ADDRESS, emailList, message)
    ob.quit()

# if __name__ == "__main__":
