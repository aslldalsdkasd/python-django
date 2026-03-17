from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view
from .serializers import GroupSerializer

@extend_schema(summary='hell')
@api_view()
def hello_world_view(request: Request) -> Response:
    return Response({"message": "Hello World!"})

@extend_schema_view(
    get=extend_schema(summary='list groups'),
    post=extend_schema(summary='create groups'),
)
class GroupsListView(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
