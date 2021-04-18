from taggit.models import Tag

def tags_processor(request):
    return {
        'tags' : Tag.objects.all()
    }

def get_processor(request):
    return {
        'request_get' : request.GET
    }