from django.conf import settings

def extra_settings_context(request):
    extra_context = {
        'number_format':setting.SARPAM_NUMBER_FORMAT,
        'currency_code':settings.SARPAM_CURRENCY_CODE
    }
    return extra_context