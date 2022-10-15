from django.db import models
from django.contrib.auth.models import User
# Create your models here. Comment.objects.filter(post=best_post)
class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    rating = models.IntegerField(default=0)
    def update_rating(self):
        result_rating = 0
        for post in self.post_set.all():
            result_rating+=post.rating*3
            for comment in post.comment_set.all():
                result_rating+=comment.rating

        for comment in self.user.comment_set.all():
            result_rating+=comment.rating

        self.rating=result_rating
        self.save()
    def __str__(self):
        return f'name:{self.user.username} rating:{self.rating}'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

#Post.objects.create(author = )
class Post(models.Model):
    TYPES = [
        ('AR', 'Article'),
        ('NW', 'New')
    ]
    categories = models.ManyToManyField(Category, through='PostCategory')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2,choices=TYPES, default='AR')
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    updated_at = models.DateTimeField(auto_now=True,editable=True)
    header = models.CharField(max_length=96,default='default')
    text = models.TextField(default='default')
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating+=1
        self.save()
    def dislike(self):
        self.rating-=1
        self.save()

    def preview(self, length=124):
        return self.text[:length]+'...'





class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='default')
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=True)

    def like(self):
        self.rating+=1
        self.save()
    def dislike(self):
        self.rating-=1
        self.save()