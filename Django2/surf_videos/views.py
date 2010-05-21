from django.http import HttpResponse
from django.template import Context,loader
from Django2.surf_videos.models import *

def index(request):
	latest_video_list = video.objects.all().order_by('-upload_date')[:5]
	t = loader.get_template('surf_videos/index.html')
	c = Context({
		'latest_video_list':latest_video_list,
	})
	return HttpResponse(t.render(c))
def detail(request,vid_id):
	return HttpResponse("You're looking at video %s."%vid_id)
def results(request,vid_id):
	return HttpResponse("You're looking at results of video %s."%vid_id)
def rating(request,vid_id):
	return HttpResponse("You're looking at rating of video %s."%vid_id)
