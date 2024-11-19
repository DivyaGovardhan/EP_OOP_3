from django.contrib.auth.models import User
from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.decorators import api_view, action, renderer_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Snippet
from .permissions import IsOwnerOrReadOnly
from .serializers import SnippetSerializer, UserSerializer


# Create your views here.
class SnippetViewSet(viewsets.ModelViewSet):
   """
   This viewset automatically provides `list`, `create`, `retrieve`,
   `update` and `destroy` actions.

   Additionally we also provide an extra `highlight` action.
   """
   queryset = Snippet.objects.all()
   serializer_class = SnippetSerializer
   permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

   @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
   def highlight(self, request, *args, **kwargs):
      snippet = self.get_object()
      return Response(snippet.highlighted)

   def perform_create(self, serializer):
      serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
   queryset = User.objects.all()
   serializer_class = UserSerializer

@api_view(['GET'])
def api_root(request, format=None):
   return Response({'users': reverse('user-list', request=request, format=format),
                    'snippets': reverse('snippet-list', request=request, format=format)})

