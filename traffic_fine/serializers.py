from rest_framework import serializers
from traffic_fine.models import *

class TrafficFineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficFineCategory
        fields = ('id','name')

class TrafficFineCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficFineCity
        fields = ('id','name')

class TrafficFineSerializer(serializers.ModelSerializer):
    category = TrafficFineCategorySerializer(many=False, read_only=True)
    city = TrafficFineCitySerializer(many=False, read_only=True)
    class Meta:
        model = TrafficFine
        fields = ('traffic_offense','category','city','simplified','fine_first_offense','jail_first_offense','fine_second_offense','jail_second_offense','hyperlink')
