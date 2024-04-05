from pathlib import Path

# Paths
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = BASE_DIR / 'media'
LOCALE_PATHS = ['movies/locale']
STATIC_URL = "static/"
