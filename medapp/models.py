from django.db import models
from django.contrib.auth import get_user, get_user_model
from medapp.utils import *
from datetime import datetime
from django.urls import reverse


class BaseMixin(models.Model):
    slug = models.SlugField(unique=True,editable=False,blank=True,null=True)
    created_at = models.DateField(auto_now_add=True,blank=True,null=True,)
    updated_at = models.DateField(auto_now=True,blank=True,null=True,)
    
    class Meta:
        abstract = True
    

class Category(BaseMixin):
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            count = 0
            while Category.objects.filter(slug=self.slug).exists():
                count += 1
                self.slug = f"{slugify(self.title)}-{count}"
        super().save(*args, **kwargs)


class Tag(models.Model):
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class Blog(BaseMixin):
    title = models.CharField(max_length=300)
    image = models.ImageField()
    content = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='categoryBlogs')
    tag = models.ManyToManyField(Tag,related_name='categoryBlogs')
    writer = models.CharField(max_length=500,null=True,blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            count = 0
            while Blog.objects.filter(slug=self.slug).exists():
                count += 1
                self.slug = f"{slugify(self.title)}-{count}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog', kwargs={"slug": self.slug})


class BlogSection(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='blogSections')
    title = models.CharField(max_length=300)
    image = models.ImageField(null=True,blank=True)
    image2 = models.ImageField(null=True,blank=True)
    content = models.TextField()

    def __str__(self):
        return self.title  


class Comment(models.Model):
    description = models.TextField(null=True,blank=True)
    full_name = models.CharField(max_length=400)
    phone_number = models.CharField(max_length=400,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='comments')
    date = models.DateField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.full_name  

  