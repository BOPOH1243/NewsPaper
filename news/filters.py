from django_filters import FilterSet
from .models import Post

class NewsFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'header':['icontains'],
            'category':['icontains'],
            'created_at':[
                'lt',
                'gt'
            ],
        }
