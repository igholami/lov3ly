def get_domain(request):
    return request.get_host().split(":")[0]