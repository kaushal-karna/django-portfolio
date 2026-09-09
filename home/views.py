from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string

import os
import json
import urllib.request
import urllib.error

# Import our new security validators
from .security import is_valid_email, contains_profanity

def send_brevo_email(to_email, to_name, subject, html_content):
    """Sends an email using the Brevo HTTPS REST API (Port 443)."""
    raw_api_key = getattr(settings, 'BREVO_API_KEY', None) or os.environ.get('BREVO_API_KEY', '')
    owner_email = getattr(settings, 'OWNER_EMAIL', None) or os.environ.get('OWNER_EMAIL', '')

    api_key = raw_api_key.strip().strip('"').strip("'")
    owner_email = owner_email.strip().strip('"').strip("'")

    if not api_key:
        return False

    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json",
    }
    payload = {
        "sender": {
            "name": "Kaushal Karn",
            "email": owner_email,
        },
        "to": [
            {
                "email": to_email,
                "name": to_name,
            }
        ],
        "subject": subject,
        "htmlContent": html_content,
    }

    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status in (200, 201)
    except Exception:
        return False


# ------------------------------------------------------------------
# Page Views
# ------------------------------------------------------------------

def home(request):
    return HttpResponse("Hello, World!")


def homepage(request):
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
        message_text = request.POST.get('message', '').strip()

        # 1. Required fields validation
        if not (name and email and message_text):
            messages.error(
                request,
                'All fields are required. Please complete the form.'
            )
            return redirect('contact')

        # 2. Strict Real Gmail Validation
        is_valid, error_msg = is_valid_email(email, only_gmail=True)
        if not is_valid:
            messages.error(request, f"⚠️ {error_msg}")
            return redirect('contact')

        # 3. Multilingual Vulgar / Offensive Content Filter
        combined_text = f"{name} {message_text}"
        if contains_profanity(combined_text):
            messages.error(
                request,
                "🚫 Warning: Vulgar or offensive language is strictly prohibited. "
                "Please use respectful words, or you will be permanently blocked from this portfolio."
            )
            return redirect('contact')

        # Context to pass into email templates
        email_context = {
            'name': name,
            'email': email,
            'message_text': message_text,
        }

        # 4. Render and Send Notification to You (Kaushal)
        owner_email = getattr(settings, 'OWNER_EMAIL', None) or os.environ.get('OWNER_EMAIL', '')
        admin_subject = f"📬 [Portfolio Inquiry] New message from {name}"
        admin_html = render_to_string('emails/admin_notification.html', email_context)

        send_brevo_email(
            to_email=owner_email,
            to_name="Kaushal Karn",
            subject=admin_subject,
            html_content=admin_html
        )

        # 5. Render and Send Auto-Reply to Visitor
        visitor_subject = f"✨ Thank you for reaching out, {name}!"
        visitor_html = render_to_string('emails/visitor_autoreply.html', email_context)

        send_brevo_email(
            to_email=email,
            to_name=name,
            subject=visitor_subject,
            html_content=visitor_html
        )

        messages.success(
            request,
            f"Thank you, {name}! Your message has been received successfully. I'll get back to you soon. ✉️"
        )
        return redirect('contact')

    return render(request, 'home/contact_page.html')



def blog(request):
    return render(request, 'home/blog_page.html')


def experience(request):
    return render(request, 'home/experience.html')


def certification(request):
    return render(request, 'home/certification.html')