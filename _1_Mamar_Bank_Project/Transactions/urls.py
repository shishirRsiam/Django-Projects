from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='report'),
    path('deposit/', views.deposit, name='deposit'), 
    path('withdrow/', views.withdrow, name='withdrow'),
    path('sent/money/', views.sent_money, name='sent_money'),

    path('loan/', views.loan, name='loan'),
    path('report/', views.report, name='report'),
    path('report/download/', views.report_download, name='download_report'),
    path('report/', views.report, name='send_report_email'),
    path('report/', views.report, name='filter_transactions'),
    path('loan/request/', views.loan_request, name='loan_request'),
    path('loan/approve/<int:loan_id>/', views.approve_loan, name='approve_loan'),
    path('loan/request/', views.loan_request, name='reject_loan'),
]
