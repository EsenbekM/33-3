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


class NewsValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150)
    content = serializers.CharField()
    category_id = serializers.IntegerField(required=False, allow_null=True)
    tags = serializers.ListField(
        child=serializers.IntegerField(), 
        required=False
    )
    is_active = serializers.BooleanField(default=True)

    def validate_category_id(self, value: int):
        try:
            Category.objects.get(id=value)
        except Category.DoesNotExist:
            raise serializers.ValidationError('Категория не найдена!')
        return value

    def validate_title(self, value):
        if len(value) < 10:
            raise serializers.ValidationError('Длина заголовка должна быть больше 10 символов')
        return value

    def validate_tags(self, value: list):
        for tag_id in value:
            try:
                Tag.objects.get(id=tag_id)
            except Tag.DoesNotExist:
                raise serializers.ValidationError(f'Тег с id {tag_id} не найден!')
        return value
    
    def create(self, validated_data):
        title = validated_data.get('title')
        content = validated_data.get('content')
        category_id = validated_data.get('category_id')
        tags = validated_data.get('tags', [])
        is_active = validated_data.get('is_active', True)

        news = News.objects.create(
            title=title,
            content=content,
            category_id=category_id,
            is_active=is_active
        )

        news.tag.set(tags)

        return news
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.category_id = validated_data.get('category_id', instance.category_id)

        tags = validated_data.get('tags', instance.tag.all())
        instance.tag.set(tags)

        instance.save()

        return instance