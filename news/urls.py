from django.urls import path
from .views import NewsList, NewDetail, create_new, NewCreate, NewUpdate


urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewDetail.as_view(), name='new_detail'),
    #path('create/', create_new, name = 'new_create'),
    path('create/', NewCreate.as_view(), name='new_create'),
    path('<int:pk>/update/', NewUpdate.as_view(), name = 'new_update'),
]
