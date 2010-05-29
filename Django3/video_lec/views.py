from django.shortcuts import render_to_response, get_object_or_404
from Django3.video_lec.models import course, course_video, random_video

def index(request):
	course_list = course.objects.all().order_by('-date_last_modified')[:10]
	return render_to_response('video_lec/index.html', {'course_list': course_list})

def course_view(request, course_id):
	c = get_object_or_404(course, id=course_id)
	return render_to_response('video_lec/course_details.html', {'course': c})

def course_video_view(request, video_id):
	v = get_object_or_404(course_video, id=video_id)
	return render_to_response('video_lec/video.html', {'video': v})

def random_video_view(request, video_id):
	v = get_object_or_404(random_video, id=video_id)
	return render_to_response('video_lec/video.html', {'video': v})
