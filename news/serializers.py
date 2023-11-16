from rest_framework import serializers

from news.models import News, Comments, Category, Tag


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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'



class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class NewsDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    tag = TagSerializer(many=True)
    category_name = serializers.CharField(source='get_category_name')
    category_str = serializers.SerializerMethodField() # get_category_str
    tag_count = serializers.SerializerMethodField()
    comments = CommentsSerializer(many=True)

    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'is_active', 
                  'view_count', 'created_at', 'updated_at',
                  'category', 'tag', 'category_name', 'category_str',
                  'tag_count', 'comments')

    def get_category_str(self, obj):
        if obj.category is not None:
            return obj.category.title
        return None
    
    def get_tag_count(self, obj):
        return obj.tag.count()
