from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User

from django.utils.html import strip_tags

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
    except Exception as e:
        print(f"Error sending email: {e}")
    print("(-)"*30)


def sent_account_create_email(user):
    template = 'email_templates/account_create_email_tamplates.html'
    subject = f"Account Created Successfully, {user.first_name} {user.last_name}! Welcome to Mamar Bank"
    
    html_message = render_to_string(f'{template}', {'user': user})
    email_sent(user, subject, html_message)


def sent_deposit_confirmation_email(deposit):
    template = 'email_templates/deposit_confirmation_email_template.html'
    subject = f"Deposit Successful: ${deposit.amount} - Transaction ID: {deposit.transaction_id}"
    
    html_message = render_to_string(template, {'user': deposit.user, 'deposit': deposit})
    email_sent(deposit.user, subject, html_message)

def sent_withdow_confirmation_email(withdrawal):
    template = 'email_templates/withdrow_confirmation_email_template.html'
    subject = f"Withdrawal Confirmed: ${withdrawal.amount} - Transaction ID: {withdrawal.transaction_id}"

    html_message = render_to_string(template, {'user': withdrawal.user, 'withdrawal': withdrawal})
    email_sent(withdrawal.user, subject, html_message)

def sent_sent_money_confirmation_email(sent_money):
    template = 'email_templates/sent_money_confirmation_email_template.html'
    subject = f"Confirmation: You've Sent ${sent_money.amount} to {sent_money.receiver.first_name} {sent_money.receiver.last_name}"
    
    context = {
        'user' : sent_money.user,
        'transaction' : sent_money,
        'recipient' : sent_money.receiver
    }
    html_message = render_to_string(template, context)
    email_sent(sent_money.user, subject, html_message)

    
def sent_receive_money_confirmation_email(receive_money):
    template = 'email_templates/receive_money_confirmation_email_template.html'
    subject = f"Good News {receive_money.user.first_name} {receive_money.user.last_name}, You've Received ${receive_money.amount} from {receive_money.sender.first_name} {receive_money.sender.last_name}!"
    
    context = {
        'sender' : receive_money.sender,
        'transaction' : receive_money,
        'recipient' : receive_money.receiver
    }
    html_message = render_to_string(template, context)
    email_sent(receive_money.user, subject, html_message)

def sent_loan_request_email_to_user(loan):
    template = 'email_templates/loan_request_email_template.html'
    subject = subject = f"Received {loan.purpose} Loan Request of ${loan.amount} - Mamar Bank"

    context = {
        'user' : loan.user,
        'loan' : loan
    }
    html_message = render_to_string(template, context)
    email_sent(loan.user, subject, html_message)

def sent_loan_request_email_to_admin(loan):
    template = 'email_templates/loan_request_admin_notification_email_template.html'
    subject = f'New Loan Request - {loan.amount} from {loan.user.first_name} {loan.user.last_name}'

    context = {
        'applicant' : loan.user,
        'loan' : loan
    }
    html_message = render_to_string(template, context)

    super_user = User.objects.get(is_superuser=True)
    email_sent(super_user, subject, html_message)


def sent_loan_approve_email(loan):
    template = 'email_templates/loan_request_approve_email_templates.html'
    subject = f'Approved {loan.purpose} Loan Request of ${loan.amount} - Mamar Bank'
    context = {
        'applicant' : loan.user,
        'loan' : loan
    }
    html_message = render_to_string(template, context)

    email_sent(loan.user, subject, html_message)

def sent_change_password_email(user):
    template = 'email_templates/change_password_email_templates.html'
    subject = "Password Change Confirmation - Mamar Bank"

    html_message = render_to_string(template, {'user' : user})
    email_sent(user, subject, html_message)