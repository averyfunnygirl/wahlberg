import markdown
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QTextCursor, QPdfWriter, QTextDocument, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QSplitter, QAction, QFileDialog, QColorDialog


class WahlbergMarkdownEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and icon
        self.setWindowTitle("Wahlberg Markdown Editor")
        self.setWindowIcon(QIcon("icon.png"))

        # Set default colors
        self.text_color = QColor("#cdd6f4")
        self.background_color = QColor("#1e1e2e")
        self.preview_color = QColor("#eff1f5")

        # Create text box for editing markdown
        self.textbox = QTextEdit(self)
        self.textbox.setAcceptRichText(False)
        self.textbox.setStyleSheet(f"color: {self.text_color.name()}; background-color: {self.background_color.name()}; padding: 20%;")

        # Create preview pane for displaying rendered markdown
        self.preview = QTextEdit(self)
        self.preview.setReadOnly(True)
        self.preview.setStyleSheet(f"background-color: {self.preview_color.name()}; padding: 20%;")

        # Create splitter to allow resizing of text box and preview pane
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.textbox)
        splitter.addWidget(self.preview)
        self.setCentralWidget(splitter)

        # Connect text box to preview update function
        self.textbox.textChanged.connect(self.update_preview)

        # Add "Export as PDF" action to File menu
        export_pdf_action = QAction("Export as PDF", self)
        export_pdf_action.triggered.connect(self.export_pdf)
        self.file_menu = self.menuBar().addMenu("File")
        self.file_menu.addAction(export_pdf_action)

        # Add "Open" action to File menu
        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        self.file_menu.addAction(open_action)

        # Add "Save" action to File menu
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        self.file_menu.addAction(save_action)

        # Add "Set Text Color" action to Edit menu
        set_text_color_action = QAction("Set Text Color", self)
        set_text_color_action.triggered.connect(self.set_text_color)
        self.edit_menu = self.menuBar().addMenu("Edit")
        self.edit_menu.addAction(set_text_color_action)

        # Add "Set Background Color" action to Edit menu
        set_background_color_action = QAction("Set Background Color", self)
        set_background_color_action.triggered.connect(self.set_background_color)
        self.edit_menu.addAction(set_background_color_action)

        # Add "Set Preview Color" action to Edit menu
        set_preview_color_action = QAction("Set Preview Color", self)
        set_preview_color_action.triggered.connect(self.set_preview_color)
        self.edit_menu.addAction(set_preview_color_action)

        # Set initial file path to None
        self.file_path = None

    def update_preview(self):
        # Get markdown from editor
        markdown_text = self.textbox.toPlainText()

        # Convert markdown to HTML with extensions
        html_text = markdown.markdown(markdown_text, extensions=["tables", "fenced_code", "codehilite", "toc"])

        # Set HTML in preview pane
        self.preview.setHtml(html_text)

    def export_pdf(self):
        # Get file name and path from user
        file_path, _ = QFileDialog.getSaveFileName(self, "Export as PDF", "", "PDF Files (*.pdf)")

        if file_path:
            # Create PDF writer
            pdf_writer = QPdfWriter(file_path)

            # Set document properties
            pdf_writer.setCreator("Wahlberg Markdown Editor")
            pdf_writer.setPageSize(QPdfWriter.A4)

            # Create document and cursor
            document = QTextDocument()
            cursor = QTextCursor(document)

            # Get markdown from text box
            markdown_text = self.textbox.toPlainText()

            # Convert markdown to HTML with extensions
            html = markdown.markdown(markdown_text, extensions=["tables", "fenced_code", "codehilite", "toc"])

            # Set HTML on document
            cursor.insertHtml(html)

            # Print document to PDF
            document.print_(pdf_writer)

    def set_text_color(self):
        # Get new text color from color picker dialog
        color = QColorDialog.getColor(self.text_color, self, "Select Text Color")

        if color.isValid():
            # Update text color and text box style sheet
            self.text_color = color
            self.textbox.setStyleSheet(f"color: {self.text_color.name()}; background-color: {self.background_color.name()}; padding: 10%;")

    def set_background_color(self):
        # Get new background color from color picker dialog
        color = QColorDialog.getColor(self.background_color, self, "Select Background Color")

        if color.isValid():
            # Update background color and text box style sheet
            self.background_color = color
            self.textbox.setStyleSheet(f"color: {self.text_color.name()}; background-color: {self.background_color.name()}; padding: 10%;")

    def set_preview_color(self):
        # Get new preview color from color picker dialog
        color = QColorDialog.getColor(self.preview_color, self, "Select Preview Color")

        if color.isValid():
            # Update preview color and preview pane style sheet
            self.preview_color = color
            self.preview.setStyleSheet(f"background-color: {self.preview_color.name()}; padding: 10%;")

    def open_file(self):
        # Get file path from user
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Markdown File", "", "Markdown Files (*.md)")

        if file_path:
            # Open file and set text box text
            with open(file_path, "r") as f:
                self.textbox.setText(f.read())

            # Set file path
            self.file_path = file_path

    def save_file(self):
        if self.file_path:
            # Save changes to existing file
            with open(self.file_path, "w") as f:
                f.write(self.textbox.toPlainText())
        else:
            # Get file path from user
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Markdown File", "", "Markdown Files (*.md)")

            if file_path:
                # Save new file and set file path
                with open(file_path, "w") as f:
                    f.write(self.textbox.toPlainText())

                self.file_path = file_path


if __name__ == "__main__":
    # Create application and window
    app = QApplication([])
    window = WahlbergMarkdownEditor()
    window.show()

    # Run event loop
    app.exec_()
