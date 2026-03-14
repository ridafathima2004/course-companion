"""coursecompanion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('login/', views.login_get),
    path('login_post/', views.login_post),
    path('forgot_password_get/', views.forgot_password_get),
    path('forgot_password_post/', views.forgot_password_post),
    path('admin_home/', views.admin_home),
    path('cp_signup/', views.cp_signup),
    path('cp_signup_post/', views.cp_signup_post),
    path('admin_view_cp/', views.admin_view_cp),
    path('approve_cp/<id>', views.approve_cp),
    path('view_cp_approve/', views.view_cp_approve),
    path('reject_cp/<id>', views.reject_cp),
    path('view_cp_reject/', views.view_cp_reject),
    path('view_user/', views.view_user),
    path('view_cuser/', views.view_cuser),
    path('cp_home/',views.cp_home),
    path('view_ccp/', views.view_ccp),
    path('cp_change_password_get/',views.cp_change_password_get),
    path('cp_change_password_post/',views.cp_change_password_post),
    path('view_review/', views.view_review),
    path('view_cprofile/', views.view_cprofile),
    path('edit_cprofile/', views.edit_cprofile),
    path('edit_cprofile_post/', views.edit_cprofile_post),
    path('addc_cp/', views.addc_cp),
    path('addc_cp_post/', views.addc_cp_post),
    path('viewc_cp/', views.viewc_cp),
    path('admin_view_all_cp/',views.admin_view_all_cp),
    path('view_cp_review/',views.admin_view_cp_review),
    path('editc_cp_post/', views.editc_cp_post),
    path('removecourse/<cid>', views.removecourse),
    path('editc_cp/<cid>', views.editc_cp),
    path('viewcp_review/', views.viewcp_review),
    path('viewcp_req/', views.viewcp_req),
    path('approve_creq/<id>', views.approve_creq),
    path('reject_creq/<id>', views.reject_creq),
    path('video_cp/', views.video_cp),
    path('video_cp_post/', views.video_cp_post),
    path('cpview_video/', views.cpview_video),
    path('edit_video/<vid>', views.edit_video),
    path('edit_video_post/', views.edit_video_post),
    path('delete_video/<vid>', views.delete_video),

    path('material_cp/', views.material_cp),
    path('material_cp_post/', views.material_cp_post),
    path('cpview_material/', views.cpview_material),
    path('edit_material/<vid>', views.edit_material),
    path('edit_material_post/', views.edit_material_post),
    path('delete_material/<vid>', views.delete_material),

    path('login_out/', views.login_out),
    path('check/', views.check),
    path('admin_changepassword_get/',views. admin_changepassword_get),
    path('admin_changepassword_post/',views.admin_changepassword_post),
#     =====================USER============================
    path('user_signup/',views.user_signup),
    path('user_login/',views.user_login),
    path('app_forgot_password/',views.app_forgot_password),
    path('user_view_profile/',views.user_view_profile),
    path('user_edit_profile/',views.user_edit_profile),
    path('user_view_cp/',views.user_view_cp),
    path('user_view_offcourse/',views.user_view_offcourse),
    path('send_course_req/',views.send_course_req),
    # path('view_joined_course/',views.view_joined_course),
    path('user_review/',views.user_review),
    path('course_review/',views.course_review),
    path('view_creview/',views.view_creview),
    path('send_req/', views.send_req),
    path('req_status/',views.req_status),
    path('uview_video/',views.uview_video),
    path('uview_material/',views.uview_material),
    path('changepassword/',views.changepassword),
    path('chat_bot/',views.chat_bot),


]
