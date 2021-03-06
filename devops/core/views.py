from django.shortcuts import render_to_response, redirect
from django.contrib.auth import logout
from tiles.views import gen_context
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
import core.sync
from django.conf import settings

# Create your views here.
def sync(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed()
    elif request.user.is_authenticated:
        core.sync.sync(request.user)
        messages.success(request, 'Repositories refreshed')
    else:
        messages.error(request, 'You must login')
    return HttpResponseRedirect('/')


def home(request):
    context = RequestContext(request)

    if request.user.is_authenticated():
        context['tiles'] = []
        context = gen_context(request, settings.HOME_TILES, context, context['tiles'])

    return render_to_response('core/home.html', context)

def logout_view(request):
    logout(request)
    return redirect('/')
