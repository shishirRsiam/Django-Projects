from django.contrib import admin
from django.urls import path

from Post_App import views as PostAppViews
from Authenticator_App import views as AuthenticatorAppViews
from Categories_App import views as CategoriesAppViews

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', PostAppViews.home, name='home'),
    path('posts/<int:page_no>', PostAppViews.home_post_by_page, name='home_post_by_page'),
    path('add/post', PostAppViews.add_post, name='addpost'),
    path('post/<slug:url>/', PostAppViews.view_post, name='viewpost'),
    path('category/<slug:slug>/', PostAppViews.view_post_by_category, name='viewpostbycategory'),
    path('edit/<slug:slug_url>/', PostAppViews.edit_post, name='editpost'),
    path('delete/<slug:slug_url>/', PostAppViews.delete_post, name='deletepost'),

    path('add/category', CategoriesAppViews.add_categories, name='addcategory'),

    path('edit/profile', AuthenticatorAppViews.edit_profile, name='editprofile'),
    path('edit/password', AuthenticatorAppViews.change_password, name='changepassword'),
    path('login', AuthenticatorAppViews.login_page, name='login'),
    path('signup', AuthenticatorAppViews.signup_page, name='signup'),
    path('profile', AuthenticatorAppViews.profile, name='profile'), 
    path('logout', AuthenticatorAppViews.logout_page, name='logout'), 
]
