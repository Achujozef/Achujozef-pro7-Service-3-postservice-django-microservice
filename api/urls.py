from django.urls import path
from .views import *

app_name = 'api'  

urlpatterns = [
    path('posts/', PostViewSet.as_view({'post': 'create'}), name='post-list'),
    path('posts/<int:pk>/', PostViewSet.as_view({'delete': 'destroy'}), name='post-detail'),
    path('posts/by-doctor/<int:doctor_id>/', PostViewSet.as_view({'get': 'list_by_doctor'}), name='post-list-by-doctor'),
    path('packeposts/', PostList.as_view(), name='post-list'),
    path('posts/<int:post_id>/like-dislike/', LikeDislikeView.as_view(), name='like-dislike'),
    path('posts/<int:post_id>/create-comment/', CommentView.as_view(), name='create-comment'),
    path('comments/<int:comment_id>/',CommentView.as_view(), name='delete-comment')
]

# http://localhost:8000/api/packeposts/?user_id=1