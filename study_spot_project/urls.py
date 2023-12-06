from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'django_google_sso'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        "accounts/", include(
            "django_google_sso.urls",
            namespace="django_google_sso"
        ), name="login"
    ),
    path('', views.home, name='home'),
    path("accounts/logout", LogoutView.as_view(next_page='/'), name="logout"),
    path('map', views.map, name='map'),
    path('add', views.PlaceCreateView.as_view(), name='add'),
    path('<str:place_name_slug>/details', views.place_details, name='place_details'),
    path('admin_map/', views.admin_map, name='admin_map'),
    path('staff', views.staff, name='staff'),
    path('<str:place_name_slug>/delete', views.delete_unapproved, name='delete_unapproved'),
    path('<str:place_name_slug>/approve', views.approve_unapproved, name='approve_unapproved'),
    path('select_user_type/', views.select_user_type, name='select_user_type'),
    path('<str:place_name_slug>/remove', views.remove_place, name='remove_place'),
    path('<str:place_name_slug>/update', views.PlaceUpdateView.as_view(), name='update_place'),
    path('<str:review_id>/details/delete-review', views.delete_review, name='delete_review'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('<str:user_id>/profile', views.profile, name='profile'),
]
