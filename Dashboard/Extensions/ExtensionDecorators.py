def InModal(view):
    def wrapper(request, *args, **kwargs):
        r = view(request, *args, **kwargs)
        r.context_data = {'Modal': True}
        return r.render()
    return wrapper