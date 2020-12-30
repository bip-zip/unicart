from django.shortcuts import render,get_object_or_404, redirect,HttpResponseRedirect, HttpResponse


def simple_middleware(get_response):

    def middleware(request):
        if not request.session.get('user_id'):
            return redirect('login')
            print('okay okay')

        response = get_response(request)
        return response

    return middleware