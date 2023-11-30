from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.generics import GenericAPIView, ListCreateAPIView,  RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from rest_framework.mixins import ListModelMixin
from news.models import News, Comments, Category, Tag
from news.serializers import CategorySerializer, NewsDetailSerializer, NewsListSerializer, CommentsSerializer, NewsValidateSerializer, TagSerializer



class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'id'


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None
    # filter_backends = [SearchFilter, OrderingFilter]
    # search_fields = ['title']
    # ordering_fields = ['title', 'id']
    # permission_classes = [IsAuthenticated]
    # pagination_class = PageNumberPagination


class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


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


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_news(request):
    if request.method == 'GET':
        # print(request.user)
        news = News.objects.all() \
            .select_related('category') \
            .prefetch_related('tag', 'comments')
        
        search = request.query_params.get('search', None)
        if search is not None:
            news = news.filter(title__icontains=search)
        
        serializer = NewsDetailSerializer(instance=news, many=True)

        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = NewsValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        news = serializer.save()
        
        serializer = NewsDetailSerializer(instance=news, many=False)

        return Response(
            {
                "message": "Created!",
                "data": serializer.data
            },
            status=201
        )


@api_view(['GET', 'PUT', 'DELETE'])
def get_news_by_id(request, news_id):
    # SELECT * FROM news_news WHERE id = news_id;
    try:
        news = News.objects.get(id=news_id)
    except News.DoesNotExist:
        return Response({f"Новость с id {news_id} не существует"}, status=404)

    if request.method == 'GET':
        serializer = NewsDetailSerializer(instance=news, many=False)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = NewsValidateSerializer(instance=news, data=request.data)
        serializer.is_valid(raise_exception=True)
        news = serializer.update(instance=news, validated_data=serializer.validated_data)

        serializer = NewsDetailSerializer(instance=news, many=False)
        
        return Response(
            data={
                "message": "updated!",
                "data": serializer.data
            },
            status=200
        )
    
    if request.method == 'DELETE': 
        news.delete()
        return Response(
            data={
                'message': 'deleted'
            },
            status=204
        )


@api_view(['GET'])
def comments_list(request):
    # 1. Получить все комментарии
    comments = Comments.objects.all()
    # 2. Сериализовать комментарии
    serializer = CommentsSerializer(comments, many=True)
    # 3. Отправить ответ
    return Response(serializer.data)
