from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Event
from .serializers import EventSerializer

# List and Create Events
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def event_list_create(request):
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, Update, Delete Event
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def event_detail(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventSerializer(event, )
        return Response(serializer.data)

    elif request.method == 'PUT':
        if event.created_by != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if event.created_by != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        event.delete()
        return Response({'message': 'Event deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
