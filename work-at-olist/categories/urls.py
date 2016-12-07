from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from .views import ExistingChannelsAPIView, CategoriesAPIView

urlpatterns = [
    url(r'^channels/$', ExistingChannelsAPIView.as_view(), name='channels_list'),
    url(r'^channels/(?P<channel_name>[A-z]+)/$', ExistingChannelsAPIView.as_view(), name='channel'),
    url(r'^categories/(?P<channel_name>[A-z]+)/$', CategoriesAPIView.as_view(), name='categories_list'),
    url(r'^categories/(?P<channel_name>[A-z]+)/$', CategoriesAPIView.as_view(), name='categories_list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
