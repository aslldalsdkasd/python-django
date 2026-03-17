from django.shortcuts import render
from django.views.generic import ListView

from .models import Article


class ArticleViewList(ListView):
    template_name = 'article_list.html'
    context_object_name = 'articles'
    queryset = (Article.objects.prefetch_related('tags')
                .select_related('author','category')
                .defer('content').all()
                )




