from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter
from .models import Post, Category

class NewsFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name = 'postcategory__category',
        queryset = Category.objects.all(),
        label='Category',
        #empty_label = 'any'
    )

    class Meta:
        model = Post
        fields = {
            'header':['icontains'],
            #'categories':['exact'],
            'created_at':[
                'gt'
            ],
        }
