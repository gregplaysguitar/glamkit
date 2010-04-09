from django.contrib.auth.decorators import login_required

from ixc_common.decorators import render_to

from models import File, PressImage, IMAGE_SIZES

@login_required
@render_to("file_library/file_index.html")
def file_index(request):
    files = File.objects.filter(published=True).order_by("-publish_date")
    return {'title': 'Resources', 'files': files}