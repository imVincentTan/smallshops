from taggit.models import Tag

def tags_processor(request):
    return {
        'tags' : Tag.objects.all()
    }