from django.urls import include, path

urlpatterns = [
    path('slackin', include('django_slackin_public.urls')),
]
