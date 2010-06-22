# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from dv2.db.models import Item

#def search_form(request):
    #return render_to_response('search_form.html')

#def search(request):
    #if 'q' in request.GET:
        #message = 'You searched for: %r' % request.GET['q']
    #else:
        #message = 'You submitted an empty form.'
    #return HttpResponse(message)

#def search(request):
    #if 'q' in request.GET and request.GET['q']:
        #q = request.GET['q']
        #books = Book.objects.filter(title__icontains=q)
        #return render_to_response('search_results.html', {'books': books, 'query': q})
    #else:
        #return render_to_response('search_form.html', {'error': True})

#def search(request):
    ##error = False
    #errors = []
    #if 'q' in request.GET:
        #q = request.GET['q']
        #if not q:
            ##error = True
            #errors.append('Enter a search term.')
        #elif len(q) > 20:
            ##error = True
            #errors.append('Please enter at most 20 characters.')
        #else:
            #clips = Item.objects.filter(clip.name__icontains=q)
            #return render_to_response('search_results.html', {'clips': clips, 'query': q})
    #return render_to_response('search_form.html', {'errors': errors})
#Uncomment this block later
