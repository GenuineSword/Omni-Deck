# Media File Explorer

A personal, organized file explorer application for Windows that automatically categorizes and manages your photos, videos, documents, and audio files with drag-and-drop support.

## Features

✨ **Smart Organization**
- Automatically categorizes files: Photos, Videos, Documents, Audio
- Move or copy files to organized directories
- Both virtual organization and physical file organization options

🎯 **Search & Filter**
- Real-time search across filenames
- Filter by media type
- Quick statistics on file collections

🖱️ **Drag & Drop**
- Drag and drop files directly onto the application
- Select multiple files for batch operations
- Visual feedback with thumbnails

📊 **File Management**
- Batch copy or move operations
- Handles duplicate filenames automatically
- Detailed file information and statistics
- Support for 30+ file formats

## Installation

### Requirements
- Python 3.8+
- Windows 10 or later

### Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the application:**
```bash
python main.py
```

## Usage

### Getting Started

1. Click **"Browse Directory"** and select the folder you want to organize
2. The app will scan and display all media files with thumbnails
3. Files are automatically categorized by type

### Organizing Files

**Two organization modes:**

- **Move Files:** Click "Organize Files" - files are moved to their category folders
- **Copy Files:** Click "Copy & Organize" - creates copies in organized folders while keeping originals

### Searching & Filtering

- Use the **search box** to find files by name
- Use the **Filter by** dropdown to show only specific file types
- Results update in real-time

### Batch Operations

1. Select files by checking their checkboxes
2. Click "Organize Files" or "Copy & Organize"
3. View results and error summary

### Drag & Drop

Simply drag files from your file explorer onto the application grid to select them for organization.

## File Categories

| Category | Extensions |
|----------|------------|
| **Photos** | jpg, jpeg, png, gif, bmp, webp, svg, ico, tiff |
| **Videos** | mp4, avi, mkv, mov, wmv, flv, webm, m4v, mpeg, 3gp |
| **Documents** | pdf, docx, doc, xlsx, xls, pptx, ppt, txt, csv |
| **Audio** | mp3, wav, flac, aac, wma, ogg, m4a |

## Default Organization Structure

By default, files are organized into:
```
C:\Users\{username}\MediaExplorer/
├── photos/
├── videos/
├── documents/
└── audio/
```

You can customize the organization root directory by modifying `config.py`.

## File Structure

```
.
├── main.py              # Application entry point
├── ui.py                # PyQt6 UI components
├── file_manager.py      # File organization and filtering logic
├── config.py            # Configuration and file type definitions
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Advanced Features

### Statistics Tab
View detailed statistics about your file collection:
- Number of files per category
- Total storage used per category
- Overall statistics

### Duplicate Handling
The application automatically renames duplicate files:
- `photo.jpg` → `photo_1.jpg` → `photo_2.jpg`, etc.

### Performance
- Handles large directories efficiently
- Grid shows first 100 files (pagination coming soon)
- Background scanning option available

## Configuration

Edit `config.py` to customize:
- File extensions for each category
- Thumbnail size
- Organization root directory
- Batch operation limits

## Keyboard Shortcuts

- `Ctrl+O` - Browse directory (coming soon)
- `Ctrl+F` - Focus search box (coming soon)

## Troubleshooting

**Issue: Files not appearing**
- Make sure you've selected a directory with "Browse Directory"
- Click "Refresh" to rescan

**Issue: Organization fails**
- Check that you have write permissions to the destination folder
- Ensure no files are locked by other applications

**Issue: Thumbnails not showing**
- The app supports jpg, png, gif, and webp
- Other formats display category icons instead

## Future Enhancements

- 🎬 Video preview generation
- 📅 Automatic date-based organization
- 🔄 Undo functionality
- ⭐ Favorites and tagging
- 🎨 Theme customization
- 📱 Mobile app companion
- 🌐 Cloud sync support

## License

This project is created for personal use.

## Support

For issues or feature requests, ensure you have the latest version of dependencies:
```bash
pip install --upgrade -r requirements.txt
```
