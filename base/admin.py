from django.contrib import admin

# Register your models here.

from .models import Discussion, Topic, Comments, User,Rank,CodeCoin_history,Rank_history,notification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email' ,'github','gender','location','CodeCoin')
    search_fields = ('username','email','github',)
    list_per_page = 25


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('name','topic' ,'title','use_commints')
    search_fields = ('title',)
    ordering = ('-created',)
    list_per_page = 25

@admin.register(notification)
class notificationAdmin(admin.ModelAdmin):
    list_display = ('user','title','created','read')
    search_fields = ('user','title',)
    ordering = ('-created',)
    list_per_page = 25

@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ('user','rank','respect')
    search_fields = ('user',)
    ordering = ('-respect',)
    list_per_page = 25


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 25

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user','discussion','body','created',)
    search_fields = ('user','discussion','body')
    list_per_page = 25


admin.site.register(CodeCoin_history)
admin.site.register(Rank_history)

