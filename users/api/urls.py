from django.urls import path
from users.api.views import UserListView, UserView, UserCreateView, AddressView

urlpatterns = [
    path('list/', UserListView.as_view()),
    path('<int:pk>/', UserView.as_view()),
    path('create/', UserCreateView.as_view()),
    path('<int:user_id>/address/', AddressView.as_view()),
]
