import smtplib

def send_notification(pairs): 
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    
    # need to replace this authentication. Might just want to hard code the password since it is a dummy account
    s.login("umgcgiftpal1@gmail.com", "xhhonrpinhbfjwxx")
    
    
    # sending the mail
    for pair in pairs:
        message = """\
        Subject: New Pair

        You have been paired with """ + pair.receiver.first_name + " " + pair.receiver.last_name + """ for """ + pair.group.group_name + """!
        
        """
        s.sendmail("umgcgiftpal1@gmail.com", pair.giver.email, message)
    
    s.quit()

