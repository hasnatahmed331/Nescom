from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , unique=True)
    email = models.EmailField(max_length=200 , null=True)
    experience = models.TextField(null=True)
    interests = models.TextField(null=True)
    location = models.CharField(max_length=200 , null=True)
    joined_in_farming = models.BooleanField(default=False)
    joined_in_gardening = models.BooleanField(default=False)
    #image = models.ImageField()



class Library(models.Model):
    user = models.ForeignKey(UserProfile , on_delete=models.CASCADE)
    category = models.CharField(max_length=200 , null=False)
    article = models.TextField(null=True)

    #video


    
    



class Event(models.Model):
    category = models.CharField(max_length=200 , null=False)
 
    title = models.CharField(max_length=200 , unique=True, null=False) 
    
    description = models.TextField(null=True)
    date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


class EventUser(models.Model):
    user = models.ForeignKey(UserProfile , on_delete=models.CASCADE)
    event = models.ForeignKey(Event , on_delete=models.CASCADE)
    type = models.CharField(max_length=200)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event.title

    class Meta:
        unique_together = ('user', 'event',)




class Resource(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200 , null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
   
  
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class ResourceUser(models.Model):
    user = models.ForeignKey(UserProfile , on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource , on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_sale = models.BooleanField(default=False)
    def __str__(self):
        return self.resource.name

    class Meta:
        unique_together = ('user', 'resource',)






class Market(models.Model):
    resource = models.ForeignKey(Resource , on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile , on_delete=models.CASCADE)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)



class Community(models.Model):
    category = models.CharField(max_length=200)
  


class CommunityMember(models.Model):
    user = models.ForeignKey(UserProfile , on_delete=models.CASCADE)
    community = models.ForeignKey(Community , on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.community.category
    class Meta:
        unique_together = ('user', 'community',)




class Topic(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class TopicUser(models.Model):
    user = models.ForeignKey(UserProfile , on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic , on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    started_by = models.BooleanField(default=False)
    




    def __str__(self):
        return self.topic.title
    
    class Meta:
        unique_together = ('user', 'topic',)


class TopicActivity(models.Model):
    topic = models.ForeignKey(Topic , on_delete=models.CASCADE)
    comment = models.TextField()
    
    date = models.DateTimeField(auto_now_add=True)


    user = models.ForeignKey(UserProfile , on_delete=models.CASCADE)

    def __str__(self):
        return self.topic.title

# class Topic_comment(models.Model):
#     pass

class Likes(models.Model):
    topic_activity = models.ForeignKey(TopicActivity , on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic.title

class CommunityTopic(models.Model):
    community = models.ForeignKey(Community , on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic , on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Project(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    description = models.TextField()
    category = models.CharField(max_length=200)
   

class ProjectUser(models.Model):
    user = models.ForeignKey(UserProfile , on_delete=models.CASCADE)
    project = models.ForeignKey(Project , on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    is_collaborator = models.BooleanField()
    is_owner = models.BooleanField()

    def __str__(self):
        return self.project.title

    class Meta:
        unique_together = ('user', 'project',)


class ProjectChat(models.Model):

    project = models.ForeignKey(Project , on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile , on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project.title





