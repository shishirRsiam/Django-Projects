from .JobPost_App_Import import *
from .serializers import JobPostSerializer
from . models import JobPost, Applied
from rest_framework.views import APIView
from .response import *

class JobPostApiViewSet(APIView):
    def post(self, request):
        serializer = JobPostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def get(self, request, *args, **kwargs):
        job_post_id = kwargs.get('id')
        if job_post_id:
            try:
                job_post = JobPost.objects.get(id=job_post_id)
                serializer = JobPostSerializer(job_post)
                response = {
                    'total_applicants': job_post.applied.all().count(),
                    'job_post': serializer.data,
                }
                return Response(response)
            
            except JobPost.DoesNotExist:
                return Response({"error": "Job post not found."}, status=404)
        
        job_posts = JobPost.objects.all().order_by('-id')
        serializer = JobPostSerializer(job_posts, many=True)
        return Response({
            "authenticated": request.user.is_authenticated,
            "job_posts": serializer.data
        })
    
class JobApplyApiView(APIView):
    def post(self, request, *args, **kwargs):
        job_post_id = kwargs.get('id')

        print(')_'*30)
        print('->', request.user)
        print('->', job_post_id)
        print('-> is_apply:', request.data['is_apply'])
        if job_post_id:
            try:
                job_post = JobPost.objects.get(id=job_post_id)
            except JobPost.DoesNotExist:
                return Response({"error": "Job post not found."}, status=404)
            
        if request.data['is_apply']:
            print('-> data', request.data)
            Applied.objects.create(user=request.user, job=job_post)
            response = get_job_job_applied_response(request, job_post)
        else: response = get_job_details_button_name(request, job_post)
        return Response(response)
