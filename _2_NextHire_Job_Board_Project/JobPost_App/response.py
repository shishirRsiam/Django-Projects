def get_job_details_button_name(request, job_post):
    can_apply = False
    button_name = 'Login to Apply'
    if request.user.is_authenticated:
        if job_post.applied.filter(user=request.user).exists():
            button_name = 'Already Applied'
        else:
            can_apply = True
            button_name = 'Apply Now'
    response = {
        'can_apply': can_apply,
        'button_name': button_name
    }
    return response

def get_job_job_applied_response(request, job_post):
    response = {
        'title': "Application Submitted!",
        'message': "Your application has been submitted successfully.",
    }
    return response