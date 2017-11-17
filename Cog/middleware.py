class LogUserDetailsMiddleware(object):

    def process_request(self, request):
        print('user: ' + str(request.user))
        print('ip-address: ' + str(request.META.get('REMOTE_ADDR')))
