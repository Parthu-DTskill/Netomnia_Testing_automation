import requests

def fetch_dummy_data(base_url, kind=None, grouped=False, timeout=30):
    params = {}
    if kind:
        params["kind"] = kind
    if grouped:
        params["grouped"] = "true"

    response = requests.get(base_url, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()