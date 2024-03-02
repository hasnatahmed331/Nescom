from rest_framework import serializers
from .models import UserProfile, Library, Event, EventUser, Resource, ResourceUser, Market, Community, CommunityMember, CommunityTopic, Topic, TopicUser, TopicActivity, Project, ProjectUser, ProjectChat , Likes

from rest_framework.authtoken.models import Token
class UserProfileSerializer(serializers.ModelSerializer):
     class Meta:
        model = UserProfile
        fields = '__all__'

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventUser
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class ResourceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceUser
        fields = '__all__'

class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__'

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'

class CommunityMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityMember
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class CommunityTopicSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(read_only=True)
    
    class Meta:
        model = CommunityTopic
        fields = '__all__'

class TopicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicUser
        fields = '__all__'

class TopicActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicActivity
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ProjectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = '__all__'

class ProjectChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectChat
        fields = '__all__'

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'