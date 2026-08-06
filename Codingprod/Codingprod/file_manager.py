"""File management utilities for organizing photos, videos, and other media"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
from config import MEDIA_TYPES


class FileOrganizer:
    """Handles file organization and categorization"""
    
    def __init__(self, source_dir: str, org_root: str = None):
        """
        Initialize the file organizer
        
        Args:
            source_dir: Directory to scan for files
            org_root: Root directory for organized files
        """
        self.source_dir = Path(source_dir)
        self.org_root = Path(org_root) if org_root else Path.home() / 'MediaExplorer'
        self.files_by_category = {}
        self._build_extension_map()
    
    def _build_extension_map(self):
        """Build a quick lookup map of extensions to categories"""
        self.extension_map = {}
        for category, info in MEDIA_TYPES.items():
            for ext in info['extensions']:
                self.extension_map[ext.lower()] = category
    
    def categorize_file(self, file_path: Path) -> str:
        """
        Determine the category of a file
        
        Args:
            file_path: Path to the file
            
        Returns:
            Category name or 'other'
        """
        ext = file_path.suffix.lower()
        name = file_path.name.lower()
        path_text = ' '.join(part.lower() for part in file_path.parts)

        game_keywords = ['game', 'games', 'steam', 'epic', 'gog', 'launcher', 'play', 'rpg', 'sim', 'fps', 'adventure']
        app_extensions = {'.exe', '.msi', '.apk', '.jar', '.bat', '.cmd', '.lnk', '.app', '.dmg', '.pkg', '.appimage'}

        if ext in app_extensions:
            if any(keyword in name or keyword in path_text for keyword in game_keywords):
                return 'games'
            return 'apps'

        return self.extension_map.get(ext, 'other')
    
    def scan_directory(self, recursive: bool = True) -> Dict[str, List[Path]]:
        """
        Scan directory for media files
        
        Args:
            recursive: Whether to scan subdirectories
            
        Returns:
            Dictionary with categories as keys and lists of file paths as values
        """
        self.files_by_category = {cat: [] for cat in MEDIA_TYPES.keys()}
        self.files_by_category['other'] = []
        
        if not self.source_dir.exists():
            return self.files_by_category
        
        pattern = '**/*' if recursive else '*'
        
        for file_path in self.source_dir.glob(pattern):
            if file_path.is_file():
                category = self.categorize_file(file_path)
                self.files_by_category[category].append(file_path)
        
        # Sort files by modification time (newest first)
        for category in self.files_by_category:
            self.files_by_category[category].sort(
                key=lambda x: x.stat().st_mtime, 
                reverse=True
            )
        
        return self.files_by_category
    
    def organize_files(self, files: List[Path], copy_mode: bool = False) -> Tuple[int, List[str]]:
        """
        Organize files into category folders
        
        Args:
            files: List of file paths to organize
            copy_mode: If True, copy files; if False, move files
            
        Returns:
            Tuple of (success_count, list of error messages)
        """
        success_count = 0
        errors = []
        
        # Create organization root
        self.org_root.mkdir(parents=True, exist_ok=True)
        
        for file_path in files:
            try:
                if not file_path.exists():
                    errors.append(f"File not found: {file_path}")
                    continue
                
                category = self.categorize_file(file_path)
                category_dir = self.org_root / category
                category_dir.mkdir(parents=True, exist_ok=True)
                
                dest_path = category_dir / file_path.name
                
                # Handle duplicate filenames
                counter = 1
                while dest_path.exists():
                    stem = file_path.stem
                    suffix = file_path.suffix
                    dest_path = category_dir / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                if copy_mode:
                    shutil.copy2(file_path, dest_path)
                else:
                    shutil.move(str(file_path), str(dest_path))
                
                success_count += 1
                
            except Exception as e:
                errors.append(f"Error organizing {file_path}: {str(e)}")
        
        return success_count, errors
    
    def get_file_info(self, file_path: Path) -> Dict:
        """
        Get detailed information about a file
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file information
        """
        stat = file_path.stat()
        return {
            'name': file_path.name,
            'size': stat.st_size,
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'created': datetime.fromtimestamp(stat.st_ctime),
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'category': self.categorize_file(file_path),
            'path': str(file_path)
        }


class FileFilter:
    """Handles filtering and searching of files"""
    
    def __init__(self):
        self.search_term = ""
        self.selected_categories = set(MEDIA_TYPES.keys())
    
    def filter_files(self, files: List[Path], search_term: str = "", 
                    categories: List[str] = None) -> List[Path]:
        """
        Filter files based on search term and categories
        
        Args:
            files: List of file paths to filter
            search_term: Search term to match in filename
            categories: List of categories to include (None = all)
            
        Returns:
            Filtered list of file paths
        """
        filtered = files
        
        # Filter by search term
        if search_term:
            filtered = [f for f in filtered if search_term.lower() in f.name.lower()]
        
        # Filter by categories
        if categories:
            organizer = FileOrganizer(Path.cwd())
            filtered = [f for f in filtered if organizer.categorize_file(f) in categories]
        
        return filtered
