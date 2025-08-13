import json
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

def index(request):
    return render(request, 'deals_app/index.html')

@csrf_exempt
def save_auth(request):
    """
    Принимаем объект BX24.getAuth() и кладём в сессию.
    ВАЖНО: фронт должен слать fetch(..., { credentials: 'include' }).
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'error': 'bad_json'}, status=400)

    # Минимум, что нам нужно для запроса в Б24:
    token  = data.get('access_token') or data.get('auth_id')
    domain = data.get('domain') or getattr(getattr(settings, 'APP_SETTINGS', None), 'portal_domain', None)
    if not token or not domain:
        return JsonResponse({'error': 'no_token_or_domain'}, status=400)

    request.session['bx_auth'] = {'access_token': token, 'domain': domain}
    request.session.set_expiry(3600)  # токен живёт ~час — синхронизируем
    request.session.modified = True
    return JsonResponse({'ok': True})

def user_current(request):
    """
    Возвращаем {FULL_NAME, NAME, LAST_NAME} текущего пользователя.
    """
    auth = request.session.get('bx_auth')
    if not auth:
        return JsonResponse({'error': 'no_auth'}, status=401)

    domain = auth['domain']
    token  = auth['access_token']

    # Запрос в Bitrix24
    try:
        r = requests.get(
            f"https://{domain}/rest/user.current.json",
            params={'auth': token},
            timeout=15
        )
        r.raise_for_status()
        j = r.json()
    except Exception as e:
        return JsonResponse({'error': f'bitrix_request_failed: {e}'}, status=502)

    if 'error' in j:
        # Токен мог протухнуть: фронт пусть перезайдёт/обновит страницу
        return JsonResponse({'error': j.get('error_description', 'bitrix_error')}, status=401)

    res = j.get('result', {}) or {}
    full = f"{res.get('NAME','')} {res.get('LAST_NAME','')}".strip()
    return JsonResponse({
        'ID': res.get('ID'),
        'NAME': res.get('NAME'),
        'LAST_NAME': res.get('LAST_NAME'),
        'FULL_NAME': full
    })
