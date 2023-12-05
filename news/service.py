from news.models import News


class NewsService:
    __model = News

    @classmethod
    def get_all(cls, *args, **kwargs):
        return cls.__model.objects.all(
            *args, **kwargs
        )
 
    @classmethod
    def get_by_id(cls, news_id):
        return cls.__model.objects.get(id=news_id)
    
    @classmethod
    def create(cls, **kwargs):
        return cls.__model.objects.create(**kwargs)
    
    @classmethod
    def update(cls, news, **kwargs):
        for attr, value in kwargs.items():
            setattr(news, attr, value)
        news.save()
        return news
    