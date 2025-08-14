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

def user_deals(request):
    """10 последних активных (не закрытых) сделок пользователя портала."""
    auth = request.session.get('bx_auth')
    if not auth:
        return JsonResponse({'error': 'no_auth'}, status=401)

    domain = auth['domain']
    token  = auth['access_token']

    params = {
        'filter[CLOSED]': 'N',                 # только активные
        'order[ID]': 'DESC',                   # последние
        'select[]': ['ID','TITLE','STAGE_ID','DATE_CREATE','OPPORTUNITY','ASSIGNED_BY_ID'],
        'start': 0,
        'auth': token,
    }
    r = requests.post(f"https://{domain}/rest/crm.deal.list.json", data=params, timeout=15)
    try:
        r.raise_for_status()
        items = r.json().get('result', [])
    except Exception as e:
        return JsonResponse({'error': f'bitrix_request_failed: {e}'}, status=502)

    return JsonResponse(items[:10], safe=False)


@csrf_exempt
def deal_create(request):
    """Создание сделки с кастомным полем UF_CRM_1755174858."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    auth = request.session.get('bx_auth')
    if not auth:
        return JsonResponse({'error': 'no_auth'}, status=401)

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'error': 'bad_json'}, status=400)

    title = (payload.get('title') or '').strip()
    if not title:
        return JsonResponse({'error': 'title_required'}, status=400)

    # сумма как число
    opp_raw = payload.get('sum')
    try:
        opportunity = float(opp_raw) if opp_raw not in (None, "") else None
    except Exception:
        opportunity = None

    custom_value = payload.get('UF_CRM_1755174858')

    # минимальный набор полей
    fields = {'TITLE': title}
    if opportunity is not None:
        fields['OPPORTUNITY'] = opportunity
    if custom_value is not None:
        fields['UF_CRM_1755174858'] = custom_value

    domain = auth['domain']
    token = auth['access_token']

    # ВАЖНО: шлём как fields[KEY]=VALUE, это надёжнее
    data = {'auth': token}
    for k, v in fields.items():
        data[f'fields[{k}]'] = v

    try:
        r = requests.post(f"https://{domain}/rest/crm.deal.add.json", data=data, timeout=15)
        # НЕ делаем raise_for_status, чтобы прочитать тело ошибки от Б24
        j = r.json()
    except Exception as e:
        return JsonResponse({'ok': False, 'error': f'bitrix_request_failed: {e}', 'raw': r.text if 'r' in locals() else ''}, status=502)

    # Если Б24 вернул ошибку — отдаём её наверх, чтобы ты видел точную причину
    if isinstance(j, dict) and 'error' in j:
        return JsonResponse({'ok': False, 'error': j.get('error'), 'error_description': j.get('error_description'), 'raw': j}, status=400)

    return JsonResponse({'ok': True, 'result': j.get('result')})


