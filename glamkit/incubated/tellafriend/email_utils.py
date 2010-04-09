from django.template import RequestContext, loader, TemplateDoesNotExist
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.http import Http404


def send_link(sender_name, sender_email, recipient_name, recipient_email, email_html_template, email_txt_template, subject_template, context):

    sender = '"%s" <%s>' % (sender_name, sender_email)
    recipient = '"%s" <%s>' % (recipient_name, recipient_email)

    subject = subject_template.render(context)     
    
    if email_html_template and email_txt_template:
        html_body = email_html_template.render(context)
        plain_body = email_txt_template.render(context)
        msg = EmailMultiAlternatives(subject, plain_body, sender, [recipient])
        msg.attach_alternative(html_body, "text/html")
    elif email_txt_template:
        plain_body = email_txt_template.render(context)
        msg = EmailMessage(subject, plain_body, sender, [recipient])
    elif email_html_template:
        html_body = email_html_template.render(context)
        msg = EmailMessage(subject, html_body, sender, [recipient])
        msg.content_subtype = "html"
    else:
        raise Exception, 'No email template found.'
    
    msg.send()