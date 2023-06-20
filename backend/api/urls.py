from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet  # noqa

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
router.register(
    'recipes', RecipeViewSet, basename='recipes'
)
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
    path('auth/', include('djoser.urls.authtoken')),
]
