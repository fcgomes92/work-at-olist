from django.conf.urls import url, include

from categories import urls

from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Work At OList - API')

urlpatterns = [
    url(r'^docs/', schema_view),
    url(r'^$', schema_view),
    url(r'api/v1/', include(urls.urlpatterns, namespace='v1')),
]
