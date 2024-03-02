from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework import status
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from django.contrib.auth import authenticate , login , logout
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication , TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from .serializers import UserProfileSerializer , TokenSerializer , LibrarySerializer , EventSerializer , EventUserSerializer , ResourceSerializer , ResourceUserSerializer , MarketSerializer , CommunitySerializer , CommunityMemberSerializer , TopicSerializer , CommunityTopicSerializer , TopicUserSerializer , LikesSerializer
from .models import UserProfile, Library, Event, EventUser, Resource, ResourceUser, Market, Community, CommunityMember, CommunityTopic, Topic, TopicUser, TopicActivity, Project, ProjectUser, ProjectChat , Likes


@api_view(['POST' , 'GET'])
def login_view(request):
    # Get the username and password from the request data
    try:
        username = request.data.get('username')
        password = request.data.get('password')


        # Authenticate the user using the UserProfile model
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            

            # Get the user profile and serialize it
            token, created = Token.objects.get_or_create(user=user)
            _token = TokenSerializer(token)
            user_profile = UserProfile.objects.get(user=user)
            serializer = UserProfileSerializer(user_profile)

            # Return the serialized user profile
            return Response({ 'user_token' : _token.data , 'user_data':serializer.data } , status=status.HTTP_200_OK)

        # If the authentication failed, return an error response
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(e.args[0])
        return Response({'error': e.args[0]}, status=status.HTTP_400_UNAUTHORIZED)

@api_view(['POST' , 'GET'])
def signup_view(request):
    # Get the username, password, and additional fields from the request data
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', None)  # Default to None if not provided
        experience = request.data.get('experience', None)
        interests = request.data.get('interests', None)
        location = request.data.get('location', None)

        # Create a new user object with the given username and password
        user = User.objects.create_user(username, email, password)

        # Create a new user profile object with the new user and the additional fields
        user_profile = UserProfile.objects.create(
            user=user,
            email=email,
            experience=experience,
            interests=interests,
            location=location
        )

        # Create or get a token for the new user
        token, created = Token.objects.get_or_create(user=user)
        
        # Serialize the token and user profile objects
        token_serializer = TokenSerializer(token)
        print(token_serializer.data)
        user_profile_serializer = UserProfileSerializer(user_profile)
        
        # Return the serialized user profile and token in the response
        return Response({'user_data': user_profile_serializer.data, 'user_token': token_serializer.data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e.args[0])
        return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET' , 'POST'])
@authentication_classes([SessionAuthentication , TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
            
        logout(request)
        token = Token.objects.get(user=request.user)
        token.delete()
        
        return Response({'message' : 'logout'})
    except Exception as e:
        print(e.args[0])
        return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET' , 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def UserProfileView(request):
    try:
        join_community = False
        user_profile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(user_profile)

        user_resources = ResourceUser.objects.filter(user=user_profile).prefetch_related('resource')
        resources_data = []
        for ur in user_resources:
            resrouce_data = ResourceSerializer(ur.resource).data
            resrouce_data['date'] = ur.on_sale
            resources_data.append(resrouce_data)
       
        return Response({'user_data': serializer.data, 'user_resources': resources_data })
    except Exception as e:
        print(e.args[0])
        return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET' , 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def GetProjets(request):
    try:
        
        projects = ProjectUser.objects.filter(user=user_profile).prefetch_related('project')
        projects_data = ProjectSerializer(projects, many=True)
        return Response({'projects': projects_data.data})
    
    except Exception as e:
        print(e.args[0])
        return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET' , 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def RegisterEvent(request):
    try:
        if request.method == 'POST':
            user_profile = get_object_or_404(UserProfile, user=request.user)
            type = request.data.get('type')
            event_id = request.data.get('event_id')
            event_date = request.data.get('event_date')
            event = get_object_or_404(Event, id=event_id)
            event_user = EventUser.objects.create(user=user_profile, event=event , type=type , date=event_date)
            return Response({'message':'Event registered successfully' , 'status':status.HTTP_200_OK})
        return Response({'message':'Invalid request method' , 'status':status.HTTP_400_BAD_REQUEST})
    except Exception as e:
        print(e.args[0])
        return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST' , 'GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Buy(request):
    try:

        if request.method == 'POST':
           
            resource_id = request.data.get('resource_id')
            buying_user = get_object_or_404(UserProfile, user=request.user)
            print(resource_id)
            resource = Resource.objects.get(id=resource_id)
            userResource = ResourceUser.objects.create(user=buying_user , resource=resource , on_sale=False)
            print(userResource)
            selling_resources = ResourceUser.objects.filter(resource_id=resource_id)

            selling_resources.delete()
            userResource.save()
            marketplace = Market.objects.get(user=selling_user, resource_id=resource_id)
            marketplace.delete()
            return Response({'message' : 'Resource bought successfully' , 'status':status.HTTP_200_OK})
    except Exception as e:
        print(e.args[0])
        return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST' , 'GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Sell(request):
    if request.method == 'POST':
        user_profile = get_object_or_404(UserProfile, user=request.user)
        resource_id = request.data.get('resource_id')
        selling_price = request.data.get('selling_price')
        market = Market.objects.create(user=user_profile, resource_id=resource_id, selling_price=selling_price)
        market.save()
        user_resource = ResourceUser.objects.get(user=user_profile, resource_id=resource_id)
        user_resource.on_sale = True
        return Response({'message' : 'Resource added to market' , 'status':status.HTTP_200_OK})

    return Response({'message' : 'Invalid request method' , 'status':status.HTTP_400_BAD_REQUEST})




@api_view(['GET' , 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def libraryItems(request):
    library_items = Library.objects.all()
    serializer = LibrarySerializer(library_items, many=True)
    return Response({'library': serializer.data}) 


@api_view(['GET' , 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def JoinCommunity(request):
    if request.method == 'POST':
        user_profile = get_object_or_404(UserProfile, user=request.user)
        community_id = request.data.get('community_id')
        if request.data.get('farming'):
            User.objects.filter(id=user_profile.user.id).update(joined_in_farming=True)
        if request.data.get('gardening'):
            User.objects.filter(id=user_profile.user.id).update(joined_in_gardening=True)
        community = get_object_or_404(Community, id=community_id)
        community_member = CommunityMember.objects.create(user=user_profile, community=community)
        community_member.save()
        return Response({'message':'Community joined successfully' , 'status':status.HTTP_200_OK})
    return Response({'message':'Invalid request method' , 'status':status.HTTP_400_BAD_REQUEST})

@api_view(['GET' , 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def CreateTopic(request):
    if request.method == 'POST':
        user_profile = get_object_or_404(UserProfile, user=request.user)
        community_id = request.data.get('community_id')
        description = request.data.get('description')
        title = request.data.get('title')
        community = get_object_or_404(Community, id=community_id)

        topic = Topic.objects.create(title=title, description=description)
        CommunityTopic.objects.create(community=community, topic=topic )
        CommunityTopic.save()
        TopicUser.objects.create(user=user_profile, topic=topic , started_by=True)
        TopicUser.save()


        return Response({'message':'Topic created successfully' , 'status':status.HTTP_200_OK})
    return Response({'message':'Invalid request method' , 'status':status.HTTP_400_BAD_REQUEST})



@api_view(['GET' , 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def JoinTopic(request):
    if request.method == 'POST':
        user_profile = get_object_or_404(UserProfile, user=request.user)
        topic_id = request.data.get('topic_id')
        topic = get_object_or_404(Topic, id=topic_id)
        TopicUser.objects.create(user=user_profile, topic=topic , started_by=False)
        TopicUser.save()
        return Response({'message':'Topic joined successfully' , 'status':status.HTTP_200_OK})
    return Response({'message':'Invalid request method' , 'status':status.HTTP_400_BAD_REQUEST})


@api_view(['GET' , 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def PerformActivity(request):
    if request.method == 'POST':
        user_profile = get_object_or_404(UserProfile, user=request.user)
        topic_id = request.data.get('topic_id')
        comment = request.data.get('comment')
        topic = get_object_or_404(Topic, id=topic_id)
        TopicActivity.objects.create(user=user_profile, topic=topic , comment=comment )
        return Response({'message':'Activity performed successfully' , 'status':status.HTTP_200_OK})
    return Response({'message':'Invalid request method' , 'status':status.HTTP_400_BAD_REQUEST})


@api_view(['GET' , 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Like(request):
    if request.method == 'POST':
        topic_activity_id = request.data.get('topic_activity_id')
        topic_activity = get_object_or_404(TopicActivity, id=topic_activity_id)
        like = Likes.objects.create(topic_activity=topic_activity)
        return Response({'message':'Liked successfully' , 'status':status.HTTP_200_OK})
    return Response({'message':'Invalid request method' , 'status':status.HTTP_400_BAD_REQUEST})


@api_view(['GET' , 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ShowProject(request):
    project = Project.objects.all()
    serializer = ProjectSerializer(project, many=True)
    return Response({'project': serializer.data})

@api_view(['GET' , 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def AddProject(request):
    if request.method == 'POST':
        user_profile = get_object_or_404(UserProfile, user=request.user)
        title = request.data.get('title')
        description = request.data.get('description')
        category = request.data.get('category')
        is_completed = request.data.get('is_completed')
        project = Project.objects.create(title=title, description=description, category=category  , completed=is_completed)
        ProjectUser.objects.create(user=user_profile, project=project)
        return Response({'message':'Project added successfully' , 'status':status.HTTP_200_OK})
    return Response({'message':'Invalid request method' , 'status':status.HTTP_400_BAD_REQUEST})

@api_view(['GET' , 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ShowTopics(request):
    category = request.data.get('category')
    if category:
      
        communities_in_category = Community.objects.filter(category=category)
        
       
        community_topics = CommunityTopic.objects.filter(community__in=communities_in_category).select_related('topic')
        

        topics = [ct.topic for ct in community_topics]
        

        serializer = TopicSerializer(topics, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Category is required as a query parameter."}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET' , 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def TopicMessages(request):
    user = get_object_or_404(UserProfile, user=request.user)
    topic_id = request.query_params.get('topic_id')  # Use query_params for GET requests
    
    if not topic_id:
        return Response({"error": "Topic ID is required as a query parameter."}, status=400)
    
    # Filter TopicActivity instances by the provided topic ID
    topic_activities = TopicActivity.objects.filter(topic_id=topic_id)
    

    response_data = []
    for activity in topic_activities:

        likes_count = Likes.objects.filter(topic_activity=activity).count()
        
        # Serialize the topic activity data (Assuming you have a serializer, if not, create a dictionary manually)
        activity_data = TopicActivitySerializer(activity).data  # Adjust this line if you're manually creating the data dictionary
        activity_data['likes_count'] = likes_count  # Add the likes count to the activity data
        
        response_data.append(activity_data)
    
    return Response({'activity':response_data})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def UpcomingEvents(request):
    if request.method == 'GET':
        upcoming_events = Event.objects.filter(date__gt=timezone.now()).order_by('date')

        serializer = EventSerializer(upcoming_events, many=True)
    
        return Response(serializer.data)



@api_view(['GET' , 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def GetEventDetails(request):
    # Assuming you are identifying the user via token authentication
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.data.get('detail'):
            event_id = request.data.get('event_id')
            event = get_object_or_404(Event, id=event_id)
            serializer = EventSerializer(event)
    
    # Fetch events based on the relationship in EventUser
    participating_events_user = EventUser.objects.filter(user=user_profile, type='participating')
    attending_events_user = EventUser.objects.filter(user=user_profile, type='attending')


    all_events = Event.objects.all()

    event_to_return = []
    participating_events = [eu.event for eu in participating_events_user]
    attending_events = [eu.event for eu in attending_events_user]
    for event in all_events:
        if event not in participating_events or event not in attending_events:
            event_to_return.append(event)

    participiting_serializer = EventSerializer(participating_events, many=True)
    attending_serializer = EventSerializer(attending_events, many=True)
    other_events_serializer = EventSerializer(event_to_return, many=True)
    

    # Serialize the events
    participating_serializer = EventSerializer(participiting_serializer.data, many=True)
    attending_serializer = EventSerializer(attending_serializer.data, many=True)
    other_events_serializer = EventSerializer(other_events_serializer.data, many=True)
    
    # Return the serialized data
    return Response({
        'participating_events': participating_serializer.data,
        'attending_events': attending_serializer.data,
        'other_events': other_events_serializer.data
    })



@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def MarketPlace(request):
    if request.method == 'GET':
        # Fetch the current user's profile
        user = get_object_or_404(UserProfile, user=request.user)

        # Fetch the market listings for the current user
        market_listings = Market.objects.all()

        # Serialize the market listings
        market_serializer = MarketSerializer(market_listings, many=True)

        # Get unique resource IDs from the market listings
        resource_ids = market_listings.values_list('resource', flat=True).distinct()

        # Fetch the resources based on the unique IDs
        resources = Resource.objects.filter(id__in=resource_ids)

        # Serialize the resources
        resource_serializer = ResourceSerializer(resources, many=True)

        # Serialize the user's profile
        user_serializer = UserProfileSerializer(user)

        # Prepare the response data
        data = {
            "user": user_serializer.data,
            "market_listings": market_serializer.data,
            "resources": resource_serializer.data,
        }

        # Return the response
        return Response({'message' : data})


@api_view(['GET' , 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def JoinEvent(request):
    try:
        if request.method == 'POST':
            user_profile = get_object_or_404(UserProfile, user=request.user)
            event_id = request.data.get('event_id')
            type = request.data.get('type')
            event = get_object_or_404(Event, id=event_id)
            EventUser.objects.create(user=user_profile, event=event , type=type)
            return Response({'message':'Event joined successfully' , 'status':status.HTTP_200_OK})
        return Response({'message':'Invalid request method' , 'status':status.HTTP_400_BAD_REQUEST})
    except Exception as e:
        print(e.args[0])
        return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    





    

    



