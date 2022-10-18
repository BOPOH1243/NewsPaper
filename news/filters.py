from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter
from .models import Post, Category
from django_filters import *
from django import forms
class NewsFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name = 'postcategory__category',
        queryset = Category.objects.all(),
        label='Category',
        #empty_label = 'any'
    )
    #просто нашёл в интернете, вроде работает исправно
    start_date = DateFilter(field_name='created_at',
                            widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                            lookup_expr='gt', label='Start Date')
    end_date = DateFilter(field_name='created_at',
                          widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                          lookup_expr='lt', label='End Date')
    #created = DateTimeFilter()

    class Meta:
        model = Post
        fields = {
            'header':['icontains'],
            'post_type':['exact'],
            #'categories':['exact'],
            'created_at':[
                'gt'
            ],
        }
