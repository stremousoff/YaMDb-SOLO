from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, CreateUserView,
                    GenreViewSet, JwtTokenCreateView, ReviewViewSet,
                    TitleViewSet, UsersViewSet)

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')
router.register(r'categories', viewset=CategoryViewSet, basename='categories')
router.register(r'genres', viewset=GenreViewSet, basename='genres')
router.register(r'titles', viewset=TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    viewset=ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    viewset=CommentViewSet,
    basename='comments'
)

auth_patterns = [
    path('token/', JwtTokenCreateView.as_view()),
    path('signup/', CreateUserView.as_view()),
]

urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('', include(router.urls)),
]
