from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Avg, Count
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Condo, ReviewRating, Developer, DeveloperReview
from .forms import CondoForm, EditForm, ReviewForm, DeveloperReviewForm
from django.urls import reverse_lazy
from django.contrib import messages
from .filters import CondoFilter
from django.core.paginator import Paginator
from django.views.generic.list import MultipleObjectMixin
import json, numpy
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Create your views here.

class DeveloperView(ListView):
    model = Developer
    template_name = 'developers.html'

class DeveloperDetailView(DetailView):
    model = Developer
    template_name = 'developer_details.html'

class HomeView(ListView):
    model = Condo 
    template_name = 'home.html'
    order = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        ## Search Functionality
        myFilter = CondoFilter(self.request.GET, queryset=self.get_queryset())
        context['myFilter'] = myFilter

        # Webscraping Functionality
        url = "https://rates.ca/mortgage-rates/british-columbia#brokersandcreditunions"
        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        data = soup.find_all('div', {'class':"richtext-container"})

        mortage_brokers_list = data[2].find_all("ul")

        large_brokerage_list = []
        for li in mortage_brokers_list[0]:
            large_brokerage_list.append(li.text)
        
        context['large_brokerage_list'] = large_brokerage_list
        
        online_brokerage_list = []
        for li in mortage_brokers_list[1]:
            online_brokerage_list.append(li.text)
        
        context['online_brokerage_list'] = online_brokerage_list

        creditunion_list = []
        for li in data[3].find_all("ul")[0]:
            creditunion_list.append(li.text)
        
        context['creditunion_list'] = creditunion_list

        return context
    
class CondoDetailView(DetailView):
    model = Condo
    template_name = 'condo_details.html'

    def get_queryset(self):
        return Condo.objects.prefetch_related('reviews')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        condo = self.get_object()

        ## Paginate condo reviews
        condo_reviews = ReviewRating.objects.filter(condo=condo)
        paginator = Paginator(condo_reviews, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['condo_reviews'] = page_obj
        

        ratings = ReviewRating.objects.filter(condo=condo).aggregate(avg_customer_service=Avg('customer_service'), avg_build_quality=Avg('build_quality'),avg_amenities=Avg('amenities'), avg_location=Avg('location'))
        context['ratings'] = ratings

        ## Pass chart.js context data
        ratings_data = {
            'labels': ['Customer Service', 'Build Quality', 'Amenities', 'Location'],
            'values': [ratings['avg_customer_service'], ratings['avg_build_quality'], ratings['avg_amenities'], ratings['avg_location']]
        }
        ratings_data_json = json.dumps(ratings_data)
        context['ratings_data'] = ratings_data_json

        ## get number of rows, yes-recommendation and no-recommendation
        total_rows = ReviewRating.objects.filter(condo=condo).count()
        context['total_rows'] = total_rows
        number_of_yes = ReviewRating.objects.filter(condo=condo).filter(would_reviewer_recommend="1").count()
        context['number_of_yes'] = number_of_yes
        number_of_no = ReviewRating.objects.filter(condo=condo).filter(would_reviewer_recommend="0").count()
        context['number_of_no'] = number_of_no


        # get most recent review reviews:
        latest_review_object = ReviewRating.objects.filter(condo=condo).order_by('-id')
        if latest_review_object.exists():
            no_probability_list = []
            yes_probability_list = []
            latest_review_object = latest_review_object.first() 
            context['latest_review_object'] = latest_review_object
            last_customer_service_rating = latest_review_object.customer_service
            last_amenities_rating = latest_review_object.amenities
            last_location_rating = latest_review_object.location
            last_build_quality_rating = latest_review_object.build_quality


            ## get customer service probability
            # query formula comes from filtering for the last customer rating, whether reviewers recommend or not and getting a count of number of stars (rows) based on the last customer rating.
            yes_customer_service_probability = ReviewRating.objects.filter(condo=condo).filter(customer_service=last_customer_service_rating).filter(would_reviewer_recommend=1).aggregate(star_count=Count("id"))
            # if condition if number of yes is not 0
            if number_of_yes !=0:
                yes_customer_service_probability = (yes_customer_service_probability['star_count']) / number_of_yes
                context['yes_customer_service_probability'] = yes_customer_service_probability
                yes_probability_list.append(yes_customer_service_probability)
            

            no_customer_service_probability = ReviewRating.objects.filter(condo=condo).filter(customer_service=last_customer_service_rating).filter(would_reviewer_recommend=0).aggregate(star_count=Count("id"))
            # if condition if number of no is not 0
            if number_of_no !=0:
                no_customer_service_probability = (no_customer_service_probability['star_count'])/ number_of_no
                context['no_customer_service_probability'] = no_customer_service_probability
                no_probability_list.append(no_customer_service_probability)

            ## get amenities probability
            yes_amenities_probability = ReviewRating.objects.filter(condo=condo).filter(amenities=last_amenities_rating).filter(would_reviewer_recommend=1).aggregate(star_count=Count("id"))
            if number_of_yes !=0:
                yes_amenities_probability = (yes_amenities_probability['star_count']) / number_of_yes
                context['yes_amenities_probability'] = yes_amenities_probability
                yes_probability_list.append(yes_amenities_probability)

            no_amenities_probability = ReviewRating.objects.filter(condo=condo).filter(amenities=last_amenities_rating).filter(would_reviewer_recommend=0).aggregate(star_count=Count("id"))
            # if condition if number of no is not 0
            if number_of_no != 0:
                no_amenities_probability = (no_amenities_probability['star_count']) / number_of_no
                context['no_amenities_probability'] = no_amenities_probability
                no_probability_list.append(no_amenities_probability)

            ## get location probability
            yes_location_probability = ReviewRating.objects.filter(condo=condo).filter(location=last_location_rating).filter(would_reviewer_recommend=1).aggregate(star_count=Count("id"))
            if number_of_yes !=0:
                yes_location_probability = (yes_location_probability['star_count']) / number_of_yes
                context['yes_location_probability'] = yes_location_probability
                yes_probability_list.append(yes_location_probability)

            no_location_probability = ReviewRating.objects.filter(condo=condo).filter(location=last_location_rating).filter(would_reviewer_recommend=0).aggregate(star_count=Count("id"))
            # if condition if number of no is not 0
            if number_of_no != 0:
                no_location_probability = (no_location_probability['star_count']) / number_of_no
                
                context['no_location_probability'] = no_location_probability
                no_probability_list.append(no_location_probability)

            ## get build quality probabilty 
            yes_build_quality_probability = ReviewRating.objects.filter(condo=condo).filter(build_quality=last_build_quality_rating).filter(would_reviewer_recommend=1).aggregate(star_count=Count("id"))
            
            if number_of_yes !=0:
                context['test2'] = yes_build_quality_probability['star_count']
                yes_build_quality_probability = (yes_build_quality_probability['star_count']) / number_of_yes
                context['yes_build_quality_probability'] = yes_build_quality_probability
                yes_probability_list.append(yes_build_quality_probability)

            no_build_quality_probability = ReviewRating.objects.filter(condo=condo).filter(build_quality=last_build_quality_rating).filter(would_reviewer_recommend=0).aggregate(star_count=Count("id"))
            # if condition if number of no is not 0
            if number_of_no != 0:
                no_build_quality_probability = (no_build_quality_probability['star_count']) / number_of_no

                context['no_build_quality_probability'] = no_build_quality_probability
                no_probability_list.append(no_build_quality_probability)

            yes_probability = number_of_yes/total_rows
            context['yes_probability'] = yes_probability
            yes_probability_list.append(yes_probability)

            no_probability = number_of_no/total_rows
            context['no_probability'] = no_probability
            no_probability_list.append(no_probability)

            # yes_probability_list = [yes_customer_service_probability, yes_amenities_probability, yes_location_probability, yes_build_quality_probability, yes_probability]
            yes_probability_list = [i for i in yes_probability_list if i != 0]
            if len(yes_probability_list):
                yes_probability_list_product = numpy.prod(yes_probability_list)
            else:
                yes_probability_list_product = 0
            
            # no_probability_list = [no_customer_service_probability, no_amenities_probability, no_location_probability, no_build_quality_probability, no_probability]
            no_probability_list = [i for i in no_probability_list if i != 0]
            if len(no_probability_list) > 0:
                no_probability_list_product = numpy.prod(no_probability_list)
            else:
                no_probability_list_product = 0

            if yes_probability_list_product > no_probability_list_product:
                value_rating = 0 + (100 * yes_probability_list_product)
            else:
                value_rating = 0 - (100 * no_probability_list_product)

            context['value_rating'] = value_rating

        return context  

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
            data.would_reviewer_recommend = form.cleaned_data['would_reviewer_recommend']
            data.location = form.cleaned_data['location']
            data.condo_id = condo_id
            data.user_id = request.user.id
            data.save()
            messages.success(request, 'Thank you! Your review has been Submitted.')
            return redirect(url)
          
def chart_popup(request):
    return render(request, 'condo/chart_popup.html')
    
def chart_8071(request):
    data = pd.read_csv('/Users/i522007/Downloads/Electric_Vehicle_Population_Data.csv')
    data = data.to_dict(orient='records')
    json_data = json.dumps(data)

    context = {'message': 'Hello, change!', 'csv_data': json_data}
    return render(request, 'chart_8071.html', context)

def submit_developer_review(request, developer_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        # try:
        #     reviews = ReviewRating.objects.get(user__id=request.user.id, condo__id=condo_id)
        #     form = ReviewForm(request.POST, instance=reviews)
        #     form.save()
        #     messages.success(request, 'Thank you! Your review has been updated.')
        #     return redirect(url)
        # except ReviewRating.DoesNotExist:
        form = DeveloperReviewForm(request.POST)
        if form.is_valid():
            data = DeveloperReview()
            data.review_title = form.cleaned_data['review_title']
            data.review = form.cleaned_data['review']
            data.customer_service = form.cleaned_data['customer_service']
            data.build_quality = form.cleaned_data['build_quality']
            data.amenities = form.cleaned_data['amenities']
            data.developer_id = developer_id
            data.user_id = request.user.id
            data.save()
            messages.success(request, 'Thank you! Your review has been Submitted.')
            return redirect(url)
        else:
            messages.error(request, 'FORM ERROR')
