from mail import Email

message = 'Hello, Microsoft tech support here, system is working correctly'

e = Email(message)
e.send_email()
