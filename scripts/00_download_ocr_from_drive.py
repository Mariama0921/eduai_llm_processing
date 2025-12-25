import os
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials

# ========================
# CONFIGURATION
# ========================
SERVICE_ACCOUNT_FILE = "service_account.json"
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
OCR_FOLDER_ID = "1nW4iQgKYgeb4Oi4p-YQvxHbq9SW-2ozo"
OUTPUT_DIR = "data/ocr_json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ========================
# AUTHENTIFICATION
# ========================
creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build("drive", "v3", credentials=creds)

# ========================
# LISTE DES FICHIERS
# ========================
query = f"'{OCR_FOLDER_ID}' in parents and trashed=false"

results = service.files().list(
    q=query,
    fields="files(id, name, mimeType)"
).execute()

files = results.get("files", [])

print(f"{len(files)} fichiers trouvés")

# ========================
# TÉLÉCHARGEMENT
# ========================
for file in files:
    if not file["name"].endswith(".json"):
        continue

    print(f"⬇️ Téléchargement : {file['name']}")

    request = service.files().get_media(fileId=file["id"])
    fh = io.FileIO(os.path.join(OUTPUT_DIR, file["name"]), "wb")
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()

print(" Téléchargement terminé")
