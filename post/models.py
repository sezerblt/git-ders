from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from captcha.fields import ReCaptchaField
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey('auth.User',verbose_name='Yazar',on_delete=models.CASCADE,related_name='posts')
    title = models.CharField(max_length=100,verbose_name='Baslik')
    content = RichTextField(verbose_name='Icerik')
    pub_date = models.DateTimeField(verbose_name='Yayinlama tarihi',auto_now_add=True)
    image = models.FileField(null=True,blank=True)
    slug = models.SlugField(unique=True,editable=False,max_length=120)

    class Meta:
        ordering=['-pub_date','id']

    def __str__(self):
        return self.title

    def get_unique_slug(self):
        slug = slugify(self.title.replace('ı','i'))
        unique_slug = slug
        counter = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = ' {}-{}'.format(slug,counter)
            counter +=1
        return unique_slug




    def get_absolute_url(self):
        return reverse('post_apps:detail',kwargs={'slug':self.slug})

    def get_create_url(self):
        return reverse('post_apps:create')

    def save(self,*args,**kwargs):
        self.slug = self.get_unique_slug()
        return super(Post,self).save(*args,**kwargs)

    def get_update_url(self):
        return reverse('post_apps:update',kwargs={'slug':self.slug})

    def get_delete_url(self):
        return reverse('post_apps:delete',kwargs={'slug':self.slug})

class Comment(models.Model):
    post = models.ForeignKey('post.Post',on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80,verbose_name='isim')
    content = models.TextField(verbose_name='Yorum')
    created_date = models.DateTimeField(auto_now_add=True)

