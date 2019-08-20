from __future__ import print_function
from django.shortcuts import render, redirect
from .models import *
from .models import Book
from django.contrib import messages
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import datetime
import pickle
import os.path
import bcrypt


def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_matches = User.objects.filter(email=request.POST['email'])
        if len(user_matches) > 0:
            messages.error(request, 'Email already exists. Please log in.')
            return redirect('/')
        else:
            User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=request.POST['password']
            )
            last_user_created = User.objects.last()
            request.session['user_id'] = last_user_created.id
            request.session['user_name'] = last_user_created.first_name
            messages.success(request, 'Successfully registered!')
            return redirect('/dash')

def dash(request):
    user= User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'all_books': Book.objects.all()
    }
    return render(request, 'dash.html', context)

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_to_login_list = User.objects.filter(email=request.POST['login_email'])
        request.session['user_id'] = user_to_login_list[0].id
        request.session['user_name'] = user_to_login_list[0].first_name
        messages.success(request, 'Successfully logged in!')
        return redirect('/dash')

def book(request):
    return render(request, 'book.html')

def new_book_process(request):
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/book/new')
    else:
        user = User.objects.get(id = request.session['user_id'])
        Book.objects.create(address=request.POST['address'], phone=request.POST['phone'], start=request.POST['start'], end=request.POST['end'], notes=request.POST['notes'], creator=user)
        print (Book.objects.all())
    return redirect(f"/dash")

def edit_book(request, bookid):
    book = Book.objects.get(id=bookid)
    user = User.objects.get(id = request.session['user_id'])
    context={
        'user': user,
        "book": book
    }
    return render(request, 'edit.html', context)

def edit_book_process(request, bookid):
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/book/edit/{bookid}')
    else:
        book= Book.objects.get(id=bookid)
        book.phone=request.POST['phone']
        book.address=request.POST['address']
        book.start=request.POST['start']
        book.end=request.POST['end']
        book.notes= request.POST['notes']
        book.save()
        return redirect(f"/dash")

def add_book(request):
    errors = User.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/book')
    else:
        user = User.objects.get(id = request.session['user_id'])
        Job.objects.create(title=request.POST['title'], desc=request.POST['desc'], location=request.POST['location'], creator=user)
        print (Job.objects.all())
    return redirect(f"/dash")


def view_book(request, bookid):
    user= User.objects.get(id=request.session['user_id'])
    book= Book.objects.get(id=bookid)
    context = {
        'user': user,
        'book': book
    }
    return render(request, 'view.html', context)


def delete(request, bookid):
    book= Book.objects.get(id=bookid)
    book.delete()
    return redirect('/dash')


def profile(request, userid):
    user = User.objects.get(id=userid)
    context = {
        "user": user
    }
    return render(request, "profile.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')

def calender(request):
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    calendar_list_entry = service.calendarList().get(calendarId='primary').execute()
    #calenders = service.calenderList().list().execute()
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    
    context = {
        "calender": calendar_list_entry 
    }
    return render(request, 'calender.html', context)


if __name__ == '__main__':
    main()
