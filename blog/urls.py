from django.urls import path, include
# from . import views
from .views import HomeView, CondoDetailView, AddCondoView, UpdateCondoView, DeleteCondoView, submit_review, chart_popup
from django.conf import settings

urlpatterns = [
    # path('', views.home, name="home"),
    path('', HomeView.as_view(), name="home"),
    path('condo/<int:pk>', CondoDetailView.as_view(), name="condo-info"),
    path('add_condo/', AddCondoView.as_view(), name='add_condo'),
    path('condo/edit/<int:pk>', UpdateCondoView.as_view(), name='update_condo'),
    path('condo/<int:pk>/remove', DeleteCondoView.as_view(), name='delete_condo'),
    path('submit_review/<int:condo_id>/', submit_review, name="submit_review"),
    path('chart_popup/', chart_popup, name='chart_popup'),
]