from .JobPost_App_Import import *
from .serializers import JobPostSerializer
from . models import JobPost

class JobPostApiViewSet(viewsets.ModelViewSet):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    
    def post(self, request):
        serializer = JobPostSerializer(data=request.data)
        if serializer.is_valid():
            Post = serializer.save()
            print(':)'*30)
            print(Post)
            print(':)'*30)
            return Response(serializer.data)
        return Response(serializer.errors)
