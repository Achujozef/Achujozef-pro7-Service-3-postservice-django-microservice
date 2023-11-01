from django.shortcuts import render
from .serializer import *
from .models import *
from rest_framework import status,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response


class PostViewSet(viewsets.ViewSet):
    '''
    this view set is for Intracting with the post
    '''
    def list (self, request):
        queryset = Post.objects.all()
        serializer= PostSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Listing The Post of a doctor
    def list_by_doctor(self,request, doctor_id): #http://localhost:8000/api/posts/by-doctor/2/
        try:
            queryset=Post.objects.filter(doctor_id=doctor_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)
    #delete a post
    def destroy(self,request, pk =None):    #http://localhost:8000/api/posts/1/
        try:
            queryset= Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Like.objects.filter(post_id=pk).delete()
        Comment.objects.filter(post_id=pk).delete()
        queryset.delete()
        return Response ( status= status.HTTP_204_NO_CONTENT)

class PostList(APIView):   
    #all Post For the USer (Global)
    def get(self, request): #http://localhost:8000/api/packeposts/?user_id=1
        posts = Post.objects.all()
        serializer = PostPackSerializer(posts, many=True)
        # user_id = request.user.id  
        user_id = request.query_params.get('user_id')
        liked_posts = Like.objects.filter(user_id=user_id).values_list('post_id', flat=True)
        data = []
        for post_data in serializer.data:
            post_data['liked'] = post_data['id'] in liked_posts
            data.append(post_data)
        return Response(data)
    
class LikeDislikeView(APIView):    
    #Like And dislike Post
    def post(self, request, post_id): #http://localhost:8000/api/posts/1/like-dislike/?user_id=1
        #user_id = request.user.id
        user_id = request.query_params.get('user_id')
        try:
            like = Like.objects.get(user_id=user_id, post_id=post_id)
            like.delete()  
            return Response({'message': 'Disliked'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            Like.objects.create(user_id=user_id, post_id=post_id)
            return Response({'message': 'Liked'}, status=status.HTTP_201_CREATED)

class CommentView(APIView):
    #post comments For User
    def post(self, request, post_id): #http://localhost:8000/api/posts/1/create-comment/?user_id=1
        #user_id = request.user.id  
        user_id = request.query_params.get('user_id')
        text = request.data.get('text')  
        try:
            comment = Comment.objects.create(user_id=user_id, post_id=post_id, text=text)
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    #Delete comments For User
    def delete(self, request, comment_id): #http://localhost:8000/api/comments/6/
        try:
            comment = Comment.objects.get(pk=comment_id)
            comment.delete()
            return Response({'message':'Comment deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response({'message': 'Comment not Found'}, status=status.HTTP_404_NOT_FOUND)