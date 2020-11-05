from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Notification,Profile


def send_priority_email(name,receiver,title,message,author,block):
    #Creating message subject and sender
    subject = title
    sender = 'kaymutor@gmail.com'

    #passing in the context variables
    text_content = render_to_string('email/priority.txt',{"name":name,"title":title,"message":message,"author":author,"block":block})
    html_content = render_to_string('email/priority.html',{"name":name,"title":title,"message":message,"author":author,"block":block})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()