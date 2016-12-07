from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from .models import Channel, Category


class ChildCategoryCrawlerSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = Category
        exclude = ('id', 'uid', 'channel', 'parent')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id', 'uid', 'channel', 'parent')


class ParentCategoryCrawlerSerializer(serializers.ModelSerializer):
    channel = serializers.SlugRelatedField(read_only=True, slug_field='name', )
    parents = serializers.SerializerMethodField()
    children = ChildCategoryCrawlerSerializer(many=True)

    class Meta:
        model = Category
        exclude = ('id', 'uid', 'channel', 'parent')

    def get_parents(self, category):
        parents = []
        new_category = category.parent
        if not new_category:
            return None
        while new_category:
            print(new_category, new_category.id)
            parents.append(CategorySerializer(new_category).data)
            new_category = new_category.parent
        return parents


class ChannelSerializer(serializers.ModelSerializer):
    # categories = serializers.SerializerMethodField(read_only=True)

    # def get_categories(self, channel):
    #     return CategorySerializer(channel.base_categories, many=True).data

    class Meta:
        model = Channel
        exclude = ('id', 'uid',)
