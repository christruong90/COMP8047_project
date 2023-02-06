from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Condo
from .forms import CondoForm, EditForm
from django.urls import reverse_lazy

# Create your views here.

# def home(request):
#     return render(request, 'home.html', {})

class HomeView(ListView):
    model = Condo 
    template_name = 'home.html'
    order = ['-id']

class CondoDetailView(DetailView):
    model = Condo
    template_name = 'condo_details.html'

class AddCondoView(CreateView):
    model = Condo
    form_class = CondoForm
    template_name = 'add_condo.html'
    # fields = '__all__'

class UpdateCondoView(UpdateView):
    model = Condo
    form_class = EditForm
    template_name = "update_condo_details.html"
    # fields = '__all__'

class DeleteCondoView(DeleteView):
    model = Condo
    template_name = "delete_condo.html"
    success_url = reverse_lazy('home')