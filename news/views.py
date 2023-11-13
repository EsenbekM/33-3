from rest_framework.decorators import api_view
from rest_framework.response import Response

from news.models import News, Comments
from news.serializers import NewsDetailSerializer, NewsListSerializer, CommentsSerializer

# Method GET, POST, PUT, PATCH, DELETE

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
    # SELECT * FROM news_news;
    # ORM - Object Relational Mapping
    # news = News.objects.all() # QuerySet
    # news_list = []
    # for i in news:
    #     news_list.append(
    #         {
    #             "id": i.id,
    #             "title": i.title,
    #             "content": i.content,
    #             "is_active": i.is_active,
    #             "view_count": i.view_count,
    #             "created_at": i.created_at,
    #             "updated_at": i.updated_at,
    #         }
    #     )

    news = News.objects.all() # QuerySet
    
    serializer = NewsListSerializer(news, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def get_news_by_id(request, news_id):
    # SELECT * FROM news_news WHERE id = news_id;
    try:
        news = News.objects.get(id=news_id)
    except News.DoesNotExist:
        return Response({f"Новость с id {news_id} не существует"}, status=404)

    serializer = NewsDetailSerializer(news, many=False)

    return Response(serializer.data)


@api_view(['GET'])
def comments_list(request):
    # 1. Получить все комментарии
    comments = Comments.objects.all()
    # 2. Сериализовать комментарии
    serializer = CommentsSerializer(comments, many=True)
    # 3. Отправить ответ
    return Response(serializer.data)
