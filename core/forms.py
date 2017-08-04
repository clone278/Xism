import os
import logging
from django import forms
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.template import loader


class ContactForm(forms.Form):
    # error_messages = {
    #     'name_required': _("Name is required"),
    #     'email_required': _("Email is required"),
    #     'message_required': _("Message is required"),
    # }
    name = forms.CharField(max_length=100, label=_(u'Name'), required=True)
    email = forms.EmailField(max_length=200, label=_(u'Email'), required=True)
    subject = forms.CharField(required=True)
    body = forms.CharField(widget=forms.Textarea, label=_(u'Message'), required=True)
    from_email = settings.DEFAULT_FROM_EMAIL



class ContactForm2(forms.Form):
    """
    The base contact form class from which all contact form classes
    should inherit.

    """
    name = forms.CharField(max_length=100, label=_(u'Your name'))
    email = forms.EmailField(max_length=200, label=_(u'Your email address'))
    body = forms.CharField(widget=forms.Textarea, label=_(u'Your message'))
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [mail_tuple[1] for mail_tuple in settings.MANAGERS]

    subject_template_name = "core/contact_form_subject.txt"
    template_name = 'core/contact_form.txt'

    def __init__(self, data=None, files=None, request=None,
                 recipient_list=None, *args, **kwargs):
        if request is None:
            raise TypeError("Keyword argument 'request' must be supplied")
        self.request = request
        if recipient_list is not None:
            self.recipient_list = recipient_list
        super(ContactForm, self).__init__(data=data, files=files,
                                          *args, **kwargs)

    def message(self):
        """
        Render the body of the message to a string.

        """
        template_name = self.template_name() if \
            callable(self.template_name) \
            else self.template_name
        return loader.render_to_string(
            template_name, self.get_context(), request=self.request
        )

    def subject(self):
        """
        Render the subject of the message to a string.

        """
        template_name = self.subject_template_name() if \
            callable(self.subject_template_name) \
            else self.subject_template_name
        subject = loader.render_to_string(
            template_name, self.get_context(), request=self.request
        )
        return ''.join(subject.splitlines())

    def get_context(self):
        """
        Return the context used to render the templates for the email
        subject and body.

        By default, this context includes:

        * All of the validated values in the form, as variables of the
          same names as their fields.

        * The current ``Site`` object, as the variable ``site``.

        * Any additional variables added by context processors (this
          will be a ``RequestContext``).

        """
        if not self.is_valid():
            raise ValueError(
                "Cannot generate Context from invalid contact form"
            )
        return dict(self.cleaned_data, site=get_current_site(self.request))

    def get_message_dict(self):
        """
        Generate the various parts of the message and return them in a
        dictionary, suitable for passing directly as keyword arguments
        to ``django.core.mail.send_mail()``.

        By default, the following values are returned:

        * ``from_email``

        * ``message``

        * ``recipient_list``

        * ``subject``

        """
        if not self.is_valid():
            raise ValueError(
                "Message cannot be sent from invalid contact form"
            )
        message_dict = {}
        for message_part in ('from_email', 'message',
                             'recipient_list', 'subject'):
            attr = getattr(self, message_part)
            message_dict[message_part] = attr() if callable(attr) else attr
        return message_dict

    def save(self, fail_silently=False):
        """
        Build and send the email message.

        """
        logging.info('Sending mail...', **self.get_message_dict())
        send_mail(fail_silently=fail_silently, **self.get_message_dict())


