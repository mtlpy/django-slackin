import django


if django.VERSION >= (2,):
    from django.urls import include, path

    pattern = path('slackin', include('django_slackin_public.urls'))

else:
    from django.conf.urls import include, url

    pattern = url(r'^slackin', include('django_slackin_public.urls'))


urlpatterns = [pattern]
