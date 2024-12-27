from .JobPost_App_Import import *
from .serializers import JobPostSerializer
from . models import JobPost
from rest_framework.views import APIView

class JobPostApiViewSet(APIView):
    def post(self, request):
        serializer = JobPostSerializer(data=request.data)
        print('()'*30)
        print(request.data)
        print('serializer', serializer)
        print('request.user', request.user)
        print('()'*30)

        if serializer.is_valid():
            post = serializer.save(user=request.user)
            print('serializer.data', serializer.data)
            return Response(serializer.data)

        return Response(serializer.errors)
    
    def list(self, request, *args, **kwargs):
        job_posts = JobPost.objects.all()
        serializer = JobPostSerializer(job_posts, many=True)
        return Response({
            "authenticated": request.user.is_authenticated,
            "Si": request.user.is_authenticated,
            "job_posts": serializer.data
        })
