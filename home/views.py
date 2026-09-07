from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .models import ContactMessage


# Create your views here.

def home(request):
    # return render(request, 'home.html')
    return HttpResponse("Hello, World!")


def homepage(request):
    # return HttpResponse("Welcome to the homepage!")

    content = {
        'title': 'My Website - Kaushal Karn',
        'message': 'Welcome to the Landing Page!',
    }

    return render(request, 'home/landing_page.html', content)


def about(request):
    return render(request, 'home/about_page.html')


def contact(request):

    if request.method == 'POST':

        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        # Validate form
        if not (name and email and message):
            messages.error(
                request,
                'All fields are required. Please fill in the form completely.'
            )
            return render(request, 'home/contact_page.html')

        # 1. Save message to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )

        # --------------------------------------------------
        # 2. Email notification to site owner
        # --------------------------------------------------

        subject = f'[Kaushal-Portfolio] New message from {name}'

        body = (
            f'You received a new contact form submission.\n\n'
            f'Name:    {name}\n'
            f'Email:   {email}\n'
            f'Message:\n{message}\n\n'
            f'---\n'
            f'Sent via the portfolio contact form.'
        )

        # --------------------------------------------------
        # 3. Confirmation email to the user
        # --------------------------------------------------

        subject_reply = '[Kaushal-Portfolio] Thank you for contacting me'

        body_reply = (
            f'Hello {name},\n\n'
            f'Thank you for contacting me through my portfolio.\n\n'
            f'Your message has been received successfully. '
            f'I have received your inquiry and will get back to you '
            f'as soon as possible.\n\n'
            f'Thank you for your patience, and I look forward to '
            f'connecting with you.\n\n'
            f'Best regards,\n'
            f'Kaushal Karn\n'
            f'Portfolio'
        )

        try:

            # Send notification to site owner
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.RECIPIENT_EMAIL],
                fail_silently=False,
            )

            # Send confirmation to person who submitted the form
            send_mail(
                subject=subject_reply,
                message=body_reply,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(
                request,
                f"Thank you, {name}! Your message has been received successfully. "
                f"I'll get back to you soon. ✉️"
            )

        except Exception as exc:

            # Message is already saved in DB
            messages.warning(
                request,
                'Your message was received and saved, but there was a problem '
                'sending the email. I will still see it — thank you!'
            )

        return redirect('contact')

    return render(request, 'home/contact_page.html')


def blog(request):
    return render(request, 'home/blog_page.html')


def experience(request):
    return render(request, 'home/experience.html')


def certification(request):
    return render(request, 'home/certification.html')