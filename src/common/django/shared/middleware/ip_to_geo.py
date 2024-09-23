import logging
from django.conf import settings

logger = logging.getLogger("default")

class IpToGeoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            ipinfo_handler =  settings.IPINFO_HANDLER
            if ipinfo_handler:
                forwarded_for = request.headers.get(settings.REQUEST_ORIGIN_HEADER)
                client_ip = forwarded_for.split(',')[0].strip() if forwarded_for else None

                ip_info = ipinfo_handler.getDetails(client_ip)

                country = ip_info.country if ip_info else "XX"
                request.META['Request-Country-Code'] = country
            return self.get_response(request)
        except Exception as e:
            logger.error("Error retrieving IP information: %s", str(e))
            raise("Error retrieving IP information")
