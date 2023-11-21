def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_device_type(parsed_user_agent):
    if 'tablet' in parsed_user_agent.get('device', '').lower():
        return 'Tablet'
    elif 'mobile' in parsed_user_agent.get('device', '').lower():
        return 'Mobile'
    else:
        return 'Desktop'