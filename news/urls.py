from django.urls import path
from .views import NewDelete, NewsList, NewDetail, create_new, NewCreate, NewUpdate, subscribe


urlpatterns = [
    path('', NewsList.as_view(), name='new_list'),
    path('<int:pk>', NewDetail.as_view(), name='new_detail'),
    #path('create/', create_new, name = 'new_create'),
    path('create/', NewCreate.as_view(), name='new_create'),
    path('<int:pk>/update/', NewUpdate.as_view(), name = 'new_update'),
    path('<int:pk>/delete/', NewDelete.as_view(), name = 'new_delete'),
    path('categories/<int:pk>/subscribe/', subscribe, name='subscribe_to_category'),
]


#<str:post_type>/
