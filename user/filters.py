from django_filters import rest_framework as filters
from .models import User


class UserFilter(filters.FilterSet):
    email = filters.CharFilter(field_name="email", lookup_expr="icontains", label="E-mail")

    class Meta:
        model = User
        fields = []