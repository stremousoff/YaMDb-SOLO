from django.db import models
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CreateUserSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    email = serializers.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено.'
            )
        return username

    def validate(self, data):
        """Запрещает использовать повторные username и email."""
        repeat_request_check = (
            User.objects.filter(
                username=data.get('username'),
                email=data.get('email')
            )
        )
        if repeat_request_check:
            return data
        user_check = User.objects.filter(username=data.get('username'))
        if user_check:
            raise serializers.ValidationError(f'{user_check} уже заняты.')
        email_check = User.objects.filter(email=data.get('email'))
        if email_check:
            raise serializers.ValidationError(f'{email_check} уже заняты.')
        return data


class UsersSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                f'Пользователь с {email} уже существует.')
        return email


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256, required=True)
    slug = serializers.SlugField(max_length=50, required=True)

    class Meta:
        model = Category
        fields = ('name', 'slug')

    def validate_slug(self, slug):
        if Category.objects.filter(slug=slug).exists():
            raise serializers.ValidationError('Slug должен быть уникальным.')
        return slug


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256, required=True)
    slug = serializers.SlugField(max_length=50, required=True)

    class Meta:
        model = Genre
        fields = ('name', 'slug')

    def validate_slug(self, slug):
        if Genre.objects.filter(slug=slug).exists():
            raise serializers.ValidationError('Slug должен быть уникальным.')
        return slug


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class GetTitleSerializer(serializers.ModelSerializer):
    genre = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_genre(self, title):
        genre_serializer = GenreSerializer(title.genre, many=True)
        return genre_serializer.data

    def get_category(self, title):
        category_serializer = CategorySerializer(title.category)
        return category_serializer.data

    def get_rating(self, title):
        query_set_reviews = title.reviews.all()
        if not query_set_reviews:
            return None
        rating = query_set_reviews.aggregate(
            average_score=models.Avg('score')
        )['average_score']
        return int(rating)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'title', 'score', 'pub_date')
        read_only_fields = ('title',)

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title = get_object_or_404(
                Title,
                id=self.context['view'].kwargs.get('title_id')
            )
            author = self.context['request'].user
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли отзыв к этому произведению'
                )
        return data

    def validate_score(self, score):
        if not 1 <= score <= 10:
            raise serializers.ValidationError('Оценка должна быть от 1 до 10')
        return score


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)

