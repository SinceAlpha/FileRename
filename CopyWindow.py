# Author Darwin Borsato
import os
import shutil
import sys

from PyQt5.QtWidgets import QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QApplication

from MainWindow import MainWindow


class CopyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the GUI
        self.setWindowTitle("File Copying Tool")
        self.setGeometry(100, 100, 500, 200)

        # Set up the widgets
        self.file_label = QLabel("No file selected")
        self.new_file_label = QLabel("New filename:")
        self.new_file_input = QLineEdit()
        self.copy_button = QPushButton("Copy")
        self.file_dialog_button = QPushButton("Select File")
        self.quit_button = QPushButton("Quit")

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.file_dialog_button)
        layout.addWidget(self.file_label)
        layout.addWidget(self.new_file_label)
        layout.addWidget(self.new_file_input)
        layout.addWidget(self.copy_button)
        layout.addWidget(self.quit_button)
        self.setLayout(layout)

        # Connect the signals to the slots
        self.file_dialog_button.clicked.connect(self.select_file)
        self.copy_button.clicked.connect(self.copy_file)
        self.quit_button.clicked.connect(self.quit_program)

        # Set up the file path variable
        self.file_path = ""

    def select_file(self):
        # Open a file dialog to select a file
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")

        if file_path:
            # Show the selected file name in the label
            self.file_label.setText(os.path.basename(file_path))
            self.file_path = file_path

    def copy_file(self):
        if self.file_path:
            # Get the new file name from the input field
            new_file_name = self.new_file_input.text()

            # Generate the new file path by incrementing the number before the extension
            new_file_path = self.increment_filename(self.file_path, new_file_name)

            # Copy the file to the new path
            shutil.copy2(self.file_path, new_file_path)

    @staticmethod
    def increment_filename(file_path, new_file_name):
        directory, old_file_name = os.path.split(file_path)
        name, extension = os.path.splitext(old_file_name)

        new_name = "{}{}".format(new_file_name, extension)
        new_file_path = os.path.join(directory, new_name)

        index = 1
        while os.path.exists(new_file_path):
            new_name = "{}-{}{}".format(new_file_name, index, extension)
            new_file_path = os.path.join(directory, new_name)
            index += 1

        return new_file_path

    def quit_program(self):
        # Quit the program
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    copy_window = CopyWindow()

    # Connect the 'switch_to_copy' button to show the copy window
    main_window.copy_file_button.clicked.connect(copy_window.show)
    main_window.copy_file_button.clicked.connect(main_window.hide)

    main_window.show()

    # Run the event loop until the user quits
    sys.exit(app.exec_())
