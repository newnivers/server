import requests

from config import settings


def get_naver_access_token(code: str, state: str):
    response = requests.get(
        f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={settings.NAVER_CLIENT_ID}"
        f"&client_secret={settings.NAVER_CLIENT_SECRET}&code={code}&state={state}"
    ).json()
    access_token = response.get("access_token", None)
    return access_token


def get_naver_user_info(access_token: str):
    response = requests.post(
        "https://openapi.naver.com/v1/nid/me",
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()
    message = response.get("message", "failed")
    return response["response"] if message == "success" else None
