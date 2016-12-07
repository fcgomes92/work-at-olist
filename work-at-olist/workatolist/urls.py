from django.conf.urls import url, include

from categories import urls

urlpatterns = [
    url(r'^api/v1/', include(urls.urlpatterns, namespace='v1')),
]
