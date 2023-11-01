
from rest_framework import serializers
from .models import Comment, Post,Like

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model =Like
        fields = '__all__'
        

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model =Post
        fields ='__all__'


class PostPackSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta :
        model = Post
        fields= '__all__'

    def get_like(self, obj):
        return Like.objects.filter(post_id=obj.id).count()
    def get_comments(self,obj):
        comments = Comment.objects.filter(post_id=obj.id)
        return CommentSerializer(comments, many=True).data
    

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'