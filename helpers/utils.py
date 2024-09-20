from django.contrib.auth import get_user_model
import string 
import random
from django.core.management.base import BaseCommand
import unicodedata
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response



class BasicPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        if not hasattr(self, 'page'):
            raise AttributeError("Paginação não inicializada corretamente.")

        total_items = self.page.paginator.count
        total_pages = self.page.paginator.num_pages

        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_pages': total_pages,
            'count': total_items,
            'results': data
        })

def get_unique_username(value):
    """Criar um usuario unico pegando primeiros dados do email"""
    value = value.lower().split('@')
    username = value[0]
    nfkd = unicodedata.normalize('NFKD', username)
    username = "".join([u for u in nfkd if not unicodedata.combining(u)])
    UserModel = get_user_model()
    n = 1
    while True:
        if UserModel.objects.filter(username=username).exists():
            username = f'{username}{n}'
            n += 1
        else:
            return username