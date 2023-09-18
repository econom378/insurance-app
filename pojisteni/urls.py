from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [

    path('policyholders/', views.policyholders, name="policyholder_list"),
    path("<int:pk>/policiholder_detail/", views.policyholder_detail,
         name="policyholder_detail"),
    path("create_policyholder/", views.create_policyholder,
         name="create_policyholder"),
    path("<int:pk>/update_policyholder/", views.update_policyholder,
         name="update_policyholder"),
    path("<int:pk>/delete_policyholder/", views.delete_policyholder,
         name="delete_policyholder"),
    path('insurances/', views.insurances, name="insurance_list"),
    path("<int:pk>/insurance_detail/", views.insurance_detail,
         name="insurance_detail"),
    path("<int:pk>/create_insurance/", views.create_insurance,
         name="create_insurance"),
    path("<int:pk>/update_insurance/", views.update_insurance,
         name="update_insurance"),
    path("<int:pk>/delete_insurance/", views.delete_insurance,
         name="delete_insurance"),
    path('events/', views.events, name="event_list"),
    path("<int:pk>/event_detail/", views.event_detail,
         name="event_detail"),
    path("<int:pk>/create_event/", views.create_event,
         name="create_event"),
    path("<int:pk>/update_event/", views.update_event,
         name="update_event"),
    path("<int:pk>/delete_event/", views.delete_event,
         name="delete_event"),

    path("login/", views.user_login, name="login"),
    path("register/", views.user_register, name="register"),
    path("logout/", views.user_logout, name="logout"),

    path("pdf-report/", views.render_pdf_view, name="pdf_report"),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
