from rest_framework import serializers
from watchlist.models import WatchList,StreamPlatform,Reviews
class ReviewSerializers(serializers.ModelSerializer):
      review_user=serializers.StringRelatedField(read_only=True)
      class Meta:
          model=Reviews
      #     fields= "__all__"
          exclude=('watchlist',)
class WatchSerializers(serializers.ModelSerializer):
      reviews=ReviewSerializers(many=True,read_only=True)
      platform=serializers.CharField(source="platform.name")
      class Meta:
          model=WatchList
          fields= "__all__"
class StreamPlatformSerializers(serializers.HyperlinkedModelSerializer):
      watchlist=WatchSerializers(many=True,read_only=True)#for Acessing complete data of watchlist
      # watchlist=serializers.StringRelatedField(many=True)#it return string name that we define in watchlist model class
      class Meta:
            model=StreamPlatform
            fields= "__all__"
