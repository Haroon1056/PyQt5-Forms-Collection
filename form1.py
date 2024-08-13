import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import mysql.connector
from mysql.connector import Error

class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('User Form')
        
        self.layout = QFormLayout()
        
        self.firstName = QLineEdit()
        self.lastName = QLineEdit()
        self.email = QLineEdit()
        
        self.layout.addRow('First Name', self.firstName)
        self.layout.addRow('Last Name', self.lastName)
        self.layout.addRow('Email', self.email)
        
        self.submitBtn = QPushButton('Submit')
        self.submitBtn.clicked.connect(self.submitData)
        
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.layout)
        self.mainLayout.addWidget(self.submitBtn)
        
        self.setLayout(self.mainLayout)
    
    def submitData(self):
        first_name = self.firstName.text()
        last_name = self.lastName.text()
        email = self.email.text()
        
        if not first_name or not last_name or not email:
            QMessageBox.warning(self, 'Input Error', 'All fields are required!')
            return
        
        if save_to_db(first_name, last_name, email):
            QMessageBox.information(self, 'Success', 'Data saved successfully!')
        else:
            QMessageBox.critical(self, 'Failure', 'Failed to save data!')

def save_to_db(first_name, last_name, email):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='formdb',
            user='root',
            password='1056'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            sql = "INSERT INTO users (first_name, last_name, email) VALUES (%s, %s, %s)"
            values = (first_name, last_name, email)
            cursor.execute(sql, values)
            connection.commit()
            return True
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def main():
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
