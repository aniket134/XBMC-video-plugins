import dsh_common_django_request



def set(req):
    dsh_common_django_request.set(req)



def get():
    return dsh_common_django_request.get()



def deny_it(request):
    return dsh_common_django_request.deny_it(request)



def no_permission_reply():
    return dsh_common_django_request.no_permission_reply()
