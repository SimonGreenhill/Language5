from tastypie.resources import ModelResource
from tastypie.cache import SimpleCache
from website.apps.core.models import Language, Source

class LanguageResource(ModelResource):
    
    def determine_format(self, request):
        return 'application/json'
    
    class Meta:
        queryset = Language.objects.all()
        allowed_methods = ['get']
        excludes = ['comment', 'bibtex', ]
        #cache = SimpleCache(timeout=10)
        detail_uri_name = 'slug'


class SourceResource(ModelResource):
    
    def determine_format(self, request):
        return 'application/json'
    
    class Meta:
        queryset = Source.objects.all()
        allowed_methods = ['get']
        excludes = ['information', ]
        cache = SimpleCache(timeout=10)
        detail_uri_name = 'slug'
        

