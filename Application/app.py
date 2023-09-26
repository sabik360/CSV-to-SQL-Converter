import sys
import csv
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QMessageBox, QDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the size of the main window
        self.setGeometry(100, 100, 500, 500)

        # Set the title of the main window
        self.setWindowTitle('CSV to SQL Converter')

        # Create input fields and button
        self.csv_button = QPushButton('Select the .csv file to convert', self)
        self.csv_button.setGeometry(50, 50, 400, 50)

        self.convert_button = QPushButton('Convert', self)
        self.convert_button.move(200, 120)

        # Connect the browse button to the browse_file method
        self.csv_button.clicked.connect(self.browse_file)

        # Connect the convert button to the convert_file method
        self.convert_button.clicked.connect(self.convert_file)

    def browse_file(self):
        # Open a file dialog to select a CSV file
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '', 'CSV Files (*.csv)')

        if file_name:
            # Open a file dialog to select a location to save the output text file
            save_file_name, _ = QFileDialog.getSaveFileName(self, 'Select Destination of Output file', '', 'Text Files (*.txt)')

            if save_file_name:
                self.convert_file(file_name, save_file_name)

    def convert_file(self, csv_file_name, txt_file_name):
        # Open the CSV file
        with open(csv_file_name, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            # Open the output text file
            with open(txt_file_name, 'w') as txt_file:
                # Get the header row of the CSV file
                header = next(csv_reader)

                # Get the table name from the input file name
                table_name = os.path.splitext(os.path.basename(csv_file_name))[0]

                # Write a MySQL CREATE TABLE command to the text file
                create_table_command = f"CREATE TABLE {table_name} ({', '.join([f'{column} VARCHAR(255)' for column in header])});\n"
                txt_file.write(create_table_command)

                # Write a MySQL INSERT INTO command to the text file for each row of data in the CSV file
                for row in csv_reader:
                    values = [f"'{value}'" for value in row]
                    insert_into_command = f"INSERT INTO {table_name} ({', '.join(header)}) VALUES ({', '.join(values)});\n"
                    txt_file.write(insert_into_command)

        # Show a message box indicating whether the conversion was successful or not
        QMessageBox.information(self, 'Conversion', f'Successfully converted {csv_file_name} to {txt_file_name}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())