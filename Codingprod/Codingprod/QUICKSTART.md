# Quick Start Guide

## Installation & Running

### Step 1: Install Dependencies
Open PowerShell or Command Prompt in the project directory and run:

```powershell
pip install -r requirements.txt
```

This will install:
- **PyQt6** - Desktop GUI framework
- **Pillow** - Image processing for thumbnails
- **pathlib2** - Path utilities

### Step 2: Run the Application

```powershell
python main.py
```

The Media File Explorer window will open.

### Step 3: Start Organizing

1. Click **"Browse Directory"** button
2. Select a folder containing your media files
3. The app will scan and display all files with thumbnails
4. Select files using checkboxes
5. Click **"Organize Files"** to move them, or **"Copy & Organize"** to copy them to organized folders

## What the Application Does

### Core Features:

- 📁 **Smart Organization**: Automatically sorts files into Photo, Video, Document, and Audio folders
- 🖼️ **Thumbnails**: Shows preview images for photos
- 🔍 **Search**: Find files by typing in the search box
- 🏷️ **Filter**: Filter by file type
- 📊 **Statistics**: View file counts and storage usage
- 🖱️ **Drag & Drop**: Select files easily
- 📦 **Batch Operations**: Organize multiple files at once
- 📋 **Two Modes**: Move or copy files

### Organization Targets:

By default, organized files go to:
- `C:\Users\{username}\MediaExplorer\photos`
- `C:\Users\{username}\MediaExplorer\videos`
- `C:\Users\{username}\MediaExplorer\documents`
- `C:\Users\{username}\MediaExplorer\audio`

Edit `config.py` to change the root directory.

## Supported File Types

| Type | Formats |
|------|---------|
| Photos | JPG, PNG, GIF, BMP, WEBP, SVG, ICO, TIFF |
| Videos | MP4, AVI, MKV, MOV, WMV, FLV, WEBM, M4V, MPEG, 3GP |
| Documents | PDF, DOCX, DOC, XLSX, XLS, PPTX, PPT, TXT, CSV |
| Audio | MP3, WAV, FLAC, AAC, WMA, OGG, M4A |

## Tips

- Always use **"Copy & Organize"** if you want to keep the original files
- Use **"Organize Files"** to move files permanently
- Check the **Statistics** tab to see what you have
- Search works in real-time as you type
- Selected files persist until you deselect them

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No files appear | Make sure you selected a directory with the Browse button |
| Errors during organization | Check file permissions; ensure files aren't open in other apps |
| Thumbnails not showing | The app shows icons for non-image formats |
| Application crashes | Update dependencies: `pip install --upgrade -r requirements.txt` |

## Next Steps

- Add more file types in `config.py`
- Customize organization paths
- Modify thumbnail size for your preference
- Check `file_manager.py` for advanced filtering options

Enjoy organizing your files! 🎉
