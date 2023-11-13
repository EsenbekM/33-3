from rest_framework import serializers

from news.models import News, Comments


# class NewsSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=150)
#     content = serializers.CharField()
#     is_active = serializers.BooleanField()
#     view_count = serializers.IntegerField()
#     created_at = serializers.DateTimeField()
#     updated_at = serializers.DateTimeField()


class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'content')


class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'