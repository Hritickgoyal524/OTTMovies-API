from django.urls import path,include
from watchlist.app.views import (WatchListAPI,ReviewList,StreamplatformAPI,WatchDetailAPI,StreamDetailAPI,ReviewDetail

,Reviewlistcreate)

urlpatterns = [
    path('stream', StreamplatformAPI.as_view(),name='streams-detail'),
    path('stream/<int:pk>', StreamDetailAPI.as_view(),name='streamplatform-detail'),
    path('<int:pk>', WatchDetailAPI.as_view(),name='movie'),
    path('list', WatchListAPI.as_view(),name='movie-details'),
    path('<int:pk>/review-create/', Reviewlistcreate.as_view(),name='review-create'),
    path('stream/<int:pk>/review',ReviewList.as_view(),name="review_list"),
    path('stream/review/<int:pk>',ReviewDetail.as_view(),name="review_details")
]

