# Author Darwin Borsato
import os
import shutil
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt


class DirectoryRenamer(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the GUI
        self.setWindowTitle("Directory Renaming Tool")
        self.setGeometry(100, 100, 500, 200)

        # Set up the widgets
        self.dir_label = QLabel("No directory selected")
        self.new_dir_label = QLabel("New directory name:")
        self.new_dir_input = QLineEdit()
        self.skip_button = QPushButton("Skip")
        self.rename_button = QPushButton("Rename")
        self.quit_button = QPushButton("Quit")
        self.folder_dialog_button = QPushButton("Select Parent Directory")

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.folder_dialog_button)
        layout.addWidget(self.dir_label)
        layout.addWidget(self.new_dir_label)
        layout.addWidget(self.new_dir_input)
        layout.addWidget(self.skip_button)
        layout.addWidget(self.rename_button)
        layout.addWidget(self.quit_button)
        self.setLayout(layout)

        # Connect the signals to the slots
        self.folder_dialog_button.clicked.connect(self.select_directory)
        self.skip_button.clicked.connect(self.skip_directory)
        self.rename_button.clicked.connect(self.rename_directory)
        self.quit_button.clicked.connect(self.quit_program)

        # Set up the directory list and current directory index
        self.directories = []
        self.current_dir_index = -1

    def select_directory(self):
        # Open a folder dialog to select a parent directory
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.Directory)
        parent_directory = folder_dialog.getExistingDirectory(self, "Select Parent Directory")

        if parent_directory:
            # Get a list of all directories in the parent directory
            self.directories = [d for d in os.listdir(parent_directory) if os.path.isdir(os.path.join(parent_directory, d))]

            if len(self.directories) > 0:
                # Show the first directory in the list
                self.current_dir_index = 0
                self.show_directory()

        # Save the selected parent directory for later use
        self.parent_directory = parent_directory
        # FUCK KEVIN
    def show_directory(self):
        # Show the current directory name in the label
        self.dir_label.setText(self.directories[self.current_dir_index])

    def skip_directory(self):
        # Move to the next directory in the list
        self.current_dir_index += 1

        if self.current_dir_index >= len(self.directories):
            # If we've reached the end of the list, reset the index
            self.current_dir_index = 0

        # Show the next directory in the list
        self.show_directory()

    def rename_directory(self):
        # Get the current directory path
        dir_path = os.path.join(self.parent_directory, self.directories[self.current_dir_index])

        # Get the new directory name from the input field
        new_dir_name = self.new_dir_input.text()

        #Check for same filename
        if new_dir_name in self.files:


        # Rename the directory with the new directory name
            os.rename(dir_path, os.path.join(self.parent_directory, new_dir_name))

        # Remove the renamed directory from the directory list
        self.directories.pop(self.current_dir_index)

        if len(self.directories) > 0:
            # Move to the next directory in the list
            self.current_dir_index %= len(self.directories)

            # Show the next directory in the list
            self.show_directory()
        else:
            # If there are no more directories, clear the label and input field
            self.dir_label.setText("No directory selected")
            self.new_dir_input.setText("")

    def quit_program(self):
        # Quit the program
        sys.exit()

