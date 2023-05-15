from django.urls import path, include
# from . import views
from .views import HomeView, CondoDetailView, AddCondoView, UpdateCondoView, DeleteCondoView, submit_review, chart_popup, chart_8071, DeveloperView, DeveloperDetailView, submit_developer_review
from django.conf import settings

urlpatterns = [
    # path('', views.home, name="home"),
    path('', HomeView.as_view(), name="home"),
    path('condo/<int:pk>', CondoDetailView.as_view(), name="condo-info"),
    path('add_condo/', AddCondoView.as_view(), name='add_condo'),
    path('condo/edit/<int:pk>', UpdateCondoView.as_view(), name='update_condo'),
    path('condo/<int:pk>/remove', DeleteCondoView.as_view(), name='delete_condo'),
    path('submit_review/<int:condo_id>/', submit_review, name="submit_review"),
    path('submit_developer_review/<int:developer_id>/', submit_developer_review, name="submit_developer_review"),
    path('chart_popup/', chart_popup, name='chart_popup'),
    path('chart_8071/', chart_8071, name='chart_8071'),
    path('developers/', DeveloperView.as_view(), name="developers"),
    path('developer/<int:pk>', DeveloperDetailView.as_view(), name='developer-detail')
    # path('mortgage_rates/', mortgage_scrape, name='mortgage_rates'),
]