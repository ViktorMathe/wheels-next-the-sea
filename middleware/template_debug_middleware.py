import logging
from django.template.response import TemplateResponse

logger = logging.getLogger(__name__)

class TemplateDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only check template responses
        if isinstance(response, TemplateResponse):
            try:
                template_paths = [t.origin.name for t in response.templates if t.origin]
                logger.info(f"[TEMPLATE DEBUG] URL={request.path} -> {template_paths}")
                print(f"[TEMPLATE DEBUG] URL={request.path} -> {template_paths}")
            except Exception:
                pass
        return response