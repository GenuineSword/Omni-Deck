"""PyQt6 UI components for the Media File Explorer"""

import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog,
    QPushButton, QLineEdit, QCheckBox, QScrollArea, QLabel, QMessageBox,
    QComboBox, QSpinBox, QProgressBar, QStatusBar, QTabWidget, QSlider,
    QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, QSize, QThread, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve, QPoint, QRect
from PyQt6.QtGui import QIcon, QPixmap, QDragEnterEvent, QDropEvent, QPainter
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QGridLayout, QFrame
import threading
import json
from pathlib import Path as PathlibPath

from config import MEDIA_TYPES, THUMB_SIZE, PREVIEW_SIZE
from file_manager import FileOrganizer, FileFilter
from themes import ThemeManager, ThemeMode


class FileGridWidget(QScrollArea):
    """Custom widget for displaying files in a grid with thumbnails"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.files = []
        self.selected_files = set()
        self.organizer = None
        
        # Setup UI
        self.setWidgetResizable(True)
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.setWidget(self.grid_widget)
        
        # Accept drops
        self.setAcceptDrops(True)
        self.grid_widget.setAcceptDrops(True)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Accept drag events"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """Handle dropped files"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            dropped_files = [Path(url.toLocalFile()) for url in urls]
            self.parent().handle_dropped_files(dropped_files)
    
    def display_files(self, files, organizer):
        """Display files in grid with thumbnails"""
        # Clear existing
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.files = files
        self.organizer = organizer
        
        col = 0
        row = 0
        cols = 4
        
        for file_path in files[:100]:  # Limit to 100 for performance
            file_frame = self._create_file_frame(file_path)
            self.grid_layout.addWidget(file_frame, row, col)
            col += 1
            if col >= cols:
                col = 0
                row += 1
        
        # Add spacer
        spacer = QWidget()
        self.grid_layout.addWidget(spacer, row + 1, 0)
        self.grid_layout.setRowStretch(row + 1, 1)
        self.grid_layout.setColumnStretch(cols, 1)
    
    def _create_file_frame(self, file_path: Path) -> QFrame:
        """Create a frame for a single file"""
        frame = QFrame()
        frame.setStyleSheet("QFrame { border: 1px solid #ccc; border-radius: 4px; }")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Thumbnail or icon
        thumb_label = QLabel()
        thumb_label.setFixedSize(THUMB_SIZE, THUMB_SIZE)
        thumb_label.setStyleSheet("background-color: #f0f0f0;")
        
        if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            try:
                pixmap = QPixmap(str(file_path))
                if not pixmap.isNull():
                    pixmap = pixmap.scaled(
                        THUMB_SIZE,
                        THUMB_SIZE,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                    thumb_label.setPixmap(pixmap)
                else:
                    raise ValueError("Empty pixmap")
            except Exception:
                thumb_label.setText("📷")
                thumb_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            category = self.organizer.categorize_file(file_path) if self.organizer else 'other'
            icon = MEDIA_TYPES.get(category, {}).get('icon', '📁')
            thumb_label.setText(icon)
            thumb_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            thumb_label.setStyleSheet("QLabel { font-size: 32px; background-color: #f0f0f0; }")
        
        layout.addWidget(thumb_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Filename
        name_label = QLabel(file_path.name)
        name_label.setMaximumWidth(THUMB_SIZE)
        name_label.setWordWrap(True)
        name_label.setStyleSheet("font-size: 9px;")
        layout.addWidget(name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Checkbox for selection
        checkbox = QCheckBox()
        checkbox.stateChanged.connect(lambda state: self._handle_file_selection(file_path, state))
        layout.addWidget(checkbox, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Store path in checkbox for later reference
        checkbox.file_path = file_path
        
        return frame
    
    def _handle_file_selection(self, file_path: Path, state):
        """Handle file selection"""
        if state:
            self.selected_files.add(file_path)
        else:
            self.selected_files.discard(file_path)


class MediaExplorerUI(QMainWindow):
    """Main UI for the Media File Explorer"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OmniDeck")
        self.setGeometry(100, 100, 1200, 800)
        
        self.organizer = None
        self.current_files = []
        self.selected_files = set()
        self.theme_manager = ThemeManager()
        self.config_file = PathlibPath.home() / '.media_explorer_config.json'
        self.section_buttons = {}
        self.active_section = None
        self.section_nav_visible = False
        self.setMouseTracking(True)
        
        # Load saved preferences
        self._load_preferences()
        
        # Setup UI
        self._setup_ui()
        self._apply_theme()
        self._start_boot_sequence()
    
    def _setup_ui(self):
        """Setup the main UI"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        self.section_nav = QWidget()
        self.section_nav.setVisible(False)
        self.section_nav.setFixedHeight(0)
        self.section_nav_layout = QHBoxLayout(self.section_nav)
        self.section_nav_layout.setContentsMargins(10, 6, 10, 6)
        self.section_nav_layout.setSpacing(8)
        self.section_nav.setObjectName("sectionNav")
        main_layout.addWidget(self.section_nav)
        
        # Top toolbar
        toolbar = self._create_toolbar()
        main_layout.addLayout(toolbar)
        
        # Theme and effects toolbar
        theme_toolbar = self._create_theme_toolbar()
        main_layout.addLayout(theme_toolbar)
        
        # Tab widget for different views
        tabs = QTabWidget()
        
        # Files grid tab
        self.grid_widget = FileGridWidget(self)
        tabs.addTab(self.grid_widget, "Files Grid")
        
        # Statistics tab
        stats_widget = QWidget()
        stats_layout = QVBoxLayout(stats_widget)
        self.stats_label = QLabel("Select a directory to scan")
        stats_layout.addWidget(self.stats_label)
        stats_layout.addStretch()
        tabs.addTab(stats_widget, "Statistics")
        
        main_layout.addWidget(tabs)
        
        # Rocket launch overlay
        self.launch_overlay = QWidget(central_widget)
        self.launch_overlay.setVisible(False)
        self.launch_overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.launch_overlay.setStyleSheet("background: transparent;")
        self.launch_overlay.raise_()
        self.rocket_size = 96
        self.rocket_pixmap = self._create_rocket_pixmap(self.rocket_size)
        self.rocket_label = QLabel(self.launch_overlay)
        self.rocket_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rocket_label.setPixmap(self.rocket_pixmap)
        self.rocket_label.setFixedSize(self.rocket_pixmap.size())
        self.rocket_label.setStyleSheet("background: transparent;")
        self.rocket_label.setVisible(False)
        self.rocket_label.raise_()
        
        # Boot intro overlay
        self.boot_overlay = QWidget(central_widget)
        self.boot_overlay.setGeometry(0, 0, central_widget.width(), central_widget.height())
        self.boot_overlay.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #030611, stop:0.55 #091227, stop:1 #132746);"
        )
        self.boot_overlay.raise_()
        self.boot_overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.boot_overlay.setVisible(False)

        self.boot_layout = QVBoxLayout(self.boot_overlay)
        self.boot_layout.setContentsMargins(40, 40, 40, 40)
        self.boot_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.boot_title = QLabel("OmniDeck")
        self.boot_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.boot_title.setStyleSheet("font-size: 26px; font-weight: 700; color: #f5fbff; letter-spacing: 2px;")
        self.boot_layout.addWidget(self.boot_title)

        self.boot_subtitle = QLabel("Preparing your launch...")
        self.boot_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.boot_subtitle.setStyleSheet("font-size: 13px; color: #96b4d6; margin-top: 8px;")
        self.boot_layout.addWidget(self.boot_subtitle)

        self.boot_progress = QProgressBar(self.boot_overlay)
        self.boot_progress.setRange(0, 100)
        self.boot_progress.setValue(0)
        self.boot_progress.setFixedWidth(260)
        self.boot_progress.setFixedHeight(8)
        self.boot_progress.setTextVisible(False)
        self.boot_progress.setStyleSheet(
            "QProgressBar { border: 1px solid #2f4d75; border-radius: 4px; background: #071120; }"
            "QProgressBar::chunk { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #5be7ff, stop:1 #2b7cff); border-radius: 4px; }"
        )
        self.boot_layout.addWidget(self.boot_progress, alignment=Qt.AlignmentFlag.AlignCenter)

        self.boot_rocket_label = QLabel(self.boot_overlay)
        self.boot_rocket_label.setFixedSize(self.rocket_size, self.rocket_size)
        self.boot_rocket_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.boot_rocket_label.setPixmap(self._create_rocket_pixmap(self.rocket_size))
        self.boot_rocket_label.setStyleSheet("background: transparent;")
        self.boot_rocket_label.setVisible(False)
        self.boot_rocket_label.raise_()

        self.boot_stars_label = QLabel("✦   ✦   ✦", self.boot_overlay)
        self.boot_stars_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.boot_stars_label.setStyleSheet("font-size: 28px; color: #fff7c2; letter-spacing: 8px; background: transparent;")
        self.boot_stars_label.setVisible(False)
        self.boot_stars_label.raise_()

        self.boot_streak_overlay = QWidget(self.boot_overlay)
        self.boot_streak_overlay.setGeometry(0, 0, 0, self.height())
        self.boot_streak_overlay.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255,255,255,0), stop:0.35 rgba(255,255,255,0.20), stop:0.75 rgba(255,255,255,0.05), stop:1 rgba(255,255,255,0));"
        )
        self.boot_streak_overlay.setVisible(False)
        self.boot_streak_overlay.raise_()

        self.boot_lightspeed_timer = QTimer(self)
        self.boot_lightspeed_timer.setSingleShot(True)
        self.boot_lightspeed_timer.timeout.connect(self._handle_lightspeed_duration_complete)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def _build_section_nav(self):
        """Create the hover-revealed section navigation bar"""
        self.section_nav_layout.addStretch()
        for category_key, info in MEDIA_TYPES.items():
            if category_key in {'other'}:
                continue
            button = QPushButton(f"{info['icon']} {info['display_name']}")
            button.setCheckable(True)
            button.clicked.connect(lambda checked, key=category_key: self._on_section_selected(key, checked))
            button.setFixedHeight(32)
            self.section_nav_layout.addWidget(button)
            self.section_buttons[category_key] = button

        self.close_section_btn = QPushButton("Close")
        self.close_section_btn.clicked.connect(self._close_active_section)
        self.close_section_btn.setVisible(False)
        self.close_section_btn.setFixedHeight(32)
        self.section_nav_layout.addWidget(self.close_section_btn)
        self.section_nav_layout.addStretch()

    def _show_section_nav(self):
        """Reveal the section navigation bar"""
        if self.section_nav_visible:
            return
        self.section_nav_visible = True
        self.section_nav.setVisible(True)
        self.section_nav.setFixedHeight(48)

    def _hide_section_nav(self):
        """Hide the section navigation bar"""
        if not self.section_nav_visible:
            return
        self.section_nav_visible = False
        self.section_nav.setFixedHeight(0)
        self.section_nav.setVisible(False)

    def _on_section_selected(self, category_key: str, checked: bool):
        """Handle section tab selection with rocket animation"""
        if not checked:
            self._close_active_section()
            return

        if self.active_section == category_key:
            self._close_active_section()
            return

        self.active_section = category_key
        for key, button in self.section_buttons.items():
            button.setChecked(key == category_key)

        self._set_category_filter(category_key)
        self.close_section_btn.setVisible(True)
        self._launch_rocket_animation()

    def _close_active_section(self):
        """Close the active section and animate the rocket returning"""
        if self.active_section is None:
            return

        self.active_section = None
        for button in self.section_buttons.values():
            button.setChecked(False)
        self.close_section_btn.setVisible(False)
        self._set_category_filter(None)
        self._launch_return_animation()

    def _set_category_filter(self, category_key):
        """Synchronize the category filter dropdown with the selected section"""
        if category_key is None:
            self.category_filter.setCurrentIndex(0)
        else:
            index = self.category_filter.findData(category_key)
            if index >= 0:
                self.category_filter.setCurrentIndex(index)
        self.apply_filters()

    def _create_rocket_pixmap(self, size: int) -> QPixmap:
        """Render the custom SVG rocket icon as a pixmap for the launch overlay"""
        svg_path = Path(__file__).resolve().parent / "assets" / "omni_deck_icon.svg"
        renderer = QSvgRenderer(str(svg_path))
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setViewport(0, 0, size, size)
            painter.setWindow(0, 0, 256, 256)
            renderer.render(painter)
        finally:
            painter.end()
        return pixmap

    def _launch_rocket_animation(self):
        """Animate a rocket launching from the top to the middle of the window"""
        if not self.rocket_label:
            return
        self.launch_overlay.setGeometry(0, 0, self.width(), self.height())
        self.launch_overlay.setVisible(True)
        self.rocket_label.setVisible(True)
        self.rocket_label.move(self.width() // 2 - self.rocket_size // 2, 18)
        self.rocket_label.raise_()

        animation = QPropertyAnimation(self.rocket_label, b"pos")
        animation.setDuration(900)
        animation.setStartValue(QPoint(self.width() // 2 - self.rocket_size // 2, 18))
        animation.setEndValue(QPoint(self.width() // 2 - self.rocket_size // 2, max(90, self.height() // 2 - self.rocket_size // 2 + 10)))
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.start()
        QTimer.singleShot(850, self._finish_launch_animation)

    def _finish_launch_animation(self):
        """Hide the overlay after the launch animation"""
        self.launch_overlay.setVisible(False)
        self.rocket_label.setVisible(False)

    def _launch_return_animation(self):
        """Animate the rocket returning to the top"""
        if not self.rocket_label:
            return
        self.launch_overlay.setGeometry(0, 0, self.width(), self.height())
        self.launch_overlay.setVisible(True)
        self.rocket_label.setVisible(True)
        self.rocket_label.move(self.width() // 2 - self.rocket_size // 2, max(90, self.height() // 2 - self.rocket_size // 2 + 10))
        self.rocket_label.raise_()

        animation = QPropertyAnimation(self.rocket_label, b"pos")
        animation.setDuration(900)
        animation.setStartValue(QPoint(self.width() // 2 - self.rocket_size // 2, max(90, self.height() // 2 - self.rocket_size // 2 + 10)))
        animation.setEndValue(QPoint(self.width() // 2 - self.rocket_size // 2, 18))
        animation.setEasingCurve(QEasingCurve.Type.InCubic)
        animation.start()
        QTimer.singleShot(850, self._finish_launch_animation)

    def resizeEvent(self, event):
        """Keep the overlay aligned with the window size"""
        super().resizeEvent(event)
        if self.launch_overlay is not None:
            self.launch_overlay.setGeometry(0, 0, self.width(), self.height())
        if self.boot_overlay is not None:
            self.boot_overlay.setGeometry(0, 0, self.width(), self.height())
            self.boot_streak_overlay.setGeometry(0, 0, 0, self.height())

    def _start_boot_sequence(self):
        """Show the startup intro, then let lightspeed handle loading and reveal the app."""
        if not self.boot_overlay:
            return

        self.boot_overlay.setVisible(True)
        self.boot_overlay.raise_()
        self.boot_progress.setValue(0)
        self.boot_subtitle.setText("Preparing your launch...")
        self.boot_rocket_label.setVisible(False)
        self.boot_stars_label.setVisible(False)
        self.boot_streak_overlay.setVisible(False)
        self.boot_lightspeed_timer.stop()
        self.boot_loading_complete = False
        self.boot_lightspeed_min_elapsed = False
        self._launch_boot_rocket()
        self._start_lightspeed_effect()
        QTimer.singleShot(180, self._advance_boot_loading)

    def _advance_boot_loading(self):
        """Advance the startup progress indicator until loading is complete."""
        current = self.boot_progress.value() + 20
        self.boot_progress.setValue(current)
        if current < 100:
            QTimer.singleShot(180, self._advance_boot_loading)
        else:
            self.boot_loading_complete = True
            self._maybe_finish_boot_transition()

    def _launch_boot_rocket(self):
        """Show the rocket once on first open, then let the loading transition take over."""
        self.boot_subtitle.setText("Engines engaged")
        self.boot_rocket_label.setVisible(True)
        self.boot_rocket_label.move(self.width() // 2 - self.rocket_size // 2, self.height() - self.rocket_size - 60)
        self.boot_rocket_label.raise_()

        rocket_animation = QPropertyAnimation(self.boot_rocket_label, b"pos")
        rocket_animation.setDuration(900)
        rocket_animation.setStartValue(QPoint(self.width() // 2 - self.rocket_size // 2, self.height() - self.rocket_size - 60))
        rocket_animation.setEndValue(QPoint(self.width() // 2 - self.rocket_size // 2, -self.rocket_size - 20))
        rocket_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        rocket_animation.start()
        QTimer.singleShot(900, lambda: self.boot_rocket_label.setVisible(False))

    def _start_lightspeed_effect(self):
        """Show a sustained lightspeed streak during loading."""
        self.boot_streak_overlay.setVisible(True)
        self.boot_streak_overlay.setGeometry(0, 0, 0, self.height())
        self.boot_streak_overlay.raise_()

        streak_animation = QPropertyAnimation(self.boot_streak_overlay, b"geometry")
        streak_animation.setDuration(700)
        streak_animation.setStartValue(QRect(0, 0, 0, self.height()))
        streak_animation.setEndValue(QRect(0, 0, self.width() * 1.6, self.height()))
        streak_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        streak_animation.start()
        self.boot_lightspeed_timer.start(3500)

    def _handle_lightspeed_duration_complete(self):
        """Allow the lightspeed effect to run for a minimum duration before finishing."""
        self.boot_lightspeed_min_elapsed = True
        self._maybe_finish_boot_transition()

    def _maybe_finish_boot_transition(self):
        """Finish the intro once loading is complete and the minimum lightspeed time has passed."""
        if not self.boot_loading_complete or not self.boot_lightspeed_min_elapsed:
            return
        self.boot_streak_overlay.setVisible(False)
        self.boot_stars_label.setVisible(True)
        self.boot_stars_label.raise_()
        self.boot_subtitle.setText("Stars aligning")
        QTimer.singleShot(900, self._finish_boot_transition)

    def _finish_boot_transition(self):
        """Hide the intro overlay and reveal the main experience."""
        self.boot_overlay.setVisible(False)
        self.boot_streak_overlay.setVisible(False)
        self.boot_stars_label.setVisible(False)
        self.status_bar.showMessage("Ready")

    def mouseMoveEvent(self, event):
        """Reveal the section nav when the pointer moves near the top"""
        if event.y() < 70:
            self._show_section_nav()
        elif self.section_nav_visible and event.y() > 140 and not self.section_nav.underMouse():
            self._hide_section_nav()
        super().mouseMoveEvent(event)

    def _create_toolbar(self) -> QHBoxLayout:
        """Create the top toolbar"""
        layout = QHBoxLayout()
        
        # Directory selection
        browse_btn = QPushButton("Browse Directory")
        browse_btn.clicked.connect(self.browse_directory)
        layout.addWidget(browse_btn)
        
        self.dir_label = QLineEdit()
        self.dir_label.setReadOnly(True)
        layout.addWidget(self.dir_label)
        
        layout.addSpacing(20)
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search files...")
        self.search_box.setMaximumWidth(200)
        self.search_box.textChanged.connect(self.apply_filters)
        layout.addWidget(self.search_box)
        
        # Category filter
        layout.addWidget(QLabel("Filter by:"))
        self.category_filter = QComboBox()
        self.category_filter.addItem("All Categories", None)
        for cat in MEDIA_TYPES.keys():
            self.category_filter.addItem(f"{MEDIA_TYPES[cat]['display_name']}", cat)
        self.category_filter.currentIndexChanged.connect(self.apply_filters)
        layout.addWidget(self.category_filter)
        
        layout.addSpacing(20)
        
        # Action buttons
        organize_btn = QPushButton("Organize Files")
        organize_btn.clicked.connect(self.organize_files)
        layout.addWidget(organize_btn)
        
        copy_btn = QPushButton("Copy & Organize")
        copy_btn.clicked.connect(self.copy_and_organize)
        layout.addWidget(copy_btn)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_files)
        layout.addWidget(refresh_btn)
        
        layout.addStretch()
        
        return layout
    
    def _create_theme_toolbar(self) -> QHBoxLayout:
        """Create theme and effects toolbar"""
        layout = QHBoxLayout()
        
        layout.addWidget(QLabel("Theme:"))
        
        # Theme selector
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(self.theme_manager.get_theme_names())
        self.theme_combo.setCurrentText(self.theme_manager.get_theme().name)
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        self.theme_combo.setMaximumWidth(150)
        layout.addWidget(self.theme_combo)
        
        layout.addSpacing(15)
        
        # Translucency checkbox
        self.translucent_check = QCheckBox("Translucent")
        self.translucent_check.setChecked(self.theme_manager.translucent)
        self.translucent_check.stateChanged.connect(self._on_translucent_changed)
        layout.addWidget(self.translucent_check)
        
        layout.addSpacing(15)
        
        # Glow intensity slider
        layout.addWidget(QLabel("Glow:"))
        self.glow_slider = QSlider(Qt.Orientation.Horizontal)
        self.glow_slider.setRange(0, 100)
        self.glow_slider.setValue(self.theme_manager.glow_intensity)
        self.glow_slider.setMaximumWidth(150)
        self.glow_slider.sliderMoved.connect(self._on_glow_changed)
        self.glow_slider.valueChanged.connect(self._on_glow_changed)
        layout.addWidget(self.glow_slider)
        
        self.glow_label = QLabel("0")
        self.glow_label.setMaximumWidth(30)
        layout.addWidget(self.glow_label)
        
        layout.addStretch()
        
        return layout
    
    def _on_theme_changed(self, theme_name: str):
        """Handle theme change"""
        theme_mode = self.theme_manager.get_theme_by_name(theme_name)
        self.theme_manager.set_theme(theme_mode)
        self._apply_theme()
        self._save_preferences()
    
    def _on_translucent_changed(self, state):
        """Handle translucency toggle"""
        is_checked = state == Qt.CheckState.Checked
        self.theme_manager.set_translucent(is_checked)
        self._apply_theme()
        self._save_preferences()
    
    def _on_glow_changed(self, value: int):
        """Handle glow intensity change"""
        self.theme_manager.set_glow_intensity(value)
        self.glow_label.setText(str(value))
        self._apply_theme()
        self._save_preferences()
    
    def _apply_theme(self):
        """Apply current theme to the application"""
        stylesheet = self.theme_manager.get_stylesheet()
        self.setStyleSheet(stylesheet)
    
    def _save_preferences(self):
        """Save theme preferences to file"""
        preferences = {
            'theme': self.theme_manager.current_theme.value,
            'translucent': self.theme_manager.translucent,
            'glow_intensity': self.theme_manager.glow_intensity
        }
        try:
            with open(self.config_file, 'w') as f:
                json.dump(preferences, f, indent=2)
        except Exception as e:
            print(f"Error saving preferences: {e}")
    
    def _load_preferences(self):
        """Load saved theme preferences"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    preferences = json.load(f)
                    
                theme_str = preferences.get('theme', ThemeMode.MIDNIGHT_CHASM.value)
                try:
                    theme_mode = ThemeMode(theme_str)
                    self.theme_manager.set_theme(theme_mode)
                except ValueError:
                    pass
                
                self.theme_manager.set_translucent(preferences.get('translucent', False))
                self.theme_manager.set_glow_intensity(preferences.get('glow_intensity', 0))
        except Exception as e:
            print(f"Error loading preferences: {e}")
    
    def browse_directory(self):
        """Open directory browser"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select a directory to scan"
        )
        
        if dir_path:
            self.dir_label.setText(dir_path)
            self.organizer = FileOrganizer(dir_path)
            self.refresh_files()
    
    def refresh_files(self):
        """Refresh file list"""
        if not self.organizer:
            QMessageBox.warning(self, "Warning", "Please select a directory first")
            return
        
        self.status_bar.showMessage("Scanning directory...")
        
        # Scan files (in background thread would be ideal, but doing sync for now)
        files_by_category = self.organizer.scan_directory()
        
        # Flatten all files
        self.current_files = []
        for category, files in files_by_category.items():
            self.current_files.extend(files)
        
        self.apply_filters()
        self.update_statistics()
        self.status_bar.showMessage(f"Found {len(self.current_files)} files")
    
    def apply_filters(self):
        """Apply search and category filters"""
        if not self.organizer:
            return
        
        search_term = self.search_box.text()
        selected_category = self.category_filter.currentData()
        
        filter_obj = FileFilter()
        categories = [selected_category] if selected_category else list(MEDIA_TYPES.keys())
        
        filtered = filter_obj.filter_files(
            self.current_files,
            search_term=search_term,
            categories=categories
        )
        
        self.grid_widget.display_files(filtered, self.organizer)
        self.selected_files = self.grid_widget.selected_files
    
    def update_statistics(self):
        """Update statistics display"""
        if not self.organizer:
            return
        
        stats = {}
        total_size = 0
        
        for category, files in self.organizer.files_by_category.items():
            count = len(files)
            size = sum(f.stat().st_size for f in files)
            total_size += size
            if count > 0:
                stats[category] = (count, size / (1024 * 1024))  # Convert to MB
        
        # Format stats
        stats_text = "File Statistics:\n\n"
        for category, (count, size_mb) in stats.items():
            if count > 0:
                display_name = MEDIA_TYPES.get(category, {}).get('display_name', category)
                stats_text += f"{display_name}: {count} files ({size_mb:.2f} MB)\n"
        
        stats_text += f"\nTotal: {sum(len(f) for f in self.organizer.files_by_category.values())} files "
        stats_text += f"({total_size / (1024 * 1024):.2f} MB)"
        
        self.stats_label.setText(stats_text)
    
    def handle_dropped_files(self, dropped_files):
        """Handle files dropped on the grid"""
        if not self.organizer:
            QMessageBox.warning(self, "Warning", "Please select a directory first")
            return
        
        for file_path in dropped_files:
            if file_path in self.grid_widget.files:
                self.grid_widget.selected_files.add(file_path)
    
    def organize_files(self):
        """Move selected files to organized directories"""
        if not self.grid_widget.selected_files:
            QMessageBox.warning(self, "Warning", "Please select files to organize")
            return
        
        files = list(self.grid_widget.selected_files)
        success, errors = self.organizer.organize_files(files, copy_mode=False)
        
        message = f"Successfully organized {success} files"
        if errors:
            message += f"\n\n{len(errors)} errors occurred:\n"
            message += "\n".join(errors[:5])  # Show first 5 errors
            if len(errors) > 5:
                message += f"\n... and {len(errors) - 5} more errors"
        
        QMessageBox.information(self, "Organization Complete", message)
        self.refresh_files()
    
    def copy_and_organize(self):
        """Copy selected files to organized directories"""
        if not self.grid_widget.selected_files:
            QMessageBox.warning(self, "Warning", "Please select files to organize")
            return
        
        files = list(self.grid_widget.selected_files)
        success, errors = self.organizer.organize_files(files, copy_mode=True)
        
        message = f"Successfully copied {success} files"
        if errors:
            message += f"\n\n{len(errors)} errors occurred:\n"
            message += "\n".join(errors[:5])  # Show first 5 errors
            if len(errors) > 5:
                message += f"\n... and {len(errors) - 5} more errors"
        
        QMessageBox.information(self, "Copy Complete", message)
        self.refresh_files()
