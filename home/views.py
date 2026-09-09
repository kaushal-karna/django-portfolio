from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages

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

        # 1. Required fields check
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

        # ------------------------------------------------------------------
        # 4. EMAIL NOTIFICATION TO YOU (KAUSHAL)
        # ------------------------------------------------------------------
        owner_email = getattr(settings, 'OWNER_EMAIL', None) or os.environ.get('OWNER_EMAIL', '')
        admin_subject = f"📬 [Portfolio Inquiry] New message from {name}"
        admin_html = f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
            <div style="background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%); padding: 24px; color: #ffffff;">
                <h2 style="margin: 0; font-size: 20px; font-weight: 700; letter-spacing: -0.02em;">New Contact Form Submission</h2>
                <p style="margin: 6px 0 0 0; color: #c7d2fe; font-size: 13px;">Received via Kaushal Karn's Portfolio</p>
            </div>
            
            <div style="padding: 24px; color: #1e293b; font-size: 14px; line-height: 1.6;">
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                    <tr>
                        <td style="padding: 8px 0; color: #64748b; font-weight: 600; width: 80px;">Sender:</td>
                        <td style="padding: 8px 0; color: #0f172a; font-weight: 600;">{name}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #64748b; font-weight: 600;">Email:</td>
                        <td style="padding: 8px 0;"><a href="mailto:{email}" style="color: #4f46e5; text-decoration: none; font-weight: 600;">{email}</a></td>
                    </tr>
                </table>
                
                <div style="color: #64748b; font-weight: 600; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">Message Content</div>
                <div style="background-color: #f8fafc; border-left: 4px solid #4f46e5; border-radius: 6px; padding: 16px; color: #334155; white-space: pre-wrap; font-size: 14px; line-height: 1.6;">{message_text}</div>
            </div>
            
            <div style="background-color: #f8fafc; border-top: 1px solid #e2e8f0; padding: 14px 24px; text-align: center; color: #94a3b8; font-size: 12px;">
                Direct reply will send to <a href="mailto:{email}" style="color: #6366f1; text-decoration: none;">{email}</a>
            </div>
        </div>
        """

        send_brevo_email(
            to_email=owner_email,
            to_name="Kaushal Karn",
            subject=admin_subject,
            html_content=admin_html
        )

        # ------------------------------------------------------------------
        # 5. ENHANCED BEAUTIFUL AUTO-REPLY TO VISITOR (WITH SOCIAL BADGES)
        # ------------------------------------------------------------------
        visitor_subject = f"✨ Thank you for reaching out, {name}!"
        visitor_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Thank you for reaching out</title>
        </head>
        <body style="margin: 0; padding: 24px 0; background-color: #0f172a; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased;">
          
          <table width="100%" border="0" cellspacing="0" cellpadding="0" style="table-layout: fixed;">
            <tr>
              <td align="center" style="padding: 0 16px;">
                
                <!-- Main Container Card -->
                <table width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width: 600px; background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.25), 0 10px 10px -5px rgba(0, 0, 0, 0.04);">
                  
                  <!-- Gradient Header -->
                  <tr>
                    <td style="background: linear-gradient(135deg, #4338ca 0%, #6366f1 50%, #8b5cf6 100%); padding: 40px 32px; text-align: center;">
                      <div style="display: inline-block; background: rgba(255, 255, 255, 0.18); border-radius: 50%; padding: 12px; margin-bottom: 12px;">
                        <span style="font-size: 32px; line-height: 1;">✉️</span>
                      </div>
                      <h1 style="margin: 0; color: #ffffff; font-size: 26px; font-weight: 800; letter-spacing: -0.03em;">Message Received!</h1>
                      <p style="margin: 8px 0 0 0; color: #e0e7ff; font-size: 15px; font-weight: 400;">Thank you for visiting my portfolio</p>
                    </td>
                  </tr>

                  <!-- Main Body Content -->
                  <tr>
                    <td style="padding: 36px 32px; color: #1e293b;">
                      
                      <p style="margin: 0 0 16px 0; font-size: 16px; line-height: 1.6;">
                        Hi <strong style="color: #0f172a;">{name}</strong>,
                      </p>
                      
                      <p style="margin: 0 0 24px 0; font-size: 15px; line-height: 1.6; color: #475569;">
                        Thank you for getting in touch! I have successfully received your inquiry. I review messages regularly and will get back to you as soon as possible.
                      </p>

                      <!-- Message Summary Box -->
                      <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid #6366f1; border-radius: 8px; padding: 18px 20px; margin-bottom: 30px;">
                        <div style="font-size: 11px; font-weight: 700; color: #6366f1; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;">
                          Summary of your message
                        </div>
                        <div style="color: #334155; font-size: 14px; line-height: 1.6; font-style: italic; white-space: pre-wrap;">
                          "{message_text}"
                        </div>
                      </div>

                      <!-- Social Media Connect Section -->
                      <div style="border-top: 1px solid #e2e8f0; padding-top: 28px; margin-top: 10px; text-align: center;">
                        <p style="margin: 0 0 16px 0; font-size: 13px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.06em;">
                          Let's Connect & Explore My Work
                        </p>
                        
                        <!-- Social Media Badges (Pills) -->
                        <table align="center" border="0" cellspacing="0" cellpadding="0" style="margin: 0 auto;">
                          <tr>
                            <td align="center" style="padding: 4px;">
                              <!-- GitHub -->
                              <a href="https://github.com/kaushal-karna" target="_blank" style="display: inline-block; background-color: #24292e; color: #ffffff; text-decoration: none; padding: 8px 14px; border-radius: 8px; font-size: 12px; font-weight: 600; margin: 3px;">
                                 GitHub
                              </a>
                            </td>
                            <td align="center" style="padding: 4px;">
                              <!-- LinkedIn -->
                              <a href="https://www.linkedin.com/in/kaushal-karn/" target="_blank" style="display: inline-block; background-color: #0A66C2; color: #ffffff; text-decoration: none; padding: 8px 14px; border-radius: 8px; font-size: 12px; font-weight: 600; margin: 3px;">
                                 LinkedIn
                              </a>
                            </td>
                            <td align="center" style="padding: 4px;">
                              <!-- YouTube -->
                              <a href="https://www.youtube.com/@maithili-codewala" target="_blank" style="display: inline-block; background-color: #FF0000; color: #ffffff; text-decoration: none; padding: 8px 14px; border-radius: 8px; font-size: 12px; font-weight: 600; margin: 3px;">
                                ▶ YouTube
                              </a>
                            </td>
                          </tr>
                          <tr>
                            <td align="center" style="padding: 4px;" colspan="3">
                              <!-- Instagram -->
                              <a href="https://www.instagram.com/karn_kaushal99/" target="_blank" style="display: inline-block; background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); color: #ffffff; text-decoration: none; padding: 8px 14px; border-radius: 8px; font-size: 12px; font-weight: 600; margin: 3px;">
                                📷 Instagram
                              </a>
                              <!-- Facebook -->
                              <a href="https://www.facebook.com/kaushalkarna.karna.1" target="_blank" style="display: inline-block; background-color: #1877F2; color: #ffffff; text-decoration: none; padding: 8px 14px; border-radius: 8px; font-size: 12px; font-weight: 600; margin: 3px;">
                                 Facebook
                              </a>
                            </td>
                          </tr>
                        </table>
                      </div>

                      <!-- Signature -->
                      <div style="border-top: 1px solid #e2e8f0; margin-top: 28px; padding-top: 20px;">
                        <p style="margin: 0; color: #64748b; font-size: 13px;">Warm regards,</p>
                        <p style="margin: 4px 0 0 0; color: #0f172a; font-size: 16px; font-weight: 700;">Kaushal Karn</p>
                        <p style="margin: 2px 0 0 0; color: #6366f1; font-size: 12px; font-weight: 600;">Full-Stack Developer & Software Architect</p>
                      </div>

                    </td>
                  </tr>

                  <!-- Footer -->
                  <tr>
                    <td style="background-color: #f8fafc; border-top: 1px solid #e2e8f0; padding: 20px 32px; text-align: center; color: #94a3b8; font-size: 11px; line-height: 1.5;">
                      This is an automated confirmation sent from Kaushal Karn's Portfolio.<br>
                      Please do not reply directly to this automated email.
                    </td>
                  </tr>

                </table>

              </td>
            </tr>
          </table>

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