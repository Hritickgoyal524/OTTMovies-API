from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from watchlist.app.permissions import IsReviewORReadonly,IsAdminORReadonly
from rest_framework.permissions import IsAuthenticated
# from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from watchlist.models import WatchList,StreamPlatform,Reviews
from watchlist.app.serializers import WatchSerializers,StreamPlatformSerializers,ReviewSerializers

# Create your views here.
# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset=Reviews.objects.all()
#     serializer_class=ReviewSerializers
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)

class Reviewlistcreate(generics.CreateAPIView):
    serializer_class=ReviewSerializers
    def get_queryset(self):
        return Reviews.objects.all()
    permission_classes=[IsAuthenticated]
    def perform_create(self,serializer):
        pk=self.kwargs.get('pk')
        watchlist=WatchList.objects.get(pk=pk)
        print(self.request.user)
        review_user=self.request.user
        review_queryset=Reviews.objects.filter(watchlist=watchlist,review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("You have already review this watch!!")
        if watchlist.num_rating==0:
            watchlist.avg_rating=serializer.validated_data['rating']
        else:
           watchlist.avg_rating=(serializer.validated_data['rating']+ watchlist.avg_rating)/2
        watchlist.num_rating=watchlist.num_rating+1
        watchlist.save()
        serializer.save(watchlist=watchlist,review_user=review_user)
class ReviewList(generics.ListAPIView):#concreate Generic Apiview
    #   queryset=Reviews.objects.all()
      serializer_class=ReviewSerializers
    #   throtlle_classes=[AnoneRateThrottle]#it is object level throtling
    #   permission_classes=[IsAuthenticated]
      filter_backends=[DjangoFilterBackend]
      filterset_fields=['review_user__username','active']
      def get_queryset(self):
          pk=self.kwargs['pk']#filter 
          return Reviews.objects.filter(watchlist=pk)
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
      queryset=Reviews.objects.all()
      permission_classes=[IsReviewORReadonly]
      serializer_class=ReviewSerializers




class StreamplatformAPI(APIView):
        permission_classes=[IsAdminORReadonly]
        def get(self,request):
            platform=StreamPlatform.objects.all()
            serializer=StreamPlatformSerializers(platform,many=True,context={"request":request})
            return Response(serializer.data)
        def post(self,request):
            serializer=StreamPlatformSerializers(data=request.data,context={"request":request})
            if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
            else:
               return Response(serializer.errors)
class WatchListAPI(APIView):
    permission_classes=[IsAdminORReadonly]
    def get(self,request):
        movie=WatchList.objects.all()
        serializer=WatchSerializers(movie,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=WatchSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
class WatchDetailAPI(APIView):
    permission_classes=[IsAdminORReadonly]
    def get(self,request,pk):
        try:
            movie=WatchList.objects.get(pk=pk)
        except movie.DoesNotExists:
               return Response({'error':"Movie not found"},status=status.HTTP_404_NOT_FOUND)
        serializer=WatchSerializers(movie)
        return Response(serializer.data)
    def put(self,request,pk):
        movie=WatchList.objects.get(pk=pk)
        serializer=WatchSerializers(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serilizer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        movie=WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class StreamDetailAPI(APIView):
    permission_classes=[IsAdminORReadonly]
    def get(self,request,pk):
        try:
            platform=StreamPlatform.objects.get(pk=pk)
            
        except platform.DoesNotExists:
               return Response({'error':"Platform not found"},status=status.HTTP_404_NOT_FOUND)
        serializer=StreamPlatformSerializers(platform,context={"request":request})
        return Response(serializer.data)
    def put(self,request,pk):
        platform=StreamPlatform.objects.get(pk=pk)
        serializer=StreamPlatformSerializers(platform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        platform=StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



