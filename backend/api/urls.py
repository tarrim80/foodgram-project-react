from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import GetTokenUser, IngredientViewSet, TagViewSet, UserViewSet  # noqa

router = DefaultRouter()

router.register(
    'users', UserViewSet, basename='users'
)

router.register(
    'tags', TagViewSet, basename='tags'
)
router.register(
    'ingredients', IngredientViewSet, basename='ingredients'
)
# router.register(
#     'titles', TitleViewSet, basename='title'
# )
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews',
#     ReviewViewSet,
#     basename='review'
# )
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewSet,
#     basename='comment'
# )

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/token/login/', GetTokenUser.as_view()),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    # path('auth/token/', include('djoser.urls.jwt')),
    # path('auth/signup/', signup_user),
]
