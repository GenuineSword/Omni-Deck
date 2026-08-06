"""Configuration for the Media File Explorer"""

# File extensions by category
MEDIA_TYPES = {
    'photos': {
        'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico', '.tiff'],
        'display_name': 'Photos',
        'icon': '🖼️'
    },
    'videos': {
        'extensions': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpeg', '.3gp'],
        'display_name': 'Videos',
        'icon': '🎬'
    },
    'documents': {
        'extensions': ['.pdf', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt', '.txt', '.csv'],
        'display_name': 'Documents',
        'icon': '📄'
    },
    'audio': {
        'extensions': ['.mp3', '.wav', '.flac', '.aac', '.wma', '.ogg', '.m4a'],
        'display_name': 'Audio',
        'icon': '🎵'
    },
    'games': {
        'extensions': [],
        'display_name': 'Games',
        'icon': '🎮'
    },
    'apps': {
        'extensions': ['.exe', '.msi', '.apk', '.jar', '.bat', '.cmd', '.lnk', '.app', '.dmg', '.pkg', '.appimage'],
        'display_name': 'Apps',
        'icon': '🧩'
    }
}

# Thumbnail sizes
THUMB_SIZE = 120  # pixels

# Preview image sizes
PREVIEW_SIZE = (400, 300)

# Maximum files to show without pagination
MAX_FILES_PER_PAGE = 100

# Default organization root directory
DEFAULT_ORG_ROOT = r'C:\Users\{username}\MediaExplorer'

# Batch operation settings
MAX_BATCH_SIZE = 500
