def get_client_ip(request):
    ip = ''
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', None)
        if x_forwarded_for is not None:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
    except BaseException as e:
        print(f'Failed to parse Client IP: {e}')
    finally:
        return ip