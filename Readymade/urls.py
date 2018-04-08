from django.urls import path
from Readymade.TfidfVectorizer import getWords,search
urlpatterns = [
    path(r'TF',getWords, name='TF'),
    path(r'search',search, name='search'),
]