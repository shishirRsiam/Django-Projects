from . models import *


def get_most_viewed_post():
    post = Post.objects.order_by('-views')[:10]
    return post

def get_post_by_page(page_no): 
    start_id = (page_no - 1) * 8
    end_id = (start_id + 8) 
    print('(*)'*20)
    print(start_id, end_id)
    print('(*)'*20)
    post = Post.objects.order_by('-id')[start_id : end_id]
    return post