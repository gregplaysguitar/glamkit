from models import ObjectWithImage
from django.shortcuts import render_to_response
from django.template import RequestContext

def crop_images(request):
    owis = ObjectWithImage.objects.all()
    return render_to_response('testapp/tester.html', {'owis':owis}, context_instance=RequestContext(request))