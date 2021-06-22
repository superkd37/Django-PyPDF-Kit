from django.urls import path
from . import views

app_name = 'pdf'

urlpatterns = [
    path('extract/single/', views.pdf_single_page_extract, name='pdf_single_page_extract'),
    path('extract/range/', views.pdf_range_extract, name='pdf_range_extract'),
    path('merge/', views.pdf_merge, name='pdf_merge'),
    path('replace/', views.pdf_replace, name='pdf_replace'),
]