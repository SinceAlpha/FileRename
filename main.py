# Author Darwin Borsato
import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the GUI
        self.setWindowTitle("File Renaming Tool")
        self.setGeometry(100, 100, 500, 200)

        # Set up the widgets
        self.file_label = QLabel("No file selected")
        self.new_file_label = QLabel("New filename:")
        self.new_file_input = QLineEdit()
        self.skip_button = QPushButton("Skip")
        self.rename_button = QPushButton("Rename")
        self.quit_button = QPushButton("Quit")
        self.file_dialog_button = QPushButton("Select Directory")

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.file_dialog_button)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)


    main_window = MainWindow()
    main_window.show()

    # Run the event loop until the user quits
    sys.exit(app.exec_())
