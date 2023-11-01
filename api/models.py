from django.db import models

# Create your models here.
class Post (models.Model):
    doctor_id = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='post_photos/')
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.title
class Like(models.Model):
    user_id= models.PositiveBigIntegerField()
    post_id= models.PositiveBigIntegerField()

    def __str__(self):
        return f"User ID {self.user_id} Liker Post {self.post_id}"
    
class Comment(models.Model):
    user_id=models.PositiveBigIntegerField()
    post_id = models.PositiveIntegerField()
    text= models.TextField()

    def __str__(self):
        return f"User Id {self.user_id} commented on {self.post_id}"
    

