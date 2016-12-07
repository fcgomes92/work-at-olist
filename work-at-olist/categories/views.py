from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Channel, Category
from .serializers import (ChannelSerializer, ParentCategoryCrawlerSerializer, ChildCategoryCrawlerSerializer,
                          SingleChannelSerializer)


class ExistingChannelsAPIView(APIView):
    """
    This view lists all existing channels.
    To get a specific channel the channel_name should be inserted in the URL.

    A format can be specified too. Just add a .<format> to the last string, i.e., channels.json or walmart.json and the response will use it.
    The format can be passed using a GET param.
    Check the OPTIONS for more information on formats.
    """
    http_method_names = ['get', 'post', 'put', 'delete', 'options']

    def get(self, request, channel_name=None, format='application/json', *args, **kwargs):
        """
        Get all channels a specific one.
        :param channel_name: A channel
        :param format: Response format

        :return:
        """
        if channel_name:
            # replace underscores to represent spaces
            channel_name = channel_name.replace('_', ' ')
            # serialize single Channel with its root categories
            serializer = SingleChannelSerializer(get_object_or_404(Channel, name=channel_name))
        else:
            # serialize all Channels
            serializer = ChannelSerializer(Channel.objects.all(), many=True)
        return Response(serializer.data)


class CategoriesAPIView(APIView):
    """

    """
    http_method_names = ['get', 'post', 'put', 'delete', ]

    def get(self, request, channel_name=None, format='application/json', *args, **kwargs):
        """
        Get all categories of a channel or a specific category.
        To get a category you must send the <category_name> usgin a get param.
        If the category is not a root category, you should also specify the <parent_name>.
        :param channel_name: A channel
        :param format: Response format
        :return:
        """
        if channel_name:
            # replace underscores to represent spaces
            channel_name = channel_name.replace('_', ' ')

        # get the chosen channel
        channel = get_object_or_404(Channel, name=channel_name)

        # get the category
        category_name = request.GET.get('category_name')

        # get the category's parent: if none will get a root category
        parent_name = request.GET.get('parent_name')

        if category_name:
            category = get_object_or_404(Category, name=category_name, channel=channel, parent__name=parent_name)

            # serialize categories children and serializes a parents list
            serializer = ParentCategoryCrawlerSerializer(category)
        else:
            # serialize all channel's categories
            serializer = ChildCategoryCrawlerSerializer(channel.base_categories, many=True)
        return Response(serializer.data)
