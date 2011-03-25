
def extra_settings_context(request):
    from django.conf import settings
    return {
        # 'sarpam_number_format':settings.SARPAM_NUMBER_FORMAT,
        #         'sarpam_currency_code':settings.SARPAM_CURRENCY_CODE
    }