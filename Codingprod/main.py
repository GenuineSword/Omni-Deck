"""
OmniDeck - A polished personal media explorer with drag-and-drop organization
Organize photos, videos, documents, and audio with a futuristic experience
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui import MediaExplorerUI


def main():
    """Launch the OmniDeck application"""
    app = QApplication(sys.argv)
    app.setApplicationName("OmniDeck")
    app.setApplicationDisplayName("OmniDeck")
    app.setWindowIcon(QIcon(str(Path(__file__).resolve().parent / "assets" / "omni_deck_icon.svg")))
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = MediaExplorerUI()
    window.setWindowTitle("OmniDeck")
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
