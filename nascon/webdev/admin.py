from django.contrib import admin
from .models import UserProfile, Library, Event, EventUser, Resource, ResourceUser, Market, Community, CommunityMember, Topic, TopicUser, TopicActivity, Likes, CommunityTopic, Project, ProjectUser, ProjectChat

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Library)
admin.site.register(Event)
admin.site.register(EventUser)
admin.site.register(Resource)
admin.site.register(ResourceUser)
admin.site.register(Market)
admin.site.register(Community)
admin.site.register(CommunityMember)
admin.site.register(Topic)
admin.site.register(TopicUser)
admin.site.register(TopicActivity)
admin.site.register(Likes)
admin.site.register(CommunityTopic)
admin.site.register(Project)
admin.site.register(ProjectUser)
admin.site.register(ProjectChat)
