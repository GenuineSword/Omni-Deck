"""Theme system for the Media File Explorer with multiple color schemes and effects"""

from enum import Enum
from typing import Dict, Tuple


class ThemeMode(Enum):
    """Available theme modes"""
    MIDNIGHT_CHASM = "midnight_chasm"
    CHROMA = "chroma"
    GRADIENT = "gradient"
    AURA = "aura"
    GLOW = "glow"
    LIGHT = "light"


class Theme:
    """Base theme class with color definitions"""
    
    def __init__(self, name: str, primary: str, secondary: str, accent: str, 
                 background: str, text: str, border: str, hover: str = None):
        self.name = name
        self.primary = primary
        self.secondary = secondary
        self.accent = accent
        self.background = background
        self.text = text
        self.border = border
        self.hover = hover or accent
    
    def get_stylesheet(self, translucent: bool = False, glow_intensity: int = 0) -> str:
        """
        Generate stylesheet for this theme
        
        Args:
            translucent: Whether to use translucent backgrounds
            glow_intensity: Intensity of glow effect (0-100)
        
        Returns:
            CSS stylesheet string
        """
        raise NotImplementedError("Subclasses must implement get_stylesheet")


class MidnightChasmTheme(Theme):
    """Dark theme with deep blacks and electric accents"""
    
    def __init__(self):
        super().__init__(
            name="Midnight Chasm",
            primary="#0a0e27",
            secondary="#1a1f3a",
            accent="#00d9ff",
            background="#0a0e27",
            text="#e0e0e0",
            border="#1e2749",
            hover="#00b8d4"
        )
    
    def get_stylesheet(self, translucent: bool = False, glow_intensity: int = 0) -> str:
        opacity = "180" if translucent else "255"
        glow = f"0px 0px {glow_intensity*2}px rgba(0, 217, 255, {glow_intensity/100});" if glow_intensity else ""
        
        return f"""
            * {{
                color: {self.text};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            
            QMainWindow, QDialog {{
                background-color: rgba({self._hex_to_rgb(self.background)}, {opacity});
                border: 1px solid {self.border};
                {glow}
            }}
            
            QWidget {{
                background-color: rgba({self._hex_to_rgb(self.background)}, {opacity});
            }}
            
            QPushButton {{
                background-color: {self.primary};
                color: {self.text};
                border: 2px solid {self.accent};
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: bold;
                transition: all 0.3s ease;
            }}
            
            QPushButton:hover {{
                background-color: {self.secondary};
                border-color: {self.hover};
                box-shadow: 0px 0px {glow_intensity}px rgba(0, 217, 255, {glow_intensity/200});
            }}
            
            QPushButton:pressed {{
                background-color: {self.accent};
                color: {self.background};
            }}
            
            QLineEdit, QComboBox {{
                background-color: {self.secondary};
                color: {self.text};
                border: 2px solid {self.border};
                border-radius: 4px;
                padding: 4px 8px;
                selection-background-color: {self.accent};
            }}
            
            QLineEdit:focus, QComboBox:focus {{
                border: 2px solid {self.accent};
                box-shadow: 0px 0px {glow_intensity}px rgba(0, 217, 255, {glow_intensity/200});
            }}
            
            QScrollArea {{
                background-color: rgba({self._hex_to_rgb(self.secondary)}, {opacity});
                border: 1px solid {self.border};
            }}
            
            QTabWidget::pane {{
                border: 1px solid {self.border};
                background-color: {self.background};
            }}
            
            QTabBar::tab {{
                background-color: {self.secondary};
                color: {self.text};
                padding: 6px 12px;
                border: 1px solid {self.border};
                border-bottom: none;
            }}
            
            QTabBar::tab:selected {{
                background-color: {self.primary};
                border: 2px solid {self.accent};
                border-bottom: none;
            }}
            
            QFrame {{
                background-color: rgba({self._hex_to_rgb(self.secondary)}, {int(opacity)*0.8});
                border: 1px solid {self.border};
                border-radius: 4px;
            }}
            
            QLabel {{
                color: {self.text};
            }}
            
            QStatusBar {{
                background-color: {self.primary};
                color: {self.accent};
                border-top: 1px solid {self.border};
            }}
            
            QCheckBox {{
                color: {self.text};
                spacing: 5px;
            }}
            
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                background-color: {self.secondary};
                border: 2px solid {self.border};
                border-radius: 3px;
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {self.accent};
                border: 2px solid {self.accent};
            }}
            
            QComboBox::drop-down {{
                border: none;
                background-color: {self.accent};
                width: 20px;
            }}
            
            QComboBox::down-arrow {{
                image: none;
                color: {self.background};
            }}
        """
    
    @staticmethod
    def _hex_to_rgb(hex_color: str) -> str:
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"{r},{g},{b}"


class ChromaTheme(Theme):
    """Vibrant multi-color theme with bold accents"""
    
    def __init__(self):
        super().__init__(
            name="Chroma",
            primary="#1a1a2e",
            secondary="#16213e",
            accent="#e94560",
            background="#0f3460",
            text="#ffffff",
            border="#e94560",
            hover="#ff6b9d"
        )
    
    def get_stylesheet(self, translucent: bool = False, glow_intensity: int = 0) -> str:
        opacity = "180" if translucent else "255"
        glow = f"0px 0px {glow_intensity*2}px rgba(233, 69, 96, {glow_intensity/100});" if glow_intensity else ""
        
        return f"""
            * {{
                color: {self.text};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            
            QMainWindow, QDialog {{
                background-color: rgba({self._hex_to_rgb(self.background)}, {opacity});
                border: 2px solid {self.accent};
                {glow}
            }}
            
            QWidget {{
                background-color: rgba({self._hex_to_rgb(self.background)}, {opacity});
            }}
            
            QPushButton {{
                background-color: {self.accent};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 14px;
                font-weight: bold;
                font-size: 11px;
            }}
            
            QPushButton:hover {{
                background-color: {self.hover};
                box-shadow: 0px 0px {glow_intensity}px rgba(233, 69, 96, {glow_intensity/200});
            }}
            
            QPushButton:pressed {{
                background-color: #cc3a52;
            }}
            
            QLineEdit, QComboBox {{
                background-color: {self.primary};
                color: {self.text};
                border: 2px solid {self.accent};
                border-radius: 4px;
                padding: 4px 8px;
                selection-background-color: {self.accent};
            }}
            
            QLineEdit:focus, QComboBox:focus {{
                border: 2px solid {self.hover};
                box-shadow: 0px 0px {glow_intensity}px rgba(233, 69, 96, {glow_intensity/200});
            }}
            
            QScrollArea {{
                background-color: rgba({self._hex_to_rgb(self.primary)}, {opacity});
                border: 1px solid {self.accent};
            }}
            
            QTabWidget::pane {{
                border: 2px solid {self.accent};
                background-color: {self.background};
            }}
            
            QTabBar::tab {{
                background-color: {self.primary};
                color: {self.text};
                padding: 6px 12px;
                border: 1px solid {self.border};
                border-bottom: none;
            }}
            
            QTabBar::tab:selected {{
                background-color: {self.accent};
                color: white;
                border: 2px solid {self.accent};
                border-bottom: none;
            }}
            
            QFrame {{
                background-color: rgba({self._hex_to_rgb(self.primary)}, {int(opacity)*0.8});
                border: 2px solid {self.accent};
                border-radius: 4px;
            }}
            
            QLabel {{
                color: {self.text};
            }}
            
            QStatusBar {{
                background-color: {self.primary};
                color: {self.accent};
                border-top: 2px solid {self.accent};
            }}
            
            QCheckBox {{
                color: {self.text};
                spacing: 5px;
            }}
            
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                background-color: {self.primary};
                border: 2px solid {self.accent};
                border-radius: 3px;
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {self.accent};
                border: 2px solid {self.accent};
            }}
        """
    
    @staticmethod
    def _hex_to_rgb(hex_color: str) -> str:
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"{r},{g},{b}"


class GradientTheme(Theme):
    """Theme with gradient-based visuals"""
    
    def __init__(self):
        super().__init__(
            name="Gradient",
            primary="#667eea",
            secondary="#764ba2",
            accent="#f093fb",
            background="#1a1a2e",
            text="#ffffff",
            border="#667eea",
            hover="#764ba2"
        )
    
    def get_stylesheet(self, translucent: bool = False, glow_intensity: int = 0) -> str:
        opacity = "180" if translucent else "255"
        glow = f"0px 0px {glow_intensity*2}px rgba(102, 126, 234, {glow_intensity/100});" if glow_intensity else ""
        
        return f"""
            * {{
                color: {self.text};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            
            QMainWindow, QDialog {{
                background-color: rgba({self._hex_to_rgb(self.background)}, {opacity});
                border: 2px solid;
                border-color: {self.primary};
                {glow}
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba({self._hex_to_rgb(self.primary)}, {opacity}), stop:1 rgba({self._hex_to_rgb(self.secondary)}, {opacity}));
            }}
            
            QWidget {{
                background-color: transparent;
            }}
            
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {self.primary}, stop:1 {self.secondary});
                color: {self.text};
                border: none;
                border-radius: 8px;
                padding: 6px 14px;
                font-weight: bold;
                font-size: 11px;
            }}
            
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {self.secondary}, stop:1 {self.accent});
                box-shadow: 0px 0px {glow_intensity}px rgba(102, 126, 234, {glow_intensity/200});
            }}
            
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #5568d3, stop:1 #6d3a92);
            }}
            
            QLineEdit, QComboBox {{
                background-color: rgba(30, 30, 50, {opacity});
                color: {self.text};
                border: 2px solid {self.primary};
                border-radius: 4px;
                padding: 4px 8px;
                selection-background-color: {self.primary};
            }}
            
            QLineEdit:focus, QComboBox:focus {{
                border: 2px solid {self.accent};
                box-shadow: 0px 0px {glow_intensity}px rgba(102, 126, 234, {glow_intensity/200});
            }}
            
            QScrollArea {{
                background-color: rgba(30, 30, 50, {opacity});
                border: 1px solid {self.primary};
            }}
            
            QTabWidget::pane {{
                border: 2px solid {self.primary};
                background-color: transparent;
            }}
            
            QTabBar::tab {{
                background-color: rgba(50, 50, 80, {opacity});
                color: {self.text};
                padding: 6px 12px;
                border: 1px solid {self.primary};
                border-bottom: none;
            }}
            
            QTabBar::tab:selected {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {self.primary}, stop:1 {self.secondary});
                color: white;
                border: 2px solid {self.accent};
                border-bottom: none;
            }}
            
            QFrame {{
                background-color: rgba(40, 40, 70, {int(opacity)*0.8});
                border: 1px solid {self.primary};
                border-radius: 4px;
            }}
            
            QLabel {{
                color: {self.text};
            }}
            
            QStatusBar {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {self.primary}, stop:1 {self.secondary});
                color: {self.text};
                border-top: 1px solid {self.border};
            }}
            
            QCheckBox {{
                color: {self.text};
                spacing: 5px;
            }}
            
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                background-color: rgba(50, 50, 80, {opacity});
                border: 2px solid {self.primary};
                border-radius: 3px;
            }}
            
            QCheckBox::indicator:checked {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {self.primary}, stop:1 {self.secondary});
                border: 2px solid {self.accent};
            }}
        """
    
    @staticmethod
    def _hex_to_rgb(hex_color: str) -> str:
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"{r},{g},{b}"


class AuraTheme(Theme):
    """Soft, ambient theme with aura/glow effects"""
    
    def __init__(self):
        super().__init__(
            name="Aura",
            primary="#1a0033",
            secondary="#330066",
            accent="#aa88ff",
            background="#0d001a",
            text="#e6d9ff",
            border="#663399",
            hover="#cc99ff"
        )
    
    def get_stylesheet(self, translucent: bool = False, glow_intensity: int = 0) -> str:
        opacity = "160" if translucent else "255"
        glow_val = glow_intensity * 3 if glow_intensity else 0
        glow = f"0px 0px {glow_val}px rgba(170, 136, 255, {glow_intensity/100});" if glow_intensity else ""
        
        return f"""
            * {{
                color: {self.text};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            
            QMainWindow, QDialog {{
                background-color: rgba({self._hex_to_rgb(self.background)}, {opacity});
                border: 1px solid rgba(170, 136, 255, 0.3);
                border-radius: 12px;
                {glow}
            }}
            
            QWidget {{
                background-color: transparent;
            }}
            
            QPushButton {{
                background-color: rgba({self._hex_to_rgb(self.secondary)}, 0.6);
                color: {self.text};
                border: 1px solid {self.accent};
                border-radius: 8px;
                padding: 6px 14px;
                font-weight: bold;
                font-size: 11px;
                box-shadow: 0px 0px 10px rgba(170, 136, 255, 0.3);
            }}
            
            QPushButton:hover {{
                background-color: rgba({self._hex_to_rgb(self.secondary)}, 0.8);
                border: 1px solid {self.hover};
                box-shadow: 0px 0px {glow_intensity+10}px rgba(170, 136, 255, {(glow_intensity+20)/200});
            }}
            
            QPushButton:pressed {{
                background-color: rgba({self._hex_to_rgb(self.primary)}, 0.9);
            }}
            
            QLineEdit, QComboBox {{
                background-color: rgba({self._hex_to_rgb(self.primary)}, 0.5);
                color: {self.text};
                border: 1px solid rgba({self._hex_to_rgb(self.accent)}, 0.5);
                border-radius: 6px;
                padding: 4px 8px;
                selection-background-color: rgba({self._hex_to_rgb(self.accent)}, 0.5);
            }}
            
            QLineEdit:focus, QComboBox:focus {{
                border: 1px solid {self.accent};
                box-shadow: 0px 0px {glow_intensity+10}px rgba(170, 136, 255, {(glow_intensity+20)/200});
            }}
            
            QScrollArea {{
                background-color: rgba({self._hex_to_rgb(self.primary)}, 0.3);
                border: 1px solid rgba({self._hex_to_rgb(self.accent)}, 0.3);
                border-radius: 8px;
            }}
            
            QTabWidget::pane {{
                border: 1px solid rgba({self._hex_to_rgb(self.accent)}, 0.3);
                background-color: transparent;
                border-radius: 8px;
            }}
            
            QTabBar::tab {{
                background-color: rgba({self._hex_to_rgb(self.primary)}, 0.4);
                color: {self.text};
                padding: 6px 12px;
                border: none;
                border-radius: 4px;
            }}
            
            QTabBar::tab:selected {{
                background-color: rgba({self._hex_to_rgb(self.secondary)}, 0.8);
                color: {self.accent};
                border: 1px solid {self.accent};
                box-shadow: 0px 0px 8px rgba(170, 136, 255, 0.5);
            }}
            
            QFrame {{
                background-color: rgba({self._hex_to_rgb(self.secondary)}, 0.2);
                border: 1px solid rgba({self._hex_to_rgb(self.accent)}, 0.3);
                border-radius: 8px;
            }}
            
            QLabel {{
                color: {self.text};
            }}
            
            QStatusBar {{
                background-color: rgba({self._hex_to_rgb(self.primary)}, 0.5);
                color: {self.accent};
                border-top: 1px solid rgba({self._hex_to_rgb(self.accent)}, 0.3);
                border-radius: 4px;
            }}
            
            QCheckBox {{
                color: {self.text};
                spacing: 5px;
            }}
            
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                background-color: rgba({self._hex_to_rgb(self.primary)}, 0.6);
                border: 1px solid rgba({self._hex_to_rgb(self.accent)}, 0.5);
                border-radius: 4px;
                box-shadow: 0px 0px 4px rgba(170, 136, 255, 0.2);
            }}
            
            QCheckBox::indicator:checked {{
                background-color: rgba({self._hex_to_rgb(self.accent)}, 0.6);
                border: 1px solid {self.accent};
                box-shadow: 0px 0px 8px rgba(170, 136, 255, 0.5);
            }}
        """
    
    @staticmethod
    def _hex_to_rgb(hex_color: str) -> str:
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"{r},{g},{b}"


class GlowTheme(Theme):
    """High-contrast theme with intense glow effects"""
    
    def __init__(self):
        super().__init__(
            name="Glow",
            primary="#000000",
            secondary="#0a0a15",
            accent="#00ff88",
            background="#050505",
            text="#00ff88",
            border="#00ff88",
            hover="#00ffaa"
        )
    
    def get_stylesheet(self, translucent: bool = False, glow_intensity: int = 0) -> str:
        opacity = "200" if translucent else "255"
        glow_val = glow_intensity * 4 if glow_intensity else 0
        glow = f"0px 0px {glow_val}px rgba(0, 255, 136, {glow_intensity/80});" if glow_intensity else ""
        
        return f"""
            * {{
                color: {self.text};
                font-family: 'Courier New', monospace;
            }}
            
            QMainWindow, QDialog {{
                background-color: rgba({self._hex_to_rgb(self.background)}, {opacity});
                border: 2px solid {self.accent};
                {glow}
            }}
            
            QWidget {{
                background-color: transparent;
            }}
            
            QPushButton {{
                background-color: transparent;
                color: {self.text};
                border: 2px solid {self.accent};
                border-radius: 4px;
                padding: 6px 14px;
                font-weight: bold;
                font-size: 11px;
                font-family: 'Courier New', monospace;
                box-shadow: 0px 0px 10px rgba(0, 255, 136, 0.5);
            }}
            
            QPushButton:hover {{
                background-color: rgba(0, 255, 136, 0.1);
                border-color: {self.hover};
                box-shadow: 0px 0px {glow_intensity+15}px rgba(0, 255, 136, {(glow_intensity+30)/200});
            }}
            
            QPushButton:pressed {{
                background-color: rgba(0, 255, 136, 0.2);
            }}
            
            QLineEdit, QComboBox {{
                background-color: rgba(0, 0, 0, 0.7);
                color: {self.text};
                border: 1px solid {self.accent};
                border-radius: 2px;
                padding: 4px 8px;
                selection-background-color: rgba(0, 255, 136, 0.3);
                font-family: 'Courier New', monospace;
                box-shadow: inset 0px 0px 4px rgba(0, 255, 136, 0.2);
            }}
            
            QLineEdit:focus, QComboBox:focus {{
                border: 2px solid {self.accent};
                box-shadow: 0px 0px {glow_intensity+15}px rgba(0, 255, 136, {(glow_intensity+30)/200}), inset 0px 0px 4px rgba(0, 255, 136, 0.3);
            }}
            
            QScrollArea {{
                background-color: rgba(0, 0, 0, 0.5);
                border: 1px solid {self.accent};
                box-shadow: inset 0px 0px 4px rgba(0, 255, 136, 0.1);
            }}
            
            QTabWidget::pane {{
                border: 1px solid {self.accent};
                background-color: rgba(0, 0, 0, 0.5);
            }}
            
            QTabBar::tab {{
                background-color: transparent;
                color: {self.text};
                padding: 6px 12px;
                border: 1px solid {self.accent};
                border-bottom: none;
            }}
            
            QTabBar::tab:selected {{
                background-color: rgba(0, 255, 136, 0.15);
                color: {self.accent};
                border: 2px solid {self.accent};
                border-bottom: none;
                box-shadow: 0px 0px 8px rgba(0, 255, 136, 0.6);
            }}
            
            QFrame {{
                background-color: transparent;
                border: 1px solid {self.accent};
                border-radius: 2px;
                box-shadow: 0px 0px 4px rgba(0, 255, 136, 0.2);
            }}
            
            QLabel {{
                color: {self.text};
            }}
            
            QStatusBar {{
                background-color: rgba(0, 0, 0, 0.7);
                color: {self.accent};
                border-top: 1px solid {self.accent};
                font-family: 'Courier New', monospace;
                box-shadow: 0px -2px 6px rgba(0, 255, 136, 0.2);
            }}
            
            QCheckBox {{
                color: {self.text};
                spacing: 5px;
                font-family: 'Courier New', monospace;
            }}
            
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                background-color: transparent;
                border: 2px solid {self.accent};
                border-radius: 2px;
                box-shadow: inset 0px 0px 3px rgba(0, 255, 136, 0.3);
            }}
            
            QCheckBox::indicator:checked {{
                background-color: rgba(0, 255, 136, 0.2);
                border: 2px solid {self.accent};
                box-shadow: 0px 0px 6px rgba(0, 255, 136, 0.6), inset 0px 0px 3px rgba(0, 255, 136, 0.3);
            }}
        """
    
    @staticmethod
    def _hex_to_rgb(hex_color: str) -> str:
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"{r},{g},{b}"


class LightTheme(Theme):
    """Light, clean theme for daytime use"""
    
    def __init__(self):
        super().__init__(
            name="Light",
            primary="#ffffff",
            secondary="#f5f5f5",
            accent="#2563eb",
            background="#f9fafb",
            text="#1f2937",
            border="#e5e7eb",
            hover="#1d4ed8"
        )
    
    def get_stylesheet(self, translucent: bool = False, glow_intensity: int = 0) -> str:
        opacity = "200" if translucent else "255"
        glow = f"0px 0px {glow_intensity*2}px rgba(37, 99, 235, {glow_intensity/200});" if glow_intensity else ""
        
        return f"""
            * {{
                color: {self.text};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            
            QMainWindow, QDialog {{
                background-color: rgba({self._hex_to_rgb(self.background)}, {opacity});
                border: 1px solid {self.border};
                {glow}
            }}
            
            QWidget {{
                background-color: transparent;
            }}
            
            QPushButton {{
                background-color: {self.accent};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 14px;
                font-weight: bold;
                font-size: 11px;
            }}
            
            QPushButton:hover {{
                background-color: {self.hover};
                box-shadow: 0px 2px 8px rgba(37, 99, 235, 0.3);
            }}
            
            QPushButton:pressed {{
                background-color: #1e40af;
            }}
            
            QLineEdit, QComboBox {{
                background-color: {self.primary};
                color: {self.text};
                border: 1px solid {self.border};
                border-radius: 4px;
                padding: 4px 8px;
                selection-background-color: {self.accent};
                selection-color: white;
            }}
            
            QLineEdit:focus, QComboBox:focus {{
                border: 2px solid {self.accent};
                box-shadow: 0px 0px {glow_intensity}px rgba(37, 99, 235, 0.2);
            }}
            
            QScrollArea {{
                background-color: {self.secondary};
                border: 1px solid {self.border};
            }}
            
            QTabWidget::pane {{
                border: 1px solid {self.border};
                background-color: {self.primary};
            }}
            
            QTabBar::tab {{
                background-color: {self.secondary};
                color: {self.text};
                padding: 6px 12px;
                border: 1px solid {self.border};
                border-bottom: none;
            }}
            
            QTabBar::tab:selected {{
                background-color: {self.accent};
                color: white;
                border: 1px solid {self.accent};
                border-bottom: none;
            }}
            
            QFrame {{
                background-color: {self.secondary};
                border: 1px solid {self.border};
                border-radius: 4px;
            }}
            
            QLabel {{
                color: {self.text};
            }}
            
            QStatusBar {{
                background-color: {self.secondary};
                color: {self.text};
                border-top: 1px solid {self.border};
            }}
            
            QCheckBox {{
                color: {self.text};
                spacing: 5px;
            }}
            
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                background-color: {self.primary};
                border: 1px solid {self.border};
                border-radius: 3px;
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {self.accent};
                border: 1px solid {self.accent};
            }}
        """
    
    @staticmethod
    def _hex_to_rgb(hex_color: str) -> str:
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"{r},{g},{b}"


class ThemeManager:
    """Manages available themes and theme switching"""
    
    THEMES = {
        ThemeMode.MIDNIGHT_CHASM: MidnightChasmTheme(),
        ThemeMode.CHROMA: ChromaTheme(),
        ThemeMode.GRADIENT: GradientTheme(),
        ThemeMode.AURA: AuraTheme(),
        ThemeMode.GLOW: GlowTheme(),
        ThemeMode.LIGHT: LightTheme(),
    }
    
    def __init__(self):
        self.current_theme = ThemeMode.MIDNIGHT_CHASM
        self.translucent = False
        self.glow_intensity = 0
    
    def get_theme(self, mode: ThemeMode = None) -> Theme:
        """Get a theme"""
        if mode is None:
            mode = self.current_theme
        return self.THEMES.get(mode, self.THEMES[ThemeMode.MIDNIGHT_CHASM])
    
    def get_stylesheet(self) -> str:
        """Get current stylesheet"""
        theme = self.get_theme()
        return theme.get_stylesheet(self.translucent, self.glow_intensity)
    
    def set_theme(self, mode: ThemeMode):
        """Set current theme"""
        self.current_theme = mode
    
    def set_translucent(self, value: bool):
        """Enable/disable translucency"""
        self.translucent = value
    
    def set_glow_intensity(self, intensity: int):
        """Set glow intensity (0-100)"""
        self.glow_intensity = max(0, min(100, intensity))
    
    def get_theme_names(self) -> list:
        """Get list of available theme names"""
        return [theme.name for theme in self.THEMES.values()]
    
    def get_theme_by_name(self, name: str) -> ThemeMode:
        """Get theme mode by name"""
        for mode, theme in self.THEMES.items():
            if theme.name == name:
                return mode
        return ThemeMode.MIDNIGHT_CHASM
