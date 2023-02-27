import django_filters

from .models import *

class CondoFilter(django_filters.FilterSet):
    class Meta:
        model = Condo
        fields = ['title', 'pet_friendly', 'city', 'number_of_units', 'built_in', 'floors']