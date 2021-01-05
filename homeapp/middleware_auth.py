from django.shortcuts import render,get_object_or_404, redirect,HttpResponseRedirect, HttpResponse


def simple_middleware(get_response):

    def middleware(request):
        yes= request.session.get('user_id')
        if not yes:
            print('okay okay')

            return redirect('homeapp:login')
            
        response = get_response(request)
        return response

    return middleware

def admin_middleware(get_response):

    def middleware(request):
        yes= request.session.get('admin_id')
        if not yes:
            print('okay okay')

            return redirect('adminlogin')
            
        response = get_response(request)
        return response

    return middleware