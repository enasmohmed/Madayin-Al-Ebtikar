"""Force site UI language to English (ignore browser Accept-Language)."""

from django.conf import settings
from django.utils import translation


class ForceArabicLanguageMiddleware:
    """
    Keep templates, LTR, and modeltranslation on the configured site language.
    The class name is historical; FORCE_SITE_LANGUAGE controls the actual locale.
    """

    language_code = getattr(settings, "FORCE_SITE_LANGUAGE", "en")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        translation.activate(self.language_code)
        request.LANGUAGE_CODE = self.language_code
        response = self.get_response(request)
        response.headers.setdefault("Content-Language", self.language_code)
        return response
