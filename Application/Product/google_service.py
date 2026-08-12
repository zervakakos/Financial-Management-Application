import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    
    cred = None
    pickle_file = f'token_{API_NAME}_{API_VERSION}.pickle'

    # 1. Load existing token if present
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    # 2. Check if token is missing or invalid
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            try:
                # Attempt to refresh the token automatically
                cred.refresh(Request())
            except Exception:
                # If refreshing fails (invalid_grant), remove the pickle file and force re-login
                os.remove(pickle_file)
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                cred = flow.run_local_server(port=0)
        else:
            # First-time login or no refresh token available
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server(port=0)

        # 3. Save the new/refreshed credentials
        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_NAME, API_VERSION, credentials=cred)
        return service
    except Exception as e:
        print(f'Failed to create service: {e}')
        return None