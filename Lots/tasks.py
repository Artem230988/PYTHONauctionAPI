from django.core.mail import send_mail
from config.celery import app


@app.task
def send_spam_email(user_email):
    send_mail('New current rate!', 'По вашему лоту сделали новую ставку', 'AuctionAPI', [user_email, ])



@app.task
def summa(x, y):
    print(x ** y ** x, '++++++++++++++++++++')
