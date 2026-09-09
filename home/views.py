import os
import json
import urllib.request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages

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

        # Validate form inputs
        if not (name and email and message_text):
            messages.error(
                request,
                'All fields are required. Please fill in the form completely.'
            )
            return render(request, 'home/contact_page.html')

        # NO DATABASE SAVING HERE - Direct email dispatch only

        # 1. Email Notification to You (Kaushal)
        owner_email = getattr(settings, 'OWNER_EMAIL', None) or os.environ.get('OWNER_EMAIL', '')
        admin_subject = f"[Kaushal-Portfolio] New message from {name}"
        admin_html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; padding: 20px; border: 1px solid #e2e8f0; border-radius: 8px;">
            <h2 style="color: #4f46e5; margin-top: 0;">New Contact Form Submission</h2>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
            <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 15px 0;">
            <p><strong>Message:</strong></p>
            <p style="white-space: pre-wrap; background: #f8fafc; padding: 14px; border-left: 4px solid #4f46e5; border-radius: 4px; color: #334155;">{message_text}</p>
        </div>
        """

        send_brevo_email(
            to_email=owner_email,
            to_name="Kaushal Karn",
            subject=admin_subject,
            html_content=admin_html
        )

        # 2. Confirmation Email to the Visitor
        visitor_subject = "[Kaushal-Portfolio] Thank you for contacting me"
        visitor_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <style>
            body {{ font-family: 'Helvetica Neue', Arial, sans-serif; background-color: #f3f4f6; margin: 0; padding: 20px; }}
            .card {{ max-width: 580px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
            .banner {{ background: linear-gradient(135deg, #4f46e5, #7c3aed); color: #ffffff; padding: 30px; text-align: center; }}
            .banner h1 {{ margin: 0; font-size: 24px; }}
            .body-content {{ padding: 25px; color: #374151; line-height: 1.6; font-size: 15px; }}
            .quote-box {{ background: #f9fafb; border-left: 4px solid #4f46e5; padding: 12px 16px; margin: 15px 0; border-radius: 4px; font-style: italic; color: #4b5563; }}
            .footer {{ background: #f9fafb; text-align: center; padding: 14px; font-size: 12px; color: #9ca3af; }}
          </style>
        </head>
        <body>
          <div class="card">
            <div class="banner">
              <h1>Message Received!</h1>
            </div>
            <div class="body-content">
              <p>Hi <strong>{name}</strong>,</p>
              <p>Thank you for contacting me through my portfolio. I have received your inquiry and will review it and get back to you as soon as possible.</p>
              
              <p style="font-size: 13px; font-weight: bold; text-transform: uppercase; color: #6b7280; letter-spacing: 0.5px;">Summary of your message:</p>
              <div class="quote-box">
                "{message_text}"
              </div>

              <p>Best regards,<br><strong>Kaushal Karn</strong><br><em>Portfolio</em></p>
            </div>
            <div class="footer">
              This is an automated confirmation from Kaushal Karn's Portfolio.
            </div>
          </div>
        </body>
        </html>
        """

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