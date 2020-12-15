import smtplib

my_email = "EMAIL ADRESS"
password = "EMAIL PASSWORD"


with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
    connection.starttls()
    connection.login(user = my_email, password=password)
    connection.sendmail(
        from_addr = my_email,
        to_addrs= "RECIEVER ADRESS",
        msg = "Subject:Hello\n\nThis is the body of my email."
    )