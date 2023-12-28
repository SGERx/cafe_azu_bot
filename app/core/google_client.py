from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from app.core.config import settings

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
INFO = {
    'type': settings.TYPE,
    'project_id': settings.PROJECT_ID,
    'private_key_id': settings.PRIVATE_KEY_ID,
    'private_key': settings.PRIVATE_KEY,
    'client_email': settings.CLIENT_EMAIL,
    'client_id': settings.CLIENT_ID,
    'auth_uri': settings.AUTH_URI,
    'token_uri': settings.TOKEN_URI,
    'auth_provider_x509_cert_url': settings.AUTH_PROVIDER_X509_CERT_URL,
    'client_x509_cert_url': settings.CLIENT_X509_CERT_URL
}

credentials = ServiceAccountCreds(scopes=SCOPES, **INFO)
service = Aiogoogle(service_account_creds=credentials)


async def get_service():
    async with service as aiogoogle:
        yield aiogoogle
