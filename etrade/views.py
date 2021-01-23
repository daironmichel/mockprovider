from authlib.oauth1.errors import OAuth1Error
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .data import orders
from .server import require_oauth, server


@require_http_methods(["POST"])
@csrf_exempt
def initiate_temporary_credential(request):
    return server.create_temporary_credentials_response(request)


@csrf_exempt
def authorize(request):
    # make sure that user is logged in for yourself
    user = User.objects.get(id=1)
    login(request, user)

    if request.method == 'GET':
        try:
            req = server.check_authorization_request(request)
            context = {'query': req.query}
            return render(request, 'authorize.html', context)
        except OAuth1Error as error:
            context = {'error': error}
            return render(request, 'error.html', context)

    granted = request.POST.get('granted')
    if granted and granted == 'Authorize':
        grant_user = request.user
    else:
        grant_user = None

    try:
        return server.create_authorization_response(request, grant_user)
    except OAuth1Error as error:
        context = {'error': error}
        return render(request, 'error.html', context)


@require_http_methods(["POST"])
@csrf_exempt
def issue_token(request):
    return server.create_token_response(request)


@require_oauth()
@csrf_exempt
def user_api(request):
    user = request.oauth1_credential.user
    return JsonResponse(dict(username=user.username))


@require_oauth()
@csrf_exempt
def list_orders(request):
    user = request.oauth1_credential.user
    return JsonResponse(orders.ORDERS_RESPONSE)
