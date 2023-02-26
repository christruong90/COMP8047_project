from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Condo, ReviewRating
from .forms import CondoForm, EditForm, ReviewForm
from django.urls import reverse_lazy
from django.contrib import messages

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

    def get_queryset(self):
        return Condo.objects.prefetch_related('reviews')

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

def submit_review(request, condo_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        # try:
        #     reviews = ReviewRating.objects.get(user__id=request.user.id, condo__id=condo_id)
        #     form = ReviewForm(request.POST, instance=reviews)
        #     form.save()
        #     messages.success(request, 'Thank you! Your review has been updated.')
        #     return redirect(url)
        # except ReviewRating.DoesNotExist:
        form = ReviewForm(request.POST)
        if form.is_valid():
            data = ReviewRating()
            data.review_title = form.cleaned_data['review_title']
            data.review = form.cleaned_data['review']
            data.customer_service = form.cleaned_data['customer_service']
            data.build_quality = form.cleaned_data['build_quality']
            data.amenities = form.cleaned_data['amenities']
            # data.would_reviewer_recommend = form.cleaned_data['would_reviewer_recommend']
            data.location = form.cleaned_data['location']
            data.condo_id = condo_id
            data.user_id = request.user.id
            data.save()
            messages.success(request, 'Thank you! Your review has been Submitted.')
            return redirect(url)
    

