from .EmailSent_App_Import import *

def email_sent(user, subject, html_message):
    print("(-)"*30)

    email = EmailMultiAlternatives(
        subject=subject,
        body=html_message,
        from_email='your.mamarbank@gmail.com',
        to=[user.email]
    )
    email.attach_alternative(html_message, 'text/html')

    try:
        email.send()
        print("Email sent successfully to:", user.email)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
    print("(-)"*30)
    return False



def sent_account_registration_activation_email(user):
    template = 'email_templates/account_registration_email_tamplates.html'
    subject = f"Account Registration Confirmation, {user.first_name} {user.last_name}! Welcome to NextHire"
    
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.id))
    activation_url = f"http://localhost:5173/accounts/activate/{uid}/{token}/"

    html_message = render_to_string(f'{template}', {'user': user, 'activation_url': activation_url})
    email_sent(user, subject, html_message)