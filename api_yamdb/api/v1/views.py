from datetime import timedelta

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from reviews.models import Category, Genre, Review, Title

from .filters import TitleFilterFields
from .mixins import ListCreateDestroyViewSet
from .permissions import AdminOrReadOnly, UserOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          CreateUserSerializer, GenreSerializer,
                          GetTitleSerializer, ReviewSerializer,
                          TitleSerializer, UsersSerializer)
from .utils import send_confirmation_code_email

User = get_user_model()


class JwtTokenCreateView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        if not request.data:
            return Response({'error': 'Отправлен пустой запрос.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if 'username' not in request.data:
            return Response({'error': 'Не указано имя пользователя.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if 'confirmation_code' not in request.data:
            return Response({'error': 'Не указан код подтверждения.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, username=request.data['username'])
        confirmation_code = request.data.get('confirmation_code')
        check_data = default_token_generator.check_token(user,
                                                         confirmation_code)
        if not check_data:
            return Response({'error': f'Невалидные данные, проверьте'
                                      f'confirmation_code/username.'},
                            status=status.HTTP_400_BAD_REQUEST)
        payload = {
            'username': user.username,
            'exp': timezone.now() + timedelta(days=30)
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return Response({'token': token}, status=status.HTTP_200_OK)


class CreateUserView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user)
        send_confirmation_code_email(user, confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(detail=False, methods=['get', 'patch'], url_path='me')
    def me(self, request):
        if request.method == 'GET':
            user = request.user
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(request.user, data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data.pop('role', None)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return User.objects.all()
        raise PermissionDenied('Недостаточно прав.')

    def update(self, request, *args, **kwargs):
        if request.method == 'PATCH':
            return super().update(request, *args, **kwargs)
        raise MethodNotAllowed(status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.role == 'admin':
            user = (get_object_or_404(User, username=kwargs.get('username'))
                    .delete())
            return Response(f'Пользователь {user} удален.',
                            status.HTTP_204_NO_CONTENT)
        return Response(f'Недостаточно прав.', status.HTTP_403_FORBIDDEN)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterFields

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (UserOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (UserOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
