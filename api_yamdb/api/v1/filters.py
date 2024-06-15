import django_filters
from reviews.models import Title


class TitleFilterFields(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'year', 'name')
