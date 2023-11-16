from rest_framework.decorators import api_view
from rest_framework.response import Response

from news.models import News, Comments
from news.serializers import NewsDetailSerializer, NewsListSerializer, CommentsSerializer

# Method GET, POST, PUT, PATCH, DELETE
# API - Application Programming Interface
# REST API - REpresentational State Transfer API
# JSON - JavaScript Object Notation
# ORM - Object Relational Mapping

# snake_case: hello_world: function, variable, method
# CamelCase: HelloWorld: class
# OverFetch - перезапрос данных
# UnderFetch - недостаточно данных

@api_view(['GET'])
def hello_world(request):
    dct = {
        'int': 1,
        'str': 'string',
        'list': [1, 2, 3],
        'dict': {
            'key': 'value'
        },
        'bool': True,
    }
    return Response(dct)


@api_view(['GET'])
def get_news(request):
    news = News.objects.all() \
        .select_related('category') \
        .prefetch_related('tag', 'comments')
    
    search = request.query_params.get('search', None)
    if search is not None:
        news = news.filter(title__icontains=search)
    
    serializer = NewsDetailSerializer(instance=news, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def get_news_by_id(request, news_id):
    # SELECT * FROM news_news WHERE id = news_id;
    try:
        news = News.objects.get(id=news_id)
    except News.DoesNotExist:
        return Response({f"Новость с id {news_id} не существует"}, status=404)

    serializer = NewsDetailSerializer(instance=news, many=False)

    return Response(serializer.data)


@api_view(['GET'])
def comments_list(request):
    # 1. Получить все комментарии
    comments = Comments.objects.all()
    # 2. Сериализовать комментарии
    serializer = CommentsSerializer(comments, many=True)
    # 3. Отправить ответ
    return Response(serializer.data)
