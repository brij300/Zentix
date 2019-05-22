import smtplib 
def send_message():
    gmailaddress = "birjuchaturvedi@gmail.com"
    gmailpassword = 'suprano1'
    mailto = 'brij300@gmail.com'
    msg = 'Humidity value is greater than 80% from 5 min'
    mailServer = smtplib.SMTP('smtp.gmail.com' , 587)
    mailServer.starttls()
    mailServer.login(gmailaddress , gmailpassword)
    mailServer.sendmail(gmailaddress, mailto , msg)
    print(" \n Sent!")
    mailServer.quit()