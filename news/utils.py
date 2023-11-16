from news.models import News, Category, Tag, Comments


def create_100_news_with_10_comments_10_tag_1_category():
    category = Category.objects.create(title='Category')
    tag = Tag.objects.create(title='Tag')
    for i in range(100):
        news = News.objects.create(
            category=category,
            title=f'News {i}',
            content=f'Content {i}',
            is_active=True,
            view_count=i,
        )
        news.tag.add(tag)
        for j in range(10):
            Comments.objects.create(
                news=news,
                content=f'Comment {j}',
            )
    print('News created')

