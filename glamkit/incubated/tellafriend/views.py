from django.shortcuts import render_to_response, get_object_or_404
from django.db import models
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import resolve, reverse
from pprint import pprint
from django.template.context import Context, RequestContext
from forms import TellAFriendForm
from django.template.loader import select_template
from email_utils import send_link

def tellafriend(request, theme=None, form_class=TellAFriendForm):
    """
    Takes a site URL and an optional template name to send to a friend.
    On first visit, the URL is tested for validity and a form is rendered for extra info.
    On valid form POST, the URL in question is internally processed, and we get the context used in that URL - the view needs a slight mod to be able to do this.
    The context is passed to the email template as URL_CONTEXT, so we can use extra info in the email template.
    
    TODO: rate limiting, HTML cleansing in the message, a simpler version for telling people (and us - eg reporting, voting) about model instances.
    """
    
    # Is it a valid and working URL on this site?
    try:
        url = request.REQUEST  ['url'] #check POST then GET
    except KeyError:
        raise Http404, "No URL to send"
    
    view, args, kwargs = resolve(url)
    """
    I haven't found a non-hacky way to derive the context from a view's response. I tried with django test Client, but that seems to operate on globals which interrupt the view surrounding this code.
    To substitute, every view pointed to by tellafriend should accept 'return_context_dict = True' and return just the context.
    Alternative strategies - how does debugtoolbar do it? Can we do this with a decorator?
    """
    kwargs['return_context_dict'] = True
    kwargs['request'] = request
    extra_context = view(*args, **kwargs) #may raise Http404
    
    TEMPLATE_DIR = "tellafriend"
    email_html_template = []
    email_txt_template = []
    subject_template = []
    form_template = []
    success_template = []
   
    if theme:
        SUB_TEMPLATE_DIR = TEMPLATE_DIR + "/%s" % theme
        email_html_template += ["%s/email.html" % SUB_TEMPLATE_DIR]
        email_txt_template += ["%s/email.txt" % SUB_TEMPLATE_DIR]
        subject_template += ["%s/subject.txt" % SUB_TEMPLATE_DIR]
        form_template += ["%s/form_page.html" % SUB_TEMPLATE_DIR]
        success_template += ["%s/success.html" % SUB_TEMPLATE_DIR]

    email_html_template += ["%s/email.html" % TEMPLATE_DIR]
    email_txt_template += ["%s/email.txt" % TEMPLATE_DIR]
    subject_template += ["%s/subject.txt" % TEMPLATE_DIR]
    form_template += ["%s/form_page.html" % TEMPLATE_DIR]
    success_template += ["%s/success.html" % TEMPLATE_DIR]
    
    if request.method == 'POST':      
        form = form_class(request.POST) 
        if form.is_valid():    
            
            #SEND THE EMAIL
            email_context = {
                'sender_name': form.cleaned_data['sender_name'],
                'sender_email': form.cleaned_data['sender_email'],
                'personal_message': form.cleaned_data['personal_message'],
                'recipient_name': getattr(form.cleaned_data, 'recipient_name', form.cleaned_data['recipient_email']),
                'recipient_email': form.cleaned_data['recipient_email'],
                'url': url,
                'extra_context': extra_context,
            }
            
            email_html_template = select_template(email_html_template)
            email_txt_template = select_template(email_txt_template)
            subject_template = select_template(subject_template)
            
            send_link(
                sender_name = form.cleaned_data['sender_name'],
                sender_email = form.cleaned_data['sender_email'],
                recipient_name = getattr(form.cleaned_data, 'recipient_name', form.cleaned_data['recipient_email']),
                recipient_email = form.cleaned_data['recipient_email'],    
                email_html_template = email_html_template,
                email_txt_template = email_txt_template,
                subject_template = subject_template,
                context = RequestContext(request, email_context),
            )
            
            # trying to make it redirect on success
            request.session['success_template'] = success_template
            # there's no need to make a copy really as we've finished with email_context, but put it in in case that's not always the case
            reduced_email_context = email_context.copy()
            # extra_context can't be pickled so can't save it in the session
            del reduced_email_context['extra_context'] 
            request.session['email_context'] = reduced_email_context
            return HttpResponseRedirect(reverse('message_sent'))
    else: #GET
        form = form_class(initial={'url': url })

    return render_to_response(form_template, {
        'form': form,
        'url': url,
        'extra_context': extra_context,
    }, context_instance=RequestContext(request))


def message_sent(request):
    success_template = request.session.get('success_template', None)
    email_context = request.session.get('email_context', None)
    if success_template and email_context:
        del request.session['success_template']
        del request.session['email_context']
        return render_to_response(success_template, email_context, context_instance=RequestContext(request))
    return HttpResponseRedirect('/')