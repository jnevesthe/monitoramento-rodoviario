#Josemar Neves
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView 
#Josemar Neves
from .models import User
from django.contrib.auth.forms import SetPasswordForm
from .forms import  Registrar, EditForm
#Josemar Neves

class List(ListView):
    model=User
    template_name='user_list.html'
    context_object_name='users'
    #Josemar Neves
    
class Delete(DeleteView):
    #Josemar Neves
    model=User
    template_name='delete2.html'
    context_object_name='user'    
    success_url=reverse_lazy('user')

class Detail(DetailView):
    model=User
    template_name='user_list2.html'
    context_object_name='user'        
    
class Create(CreateView):
    model=User
    form_class=Registrar
    template_name='create.html'
    success_url=reverse_lazy('user')
    
class Edit(UpdateView):
    model=User
    form_class=EditForm
    template_name='edit.html'
    #context_object_name='user'
    success_url=reverse_lazy('user')
    """
    def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["user_id"] = self.object.id
    return context
   """
    
            
def word(request, pk):
    if resquest.method=='POST':
        form=SetPassworForm(request.POST, request.FILES, instance=pk)
        
        if form.is_valid():
            form.save()
            return redirect('user')
    else:
        form=SetPassForm(instance=pk)     
        return render(request, 'word.html', {'form':form})   
        

#Josemar Neves

































#Josemar Neves





























































#Josemar Neves