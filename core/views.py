import logging
from socket import gaierror
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages


from core.models import Work, Comm
from core.forms import ContactForm


logging.basicConfig(filename='contact.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

try:
    from django.urls import reverse
except ImportError:  # pragma: no cover
    from django.core.urlresolvers import reverse  # pragma: no cover


def index(request):
    return render(request, 'core/index.html')


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            # from_email = form.cleaned_data['from_email']
            from_email = settings.DEFAULT_FROM_EMAIL
            body = form.cleaned_data['body']
            name = form.cleaned_data['name']

            try:
                logging.info('subject:{} body:{} from_email:{} DEFAULT_TO_EMAIL:{}', subject, body, from_email, settings.DEFAULT_TO_EMAIL)
                send_mail(subject, body, from_email, [settings.DEFAULT_TO_EMAIL], fail_silently=False)
            except BadHeaderError as bhe:
                messages.error(request, "Houston there was a problem")
                logging.exception('Exception occurred: BadHeaderError')
                return HttpResponse('Invalid header found.')
            except gaierror:
                messages.error(request, "Email server unavailable")
                logging.exception('Exception occurred: gaierror')
                # return HttpResponse('Email server is down.')
                return render(request, "core/contact.html", {'form': form})
            return redirect('success')
    return render(request, "core/contact.html", {'form': form})


def success(request):
    return render(request, "core/success.html")


class ContactPage(TemplateView):
    template_name = 'core/contact.html'

    def get(self, request):
        return render(request, self.template_name)

    # def post(self, request):


class HomePage(TemplateView):
    template_name = 'core/index.html'

    def get(self, request):
        works = Work.objects.all().order_by('title')[:4]

        args = {'works': works}
        return render(request, self.template_name, args)


class WorkList(TemplateView):
    template_name = 'core/work_list.html'

    def get(self, request):
        works = Work.objects.all().order_by('title')

        args = {'works': works}
        return render(request, self.template_name, args)


class CommList(TemplateView):
    template_name = 'core/comm_list.html'

    def get(self, request):
        comms = Comm.objects.all().order_by('title')

        args = {'comms': comms}
        return render(request, self.template_name, args)


