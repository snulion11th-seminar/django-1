from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import Tag
from .serializers import TagSerializer


# Create your views here.
class TagListView(APIView):
  # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

  def get(self, request):
    tags = Tag.objects.all()
    serializer = TagSerializer(instance=tags, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request):
    if not request.user.is_authenticated:
      return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)

    content = request.data.get('content')
    author = request.user
    if not content:
      return Response({"detail": "missing fields ['content']"}, status=status.HTTP_400_BAD_REQUEST)

    if Tag.objects.filter(content=content).exists():
      return Response({"detail" : "이미 존재하는 태그입니다."}, status=status.HTTP_409_CONFLICT)

    tag = Tag.objects.create(content=content, author=author)
    serializer = TagSerializer(tag)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

class TagDeleteView(APIView):
  def delete(self, request, tag_id):
    # TODO auth
    try:
      tag = Tag.objects.get(id=tag_id)
    except:
      return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user == tag.author:
      tag.delete()
    else:
      return Response({"detail": "작성자만 삭제가 가능합니다."}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(status=status.HTTP_204_NO_CONTENT)
