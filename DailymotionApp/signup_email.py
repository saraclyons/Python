import smtplib, ssl


def send_email(app_config, receiver_email, passcode):
    message = """\
    Your 4 digit code is: """ + str(passcode)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(app_config["smtp_server"], app_config["port"], context=context) as server:
        server.login(app_config["sender_email"], app_config["password"])
        server.sendmail(app_config["sender_email"], receiver_email, message)


