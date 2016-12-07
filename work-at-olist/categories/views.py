from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Channel, Category
from .serializers import ChannelSerializer, ParentCategoryCrawlerSerializer, ChildCategoryCrawlerSerializer


class ExistingChannelsAPIView(APIView):
    http_method_names = ['get', 'post', 'put', 'delete', ]

    def get(self, request, channel_name=None, format='application/json', *args, **kwargs):
        if channel_name:
            serializer = ChannelSerializer(get_object_or_404(Channel, name=channel_name))
        else:
            serializer = ChannelSerializer(Channel.objects.all(), many=True)
        return Response(serializer.data)


class CategoriesAPIView(APIView):
    http_method_names = ['get', 'post', 'put', 'delete', ]

    def get(self, request, channel_name=None, format='application/json', *args, **kwargs):
        channel = get_object_or_404(Channel, name=channel_name)
        category_name = request.GET.get('category_name')
        parent_name = request.GET.get('parent_name')
        if category_name:
            category = get_object_or_404(Category, name=category_name, channel=channel, parent__name=parent_name)
            serializer = ParentCategoryCrawlerSerializer(category)
        else:
            serializer = ChildCategoryCrawlerSerializer(channel.base_categories, many=True)
        return Response(serializer.data)
