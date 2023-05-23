from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    GENDER_CHOICES = [('M', 'Male'),('F', 'Female')]
    username_validator = RegexValidator(regex=r'^[A-Za-z0-9-]{3,}$', message='The Username must contain only lowercase letters and English numbers and you can use: "-". It must be at least 3 characters long.',)
    username = models.CharField(max_length=30, unique=True, validators=[username_validator],)
    first_name = models.CharField(max_length=15, null=True, blank=False)
    last_name = models.CharField(max_length=15, null=True, blank=False)
    email = models.EmailField(unique=True, null=True, blank=False)
    bio = models.TextField(max_length=255, blank=False,default="Hello, World")
    portfolio = models.TextField(blank=False,max_length=5000 ,null=True, default="# Hello, World")
    display_notification = models.BooleanField(default=True)
    github = models.CharField(max_length=100,blank=True,null=False)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    birth_date = models.DateField(null=True, blank=True)
    Use_code  = models.CharField(max_length=50, null=True, blank=True)
    Job = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    CodeCoin = models.IntegerField(default=0)
    avatar = models.ImageField(null=True, default="avatar.svg")
    smallavatar = models.ImageField(null=True, default="avatar.svg")
    


    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    @property
    def rank(self):
        rank = Rank.objects.filter(user=self).first()
        if rank:
            return rank
        return None


class Topic(models.Model):
    name = models.CharField(max_length=20)


    def __str__(self):
        return self.name


class Discussion(models.Model):
    name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) 
    topic = models.ForeignKey(Topic,max_length=20, on_delete=models.CASCADE, null=True)
    use_commints = models.BooleanField(default=True)
    Viewss = models.ManyToManyField(User,related_name='Viewss', blank=True)
    Likes = models.ManyToManyField(User, related_name='liked_posts', related_query_name='liked_post', blank=True)
    disLikes = models.ManyToManyField(User, related_name='disliked_posts', related_query_name='disliked_post', blank=True)
    title = models.CharField(max_length=100,blank=False)
    content = models.TextField(max_length=5000, blank=False, null=True )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    @property
    def rank(self):
        rank = Rank.objects.filter(user=self.name).first()
        if rank:
            return rank.rank
        return None


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    body = models.TextField(max_length=1000,blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.body[0:50]


class Rank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ranks')
    respect = models.IntegerField(default=0)
    rank = models.CharField(max_length=50, blank=True, null=True)
    Logo_rank = models.ImageField(null=True, default="Rank/BronzeIII.svg")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ['-respect']

    from .RankList import update_rank
    

@receiver(post_save, sender='auth.User')
def update_user_rank(sender, instance, created, **kwargs):
    if created:
        rank = Rank(user=instance)
    else:
        rank = instance.ranks.first()
    rank.respect = instance.profile.respect
    rank.update_rank()
    rank.save()
    
    

@receiver(post_save, sender=User)
def create_user_rank(sender, instance, created, **kwargs):
    if created:
        rank = Rank(user=instance, respect=0)
        rank.update_rank()
        rank.save()
        instance.ranks.add(rank)
        

class Rank_history(models.Model):
    TYPE_RANK = [('Loss','Loss'),('Add','Add')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255,null=True, blank=False)
    OldRank = models.IntegerField(blank=False)
    NewRank = models.IntegerField(blank=False)
    points = models.IntegerField(blank=False)
    type = models.CharField(max_length=4,choices=TYPE_RANK, null=True, blank=False)
    read = models.BooleanField(default=False)
    send = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    
    
class CodeCoin_history(models.Model):
    TYPE_RANK = [('Loss','Loss'),('Add','Add')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255,null=True, blank=False)
    CodeCoinOld = models.IntegerField(blank=False)
    CodeCoinNew = models.IntegerField(blank=False)
    points = models.IntegerField(blank=False)
    type = models.CharField(max_length=4,choices=TYPE_RANK, null=True, blank=False)
    read = models.BooleanField(default=False)
    send = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']



class notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255,blank=False)
    url = models.CharField(max_length=100,blank=False)
    read = models.BooleanField(default=False)
    send = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
