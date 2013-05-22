from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from django import forms
from django.forms.formsets import formset_factory

from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Lexicon, Word
from website.apps.entry.dataentry.generic import process_post_and_save, GenericFormSet

@login_required()
def WordlistView(request, task):
    """Data entry task using a wordlist"""
    template_name = "entry/formtemplates/generic.html"
    
    # Load wordlist.
    assert task.wordlist
    words = task.wordlist.words.all()
    
    # Set up initial data.
    initial = []
    for w in words:
        initial.append({
            'language': task.language,
            'source': task.source,
            'word': w
        })
    
    # process form
    if request.POST:
        formset = GenericFormSet(request.POST, initial=initial)
        process_post_and_save(request, task, formset)
    else:
        formset = GenericFormSet(initial=initial)
    
    return render_to_response('entry/detail.html', {
        'task': task,
        'formset': formset,
        'template': template_name,
    }, context_instance=RequestContext(request))

