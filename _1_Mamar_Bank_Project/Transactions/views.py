from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from Accounts.models import UserBankAccount
from .models import Transaction, Loan, B2B
from datetime import datetime, timedelta
from decimal import Decimal
from . import sent_email
    
def home(request):
    return render(request, 'home.html')

def deposit(request):
    context = {}
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        print(amount, description)

        if Decimal(amount) > 0.0:
            request.user.account.balance += Decimal(amount)
            request.user.account.save()
            Deposit = Transaction.objects.create(
                user=request.user,
                transaction_type='Deposit',
                amount=amount, description=description, status=1,
                after_transaction_balance=request.user.account.balance
            )
            Deposit.save()
            sent_email.sent_deposit_confirmation_email(Deposit)
            return redirect('report')
        
        context['error_msg'] = "Invalid amount"

    return render(request, 'deposit.html', context)

def withdrow(request):
    context = {}
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        print(amount, description)

        context['error_msg'] = "Invalid amount"
        if Decimal(amount) > 0.0:
            if request.user.account.balance >= Decimal(amount):
                request.user.account.balance -= Decimal(amount)
                request.user.account.save()
                Withdrawal = Transaction.objects.create(
                    user=request.user,
                    transaction_type='Withdrow',
                    amount=amount, description=description, status=1,
                    after_transaction_balance=request.user.account.balance
                )
                Withdrawal.save()
                sent_email.sent_withdow_confirmation_email(Withdrawal)
                return redirect('report')
            
            context['error_msg'] = "Insufficient balance"
        
    return render(request, 'withdrow.html', context)

def sent_money(request):
    context = {}
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        recipient = request.POST['recipient']
        print(amount, description, recipient)

        context['error_msg'] = "Invalid amount"
        if Decimal(amount) > 0.0:

            context['error_msg'] = "Insufficient balance"
            if request.user.account.balance >= Decimal(amount):

                context['error_msg'] = "Account not found."
                if recipient.isdigit() and UserBankAccount.objects.filter(account_no=int(recipient)).exists():
                    ReceiverUser = UserBankAccount.objects.get(account_no=int(recipient)).user

                    context['error_msg'] = "You cannot transfer money to your account."
                    if ReceiverUser != request.user:
                        request.user.account.balance -= Decimal(amount)
                        ReceiverUser.account.balance += Decimal(amount)
                        request.user.account.save()
                        ReceiverUser.account.save()

                        SentMoney = B2B.objects.create(
                            user=request.user,
                            sender=request.user, receiver=ReceiverUser,
                            transaction_type='Sent Money',
                            amount=amount, description=description, status=1,
                            after_transaction_balance=request.user.account.balance
                        )
                        SentMoney.save()

                        ReceiveMoney = B2B.objects.create(
                            user=ReceiverUser,
                            sender=request.user, receiver=ReceiverUser,
                            transaction_type='Receive Money',
                            transaction_id=SentMoney.transaction_id,
                            amount=amount, description=description, status=1,
                            after_transaction_balance=ReceiverUser.account.balance
                        )
                        ReceiveMoney.save()

                        sent_email.sent_sent_money_confirmation_email(SentMoney)
                        sent_email.sent_receive_money_confirmation_email(ReceiveMoney)
                        return redirect('report')
    return render(request, 'sent_money.html', context)

def loan(request):
    context = {}
    if request.method == 'POST':
        amount = request.POST['amount']
        purpose = request.POST['purpose']
        priority = request.POST['priority']
        repayment_frequency = request.POST['repayment_frequency']

        if Decimal(amount) > 0.0:
            print(amount, purpose, priority, repayment_frequency)
            loan = Loan.objects.create(
                user=request.user, amount=amount, purpose=purpose,
                transaction_type='Loan',
                priority=priority,
                repayment_frequency=repayment_frequency,
            )
            loan.save()

            sent_email.sent_loan_request_email_to_user(loan)
            sent_email.sent_loan_request_email_to_admin(loan)
            return redirect('report')
            
        context['error_msg'] = "Invalid amount"
    
    loan = Loan.objects.filter(user=request.user).order_by('-id')
    context['transactions'] = loan
    return render(request, 'loan.html', context)

def loan_request(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    loan_request = Loan.objects.filter(transaction_type='Loan', status=False)

    context = {
        'loan_request': loan_request,
    }
    return render(request, 'loan_request.html', context)

def approve_loan(request, loan_id):
    if not request.user.is_superuser:
        return redirect('home')
    
    loan = Loan.objects.get(id=loan_id)
    loan.status = True
    loan.approve_admin = request.user
    loan.user.account.balance += loan.amount
    loan.after_transaction_balance = loan.user.account.balance
    loan.user.account.save()
    loan.save()
    
    sent_email.sent_loan_approve_email(loan)
    return redirect('loan_request')

def report(request):
    if not request.user.is_authenticated:
        return redirect('home') 
    
    if request.method == 'POST':
        # Get start_date and end_date from POST data
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if start_date and end_date:
            # Convert start_date and end_date to datetime objects
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

            # Add 1 day to end_date for inclusive filtering
            end_date_obj += timedelta(days=1)

            # Filter transactions
            Transactions = request.user.transactions.filter(
                created_at__range=[start_date_obj, end_date_obj]).order_by('-id')

            context = {
                'transactions': Transactions,
            }
            return render(request, 'report.html', context)
            
        
    Transactions = request.user.transactions.all().order_by('-id')
    context = {
        'transactions': Transactions,
    }
    return render(request, 'report.html', context)

def report_download(request):
    if not request.user.is_authenticated:
        return redirect('home') 
    
    Transactions = request.user.transactions.all().order_by('-id')
    context = {
        'transactions': Transactions,
    }
    print('*^'*20)
    print('Download button clicked!')
    print('*^'*20)
    # pdf = generate_PDF.generate_pdf()
    
    return redirect('report')

