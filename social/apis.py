from libs.http import render_json
from social import logics
from user.models import User
from social.models import Friend
from vip.logics import require_permission


def rcmd_users(request):
    '''推荐用户接口'''
    users = logics.rcmd(request.uid)
    # rcmd_data = [user.to_dict() for user in users]
    rcmd_data = []
    for user in users:
        d = user.to_dict()
        d['describe'] = user.profile.describe
        rcmd_data.append(d)
    return render_json(rcmd_data)


def like(request):
    '''右滑：喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched = logics.like_someone(request.uid, sid)
    return render_json({'is_matched': is_matched})


@require_permission('superlike')
def superlike(request):
    '''上滑：超级喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched = logics.superlike_someone(request.uid, sid)
    return render_json({'is_matched': is_matched})


def dislike(request):
    '''左滑：不喜欢'''
    sid = int(request.POST.get('sid'))
    logics.dislike_someone(request.uid, sid)
    return render_json()


@require_permission('rewind')
def rewind(request):
    '''
    反悔操作

    传参处理:
        1. 客户端传来的任何东西都不可信
        2. 所有客户端传来的东西，都需要经过验证才可以使用
        3. 能不依赖客户端的数据，尽量不让客户端传
    '''
    result = logics.rewind_swipe(request.uid)
    print(result)
    return render_json({'rewind_times':result[0],'rewind_count':result[1]})


@require_permission('who_liked_me')
def who_liked_me(request):
    '''查看谁喜欢过自己'''
    users = logics.users_liked_me(request.uid)
    result = [user.to_dict() for user in users]
    return render_json(result)


def friend_list(request):
    '''查看自己的好友列表'''
    fid_list = Friend.friend_id_list(request.uid)
    friends = User.objects.filter(id__in=fid_list)
    result = [frd.to_dict() for frd in friends]
    return render_json(result)

def remove_friend(request):
    '''删除好友'''
    friend_id = int(request.GET.get('friend_id'))
    print(friend_id)
    Friend.break_off(request.uid,friend_id)
    return render_json()

def hot_rank(request):
    '''查看人气排行榜'''
    rank_data = logics.get_top_n(50)
    return render_json(rank_data)
