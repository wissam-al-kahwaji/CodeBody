from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Count,F
from django.contrib.auth import authenticate , login ,logout
from .models import Discussion, Comments, Topic, User, Rank, notification, Rank_history, CodeCoin_history
from .forms import DiscussionForm, MyUserCreationForm,EditUser,EditPortfolio
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth import authenticate, update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import StreamingHttpResponse
from .MyFunction import ReSizeImages
import markdown2
import time
import json
import uuid


# Variable
Error_validity = {'Error':'You are not authorized to enter here',}

@login_required(login_url='login')
def Data_notification(request):
    def notificationSSE():
        user = User.objects.get(username=request.user.username)
        while True:
            time.sleep(3)
            noti_all = notification.objects.filter(user=request.user)
            noti_read = noti_all.filter(read=False).count()
            if noti_read != 0:
                data = {
                    "noti_read":noti_read,
                        }
            else :
                data = ''
            if user.display_notification == True:
                noti_send = noti_all.filter(send=False)
                noti_first = noti_send.first()
                if noti_first:
                    noti_title = noti_first.title
                    noti_url = noti_first.url
                    noti_first.send = True
                    noti_first.save()
                    data = {
                    "notification": noti_title,
                    "notification_url": noti_url,
                    "noti_read":noti_read,
                    }

                
            yield 'data: %s\n\n' % json.dumps(data)

    return StreamingHttpResponse(notificationSSE(), content_type='text/event-stream')


@login_required(login_url='login')
def Data_discussion(request,pk):
    dis = Discussion.objects.get(id=pk)
    tmp = Comments.objects.filter(discussion=dis).count()
    def discussionSSE():
        Old = tmp
        while True:
            time.sleep(3)            
            data = ''
            NEW = Comments.objects.filter(discussion=dis).count()
            if NEW != Old:
                Old = NEW 
                data = {'status':True,}
                
            yield 'data: %s\n\n' % json.dumps(data)

    return StreamingHttpResponse(discussionSSE(), content_type='text/event-stream')


@login_required(login_url='login')
def Data_home(request):
    def homeSSE():
        tmp = Discussion.objects.count()
        while True:
            time.sleep(3)
            data = ''
            discussion = Discussion.objects.count()
            if discussion != tmp:
                tmp = discussion
                data = {'status':'True'}

                
            yield 'data: %s\n\n' % json.dumps(data)

    return StreamingHttpResponse(homeSSE(), content_type='text/event-stream')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topic = request.GET.get('topic') if request.GET.get('topic') != None else ''
    TopRank = Rank.objects.all()[0:3]
    form = DiscussionForm()
    
    discussions = Discussion.objects.filter(
        Q(topic__name__icontains=topic),
        Q(title__icontains=q)|
        Q(name__username__icontains=q)|
        Q(topic__name__icontains=q),)
    
    TopDiscussion = discussions.annotate(CountComments=Count('comments')).order_by('-CountComments')[0:3] 
    ranks = Rank.objects.all()
    discussion_count = discussions.count()
    topics = Topic.objects.annotate(discussion_count=Count('discussion')).order_by('-discussion_count')
    
    paginator = Paginator(discussions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
            'topic':topic,
            'q':q,
            'form': form,
            'discussions': page_obj,
            'topics':topics,
            'discussion_count':discussion_count,
            'ranks':ranks,
            'TopRank':TopRank,
            'TopDiscussion':TopDiscussion,
            }
    return render(request, 'base/home.html', context)


def RegisterPage(request):
    page = 'Register'
    form = MyUserCreationForm()
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else :
            messages.error(request, 'An error occured during registeration')
    context = {'page':page, 'form':form}
    return render(request, 'base/login_register.html',context)


def LoginPage(request):
    page = 'Login'

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username is incorrect')
            context = {'page':page}
            return render(request, 'base/login_register.html',context)

        user = authenticate(request, username=username, password=password)

        if user == None:
            messages.error(request, 'password is incorrect')


        if user is not None:
            login(request, user)
            return redirect('home')

    context = {'page':page}
    return render(request, 'base/login_register.html',context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def Profile(request,pk):
    user = User.objects.get(username=pk)
    discussions = user.discussion_set.all()
    rank = Rank.objects.get(user=user)
    tab = request.GET.get("tab") if request.GET.get("tab") != None else ''
    page = request.GET.get('page')
    if page != None:
        tab = 'Discussions'

    GitHubLike = False
    if tab == 'Projects':
        if user.github:
            GitHubLike = f"https://api.github.com/users/{user.github}/repos"

    discussion_count = discussions.count()
    followers = user.followers
    is_Follow = False
    if request.user.is_authenticated:
        is_Follow = user.followers.filter(username=request.user.username).exists()
    follow = User.objects.filter(followers=user)
    paginator = Paginator(discussions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    portfolio = markdown2.markdown(user.portfolio,
                                    extras=["html-classes","spoiler","tg-spoiler","markdown-extras","tag-friendly",
                                            "task_list","target-blank-links","fenced-code-blocks",
                                            "footnotes", "tables", "smarty-pants", "toc", "strike", "code-friendly", "cuddled-lists",
                                            "header-ids", "metadata", "xml", "footnotes-in-place", "math-text", "underline", "code-color"], safe_mode="escape")
    context = {
        'tab':tab,
        'portfolio':portfolio,
        'rank':rank,
        'user':user,
        'discussions':page_obj,
        'followers':followers,
        'follow':follow,
        'is_Follow':is_Follow,
        'discussion_count':discussion_count,
        'GitHubLike':GitHubLike,
        }
    return render(request, 'base/profile.html',context)


@login_required(login_url='login')
def discussion(request, pk):
    discussion = Discussion.objects.get(id=pk)
    Topic_discussion = Discussion.objects.all().order_by('-Viewss').exclude(id=pk)[0:5]

    if request.user.is_authenticated and request.method == 'GET':
        discussion.Viewss.add(request.user)

    is_Like = False
    is_DisLike = False
    if request.user.is_authenticated:
        is_Like = discussion.Likes.filter(username=request.user.username).exists()
        is_DisLike = discussion.disLikes.filter(username=request.user.username).exists()

    content = markdown2.markdown(discussion.content,
                                    extras=["html-classes","spoiler","tg-spoiler","markdown-extras","tag-friendly",
                                            "task_list","target-blank-links","fenced-code-blocks",
                                            "footnotes", "tables", "smarty-pants", "toc", "strike", "code-friendly", "cuddled-lists",
                                            "header-ids", "metadata", "xml", "footnotes-in-place", "math-text", "underline", "code-color"], safe_mode="escape")

    context = {
        'discussion': discussion,
        'Topic_discussion': Topic_discussion,
        'content':content,
        'is_Like':is_Like,
        'is_DisLike':is_DisLike,
    }
    return render(request, 'base/discussion.html', context)


@login_required(login_url='login')
def updateDiscussion(request, pk):
    discussion = Discussion.objects.get(id=pk)
    form = DiscussionForm(instance=discussion)
    topics = Topic.objects.all()
    if request.user != discussion.name:
        return redirect('home')

    if request.method == 'POST':
        form = DiscussionForm(request.POST, instance=discussion)
        if form.is_valid():
            topic_name = request.POST.get('topic')
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            if len(topic_name) > 20 or len(topic_name) < 3 or len(title) < 10 or len(content) < 50 :
                return redirect('home')
            topic, created = Topic.objects.get_or_create(name=topic_name)
            discussion.name = request.user
            discussion.topic = topic
            discussion.description = form.cleaned_data.get('description')
            discussion.save()
            return redirect('discussion', pk=pk)

    context = {'form': form, 'topics': topics, 'discussion': discussion}
    return render(request, 'base/discussion_form.html', context)


@csrf_exempt
@login_required(login_url='login')
def deleteDiscussion(request, pk):
    if request.method =='POST':
        discussion = Discussion.objects.get(id=pk)
        if request.user != discussion.name:
            return JsonResponse({'success': False})     
        discussion.delete()
        return JsonResponse({'success': True})


@login_required(login_url='login')
def deleteCommints(request, pk):
    comments = Comments.objects.get(id=pk)
    if request.user != comments.user:
        return redirect('home')#ibackforthis        
    if request.method =='POST':
        comments.delete()
        return redirect('home')#ibackforthis
    return render(request, 'base/delete.html', {'obj':comments})


@login_required(login_url='login')
def Settings(request, pk):
    user = request.user
    form_EditUser = EditUser(instance=user)
    form_EditPortfolio = EditPortfolio(instance=user)

    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        form_EditUser = EditUser(request.POST, instance=user)
        form_EditPortfolio = EditPortfolio(request.POST,instance=user)
        if form_EditPortfolio.is_valid():
            user = form_EditPortfolio.save(commit=False)
            user.save()
            return redirect('profile', pk=request.user.username)
        if avatar:
            avatarBig = ReSizeImages(avatar,300,300)
            avatarSmall = ReSizeImages(avatar,150,150)
            avatarBigName = str(uuid.uuid4()) + '.png'
            avatarSmallName = str(uuid.uuid4()) + '.png'
            user.avatar.save(avatarBigName, avatarBig, save=True)
            user.smallavatar.save(avatarSmallName, avatarSmall, save=True)
        if form_EditUser.is_valid():
            user = form_EditUser.save(commit=False)
            user.save()
            messages.success(request, 'Profile updated successfully')
            status=True
            context = {'pk':pk,'form_EditUser':form_EditUser,'status':status}
            return render(request, 'base/Settings.html', context)
        else:
            messages.error(request, 'An error occurred while updating the profile')

    context = {'pk':pk,
            'form_EditUser':form_EditUser,
            'form_EditPortfolio':form_EditPortfolio,
        }
    return render(request, 'base/Settings.html', context)


@csrf_exempt
@login_required(login_url='login')
def ChangePassword(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        user = authenticate(username=request.user.username, password=old_password)
        if user is not None:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return JsonResponse({'status': True})
        else:
            return JsonResponse({'status': False})
    else:
        return redirect('home')


#IBACK FOR THIS
        # user = request.user
        # rank = Rank.objects.get(user=user)
        # rank.respect += 500
        # rank.update_rank()
        # rank.save()

@csrf_exempt
@login_required(login_url='login')
def createDiscussion(request):
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        if len(request.POST.get('title')) > 100 or len(request.POST.get('title')) < 10 or len(request.POST.get('content')) > 20000 or len(request.POST.get('content')) < 50 or len(topic_name) > 20 or len(topic_name) < 3 :
            return JsonResponse({'success': False})
        
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Discussion.objects.create(
            name=request.user,
            topic=topic,
            title=request.POST.get('title'),
            content=request.POST.get('content'),
        )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@csrf_exempt
@login_required(login_url='login')
def Followers(request):
    if request.method == 'POST':
        target = request.POST.get("target")
        Follow_UnFollow = request.POST.get("status")
        user_follow = User.objects.get(username=target)
        if user_follow == request.user:
            return JsonResponse({'success': False})
        if Follow_UnFollow == "Follow":
            user_follow.followers.add(request.user)
            return JsonResponse({'success': True})
        if Follow_UnFollow == "UnFollow":
            user_follow.followers.remove(request.user)
            return JsonResponse({'success': True})
    return JsonResponse(Error_validity, safe=False)

@csrf_exempt
@login_required(login_url='login')
def Search(request):
    if request.method == 'POST':
        input = request.POST.get('input')
        topics = Topic.objects.filter(name__icontains=input)[:3]
        discussion = Discussion.objects.filter(title__icontains=input)[:3]
        user = User.objects.filter(username__icontains=input)[:3]    
        context = {
        'topics': list(topics.values()),
        'discussions': list(discussion.values()),
        'users': list(user.values()),
        }
        
        return JsonResponse(context)
    return JsonResponse(Error_validity, safe=False)


@csrf_exempt
@login_required(login_url='login')
def topic_list(request):
    input = request.GET.get('input')
    topics = Topic.objects.filter(name__icontains=input)[:5]

    context = {
    'topics': list(topics.values()),
    }
    return JsonResponse(context)


@csrf_exempt
@login_required(login_url='login')
def Notification(request):
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 5))
    noti = notification.objects.filter(user=request.user)
    noti.update(send=True)
    noti.update(read=True)
    noti_count = noti.count()
    
    if noti_count < 5 and start == 0:
        end = noti_count
        noti = list(noti.values())[start:end]
        return JsonResponse(noti, safe=False)

    if noti_count < end and noti_count > start -1 :
        start = noti_count - 1
        end = noti_count + 1
    noti = list(noti.values())[start:end]

    if not noti or noti_count < start :
        data = {'error':'NotData'}
        return JsonResponse(data, safe=False)

    return JsonResponse(noti, safe=False)


def topic(request):
    topic = Topic.objects.annotate(discussions=Count('discussion')).values('name', 'discussions').order_by('-discussions')
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 5))
    topic_count = topic.count()
    if topic_count < 10 and start == 0:
        end = topic_count
        topic = list(topic.values())[start:end]
        return JsonResponse(topic, safe=False)

    if topic_count < end and topic_count > start - 1 :
        start = topic_count - 1
        end = topic_count + 1

    if not topic or topic_count < start :
        data = {'error':'NotData'}
        return JsonResponse(data, safe=False)

    topic = list(topic.values())[start:end]
    return JsonResponse(topic, safe=False)


@csrf_exempt
@login_required(login_url='login')
def comments(request,pk):
    if request.method == 'POST':
        comments = Comments.objects.filter(discussion=pk)
        start = int(request.POST.get('start') or 0)
        end = int(request.POST.get('end') or (start + 10))

        comments_count = comments.count()
        if comments_count < 10 and start == 0:
            end = comments_count
            DoneComments = comments.values('body', 'created').annotate(rank=F('user__ranks__rank'),img=F('user__smallavatar'),FName=F('user__first_name'),LName=F('user__last_name'),username=F('user__username'))[start:end]            
            return JsonResponse(list(DoneComments), safe=False)

        if comments_count < end and comments_count > start - 1 :
            start = comments_count - 1
            end = comments_count + 1

        if not comments or comments_count < start :
            data = {'error':'NotData'}
            return JsonResponse(data, safe=False)


        DoneComments = comments.values('body', 'created').annotate(rank=F('user__ranks__rank'),img=F('user__smallavatar'),FName=F('user__first_name'),LName=F('user__last_name'),username=F('user__username'))[start:end]

        return JsonResponse(list(DoneComments), safe=False)
    return JsonResponse(Error_validity, safe=False)
    

@csrf_exempt
@login_required(login_url='login')
def CreateComment(request,pk):    
    if request.method == 'POST':
        input = request.POST.get('InputComment');
        discussion = Discussion.objects.get(id=pk)
        if len(input) > 1000 or discussion == None :
            status = {'status':'False'}
            return JsonResponse(status, safe=False)

        Comments.objects.create(
            user=request.user,
            discussion=discussion,
            body=input
        )
        if request.user != discussion.name:
            noti = f'You have a New Comment on {discussion.title}'
            oldnotification = notification.objects.filter(title=noti)
            
            if oldnotification.exists():
                oldnotification.delete()

            notification.objects.create (
            user= discussion.name,
            title= noti, 
            url= f'/discussion/{discussion.id}',)

        status = {'status':'True'}
        return JsonResponse(status, safe=False)

    return JsonResponse(Error_validity, safe=False)


@csrf_exempt
@login_required(login_url='login')
def CreateReact(request,pk):    
    if request.method == 'POST':
        discussion = Discussion.objects.get(id=pk)
        Like = request.POST.get('Like');
        DisLike = request.POST.get('DisLike');
        is_Like = False 
        is_DisLike = False
        if Like == 'Like':
            is_Like = discussion.Likes.filter(username=request.user.username).exists()
            is_DisLike = discussion.disLikes.filter(username=request.user.username).exists()
            if is_DisLike == True:
                discussion.disLikes.remove(request.user)
                discussion.Likes.add(request.user)
            if is_Like == False :
                discussion.Likes.add(request.user)
            if is_Like == True :
                discussion.Likes.remove(request.user)

            status = {'status':'True'}
            return JsonResponse(status, safe=False)

        if DisLike == 'DisLike':
            is_Like = discussion.Likes.filter(username=request.user.username).exists()
            is_DisLike = discussion.disLikes.filter(username=request.user.username).exists()
            if is_Like == True:
                discussion.Likes.remove(request.user)
                discussion.disLikes.add(request.user)
            if is_DisLike == False :
                discussion.disLikes.add(request.user)
            if is_DisLike == True :
                discussion.disLikes.remove(request.user)

            status = {'status':'True'}
            return JsonResponse(status, safe=False)

    return JsonResponse(Error_validity, safe=False)


@csrf_exempt
def ChackUsername(request):
    if request.method == 'POST':
        input = request.POST.get('input')
        user = User.objects.filter(username=input)
        if user.count() != 0:
            status= {'status':'false'}
            return JsonResponse(status, safe=False)
        if user.count() == 0 :
            status= {'status':'true'}
            return JsonResponse(status, safe=False)
        
    return JsonResponse(Error_validity, safe=False)


@csrf_exempt
def ChackEmail(request):
    if request.method == 'POST':
        input = request.POST.get('input')
        email = User.objects.filter(email=input)
        if email.count() != 0:
            status= {'status':'false'}
            return JsonResponse(status, safe=False)
        if email.count() == 0 :
            status= {'status':'true'}
            return JsonResponse(status, safe=False)
        

    return JsonResponse(Error_validity, safe=False)
