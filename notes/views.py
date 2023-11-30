from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# FLAW 3 fix: importing Djangos build in validators for 'registration' function
# from django.core.exceptions import ValidationError
# from django.contrib.auth.password_validation import validate_password
# from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
from .models import Note
from django import forms



class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']

@login_required
# FLAW 4 - Inadequate CSRF protection
# FIX: remove 'csrf_exempt' to enable CSRF protection
@csrf_exempt
def home(request):
    # FLAW 1 - SQL injection
    username = request.user.username
    query = f"SELECT * FROM notes_note WHERE user_id = (SELECT id FROM auth_user WHERE username = '{username}')"
    with connection.cursor() as cursor:
        cursor.execute(query)
        notes = cursor.fetchall()
    # FIX: notes = Note.objects.filter(user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.save()
            print("Note added successfully:", new_note.title)
            return redirect('/') 
    else:
        form = NoteForm()

    print(notes)
    return render(request, 'homePage.html', {'notes': notes, 'form': form})

@login_required
# FLAW 4 - Inadequate CSRF protection
# FIX: remove 'csrf_exempt' to enable CSRF protection
@csrf_exempt
def edit(request, note_id):
    # FLAW 2 - Broken access control
    note = Note.objects.get(pk=note_id)
    # FIX: Check if the logged in user owns the note before allowing edits
    # if note.user != request.user:
    #   return HttpResponse("You are not authorized to edit this note.")
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.save()
            print("Note edited successfully:", new_note.title)
            return redirect('/')
    else:
        form = NoteForm(instance=note)

    context = {
        'note': note,
        'form': form    
    }
    return render(request, 'edit.html', context)

# FLAW 3 - Broken Authentication
# FIX: When creating users in Django shell, use this 'registration' function to avoid common or weak passwords
# def registration(username, password):
#     try:
#         validate_password(password)
#         user = User.objects.create_user(username=username, password=password)
#         return user
#     except ValidationError as e:
#         print("Password validation error:", e.messages)
#         return None

