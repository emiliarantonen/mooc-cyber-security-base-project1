from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Note
from django import forms



class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']

@login_required
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

    return render(request, 'edit.html', {'form': form})