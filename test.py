import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "jpiswatchingyou@gmail.com"  # Enter your address
receiver_emails = ["glenn.see.2018@sis.smu.edu.sg", "maryheng.2018@sis.smu.edu.sg", "eunice.chua.2018@sis.smu.edu.sg", "chester.ong.2018@sis.smu.edu.sg", "cliffen.lee.2018@sis.smu.edu.sg", "bxtsang.2018@sis.smu.edu.sg"]  # Enter receiver address
password = "jiapengiswatchingyou123"
message = """\
Subject: :)

Fantasma was here."""

context = ssl.create_default_context()
for email in receiver_emails:
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail("Fantasma@gmail.com", email, message)

print("done")