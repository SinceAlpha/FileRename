# Author Darwin Borsato
import os
import shutil
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog
from PyQt5.QtCore import Qt




class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the GUI
        self.setWindowTitle("File Renaming Tool")
        self.setGeometry(100, 100, 500, 200)

        # Set up the widgets
        self.file_label = QLabel("No file selected")
        self.copy_file_button = QPushButton("Switch to Copy File")
        self.new_file_label = QLabel("New filename:")
        self.new_file_input = QLineEdit()
        self.skip_button = QPushButton("Skip")
        self.rename_button = QPushButton("Rename")
        self.quit_button = QPushButton("Quit")
        self.file_dialog_button = QPushButton("Select Directory")

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.file_dialog_button)
        layout.addWidget(self.copy_file_button)
        layout.addWidget(self.file_label)
        layout.addWidget(self.new_file_label)
        layout.addWidget(self.new_file_input)
        layout.addWidget(self.skip_button)
        layout.addWidget(self.rename_button)
        layout.addWidget(self.quit_button)
        self.setLayout(layout)

        # Connect the signals to the slots
        self.file_dialog_button.clicked.connect(self.select_directory)
        self.skip_button.clicked.connect(self.skip_file)
        self.rename_button.clicked.connect(self.rename_file)
        self.quit_button.clicked.connect(self.quit_program)

        # Set up the file list and current file index
        self.files = []
        self.current_file_index = -1

    def select_directory(self):
        # Open a file dialog to select a directory
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.Directory)
        directory = file_dialog.getExistingDirectory(self, "Select Directory")

        if directory:
            # Get a list of all files in the directory
            self.files = os.listdir(directory)

            if len(self.files) > 0:
                # Show the first file in the list
                self.current_file_index = 0
                self.show_file()

        # Save the selected directory for later use
        self.directory = directory

    def show_file(self):
        # Show the current file name in the label
        self.file_label.setText(self.files[self.current_file_index])

    def skip_file(self):
        # Move to the next file in the list
        self.current_file_index += 1

        if self.current_file_index >= len(self.files):
            # If we've reached the end of the list, reset the index
            self.current_file_index = 0

        # Show the next file in the list
        self.show_file()

    # def rename_file(self):
    #     # Get the current file path
    #     file_path = os.path.join(self.directory, self.files[self.current_file_index])
    #
    #     # Get the new file name from the input field
    #     new_file_name = self.new_file_input.text()
    #
    #     # Rename the file with the new file name
    #     os.rename(file_path, os.path.join(self.directory, new_file_name))
    #
    #     # Remove the renamed file from the file list
    #     self.files.pop(self.current_file_index)
    #
    #     if len(self.files) > 0:
    #         # Move to the next file in the list
    #         self.current_file_index %= len(self.files)
    #
    #         # Show the next file in the list
    #         self.show_file()
    #
    #         # Increment the new_file_input value by 1
    #         try:
    #             current_value = int(self.new_file_input.text())
    #             self.new_file_input.setText(str(current_value + 1))
    #         except ValueError:
    #             # If the input is not an integer, leave it unchanged
    #             pass
    #
    #     else:
    #         # If there are no more files, clear the label and input field
    #         self.file_label.setText("No file selected")
    #         self.new_file_input.setText("")

    def rename_file(self):
        # Get the current file path
        file_path = os.path.join(self.directory, self.files[self.current_file_index])

        # Get the new file name from the input field
        new_file_name = self.new_file_input.text()

        # Rename the file with the new file name
        os.rename(file_path, os.path.join(self.directory, new_file_name))

        # Remove the renamed file from the file list
        self.files.pop(self.current_file_index)

        if len(self.files) > 0:
            # Move to the next file in the list
            self.current_file_index %= len(self.files)

            # Show the next file in the list
            self.show_file()
        else:
            # If there are no more files, clear the label and input field
            self.file_label.setText("No file selected")
            self.new_file_input.setText("")

    def quit_program(self):
        # Quit the program
        sys.exit()

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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.copy_file()
        else:
            super().keyPressEvent(event)

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



if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    copy_window = CopyWindow()

    # Connect the 'switch_to_copy' button to show the copy window
    main_window.copy_file_button.clicked.connect(copy_window.show)
    main_window.copy_file_button.clicked.connect(main_window.hide)
    # main_window = MainWindow()
    main_window.show()

    # Run the event loop until the user quits
    sys.exit(app.exec_())
