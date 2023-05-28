
from django.views.generic import View
from django.shortcuts import render, redirect
from notes.models import Notes
from notes.forms import NotesForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class Dashboard(View):
    @method_decorator(login_required())
    def get(self, request, *args, **kwargs):
        notes = Notes.objects.filter(user_id=request.user.id).order_by('-order')
        context = {
            'notes': notes
        }
        return render(request, 'dashboard.html', context)
    
class NotesCreate(View):
    @method_decorator(login_required())
    def get(self, request, *args, **kwargs):
        form = NotesForm()
        context = {
            'title' : 'Add Notes',
            'form' : form,
        }
        template = 'notes/create.html'
        return render(request, template, context)
    
    @method_decorator(login_required())
    def post(self, request, *args, **kwargs): 
        form = NotesForm(data=request.POST)
        order = Notes.objects.filter(user_id=request.user.id).order_by('-order')[:1]
        if len(order) == 0: order = 1
        else: order = order[0].order+1
        
        if form.is_valid():
            note = form.save(commit=False)
            note.user_id = request.user.id
            note.order = order
            note.save()
            messages.success(request, 'Note successfully added.')
            return redirect('dashboard',)

        messages.error(request, 'Add note failed.')
        return render(request, 'notes/create.html', {'form': form})

class NotesEdit(View):
    @method_decorator(login_required())
    def get(self, request, id, *args, **kwargs):
        try:
            notes = Notes.objects.get(id=id)
            form = NotesForm(instance=notes)
            id = notes.id
        except:
            notes = None
            form = NotesForm()
            id = None
        context = {
            'title' : 'Edit Note',
            'form' : form,
            'edit' : 'true',
            'id' : id,
            'notes': notes,
        }
        return render(request, 'notes/create.html', context)
    
    @method_decorator(login_required())
    def post(self, request, *args, **kwargs):
        notes = Notes.objects.get(id=request.POST.get('id'))
        order = notes.order
        form = NotesForm(data=request.POST, files=request.FILES, instance=notes)
        if form.is_valid():
            notes.order = order
            notes.save()
            messages.success(request, 'Note successfully updated.')
            return redirect('dashboard')

        messages.error(request, 'Update note failed.')
        return render(request, 'notes/create.html', {'form': form})
    
class NotesFlagDelete(View):
    @method_decorator(login_required())
    def post(self, request, *args, **kwargs):
        notes = Notes.objects.get(id=request.POST.get('id'))
        if request.POST.get('action') == 'flag':
            notes.is_done = not notes.is_done
            notes.save()
            messages.success(request, 'Note successfully updated.')
            return redirect('dashboard')
        if request.POST.get('action') == 'delete':
            notes.delete()
            messages.success(request, 'Note successfully removed.')
            return redirect('dashboard')

        messages.error(request, 'Task Failed.')
        return redirect('dashboard')

class NotesReorder(View):
    @method_decorator(login_required())
    def post(self, request, *args, **kwargs):
        total = len(request.POST.getlist('id'))
        for reorder in request.POST.getlist('id'):
            # print(order)
            notes = Notes.objects.get(id=reorder)
            notes.order = total
            notes.save()
            print(reorder, total, notes.order)
            total -= 1
        messages.success(request, 'Reorder Success.')
        return redirect('dashboard')

        # messages.error(request, 'Reorder Failed.')
        # return redirect('dashboard')