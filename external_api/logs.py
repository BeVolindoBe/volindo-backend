from external_api.models import Log


def save_log(provider, url, payload, status_code, response):
    try:
        Log.objects.create(
            provider_id=provider,
            url=url,
            payload=payload,
            status_code=status_code,
            response=response
        )
    except Exception as e:
        print(f'Unable to save the log data: {e}')
