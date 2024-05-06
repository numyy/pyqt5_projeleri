import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QMessageBox
from PyQt5.QtCore import Qt

class User:
   def __init__(self, name, age, gender):
       self.name = name
       self.age = age
       self.gender = gender
       self.health_records = []
       self.exercises = []

   def add_record(self, record):
       self.health_records.append(record)

   def add_exercise(self, exercise):
       self.exercises.append(exercise)

   def generate_report(self):
       report = f"Name: {self.name}\nAge: {self.age}\nGender: {self.gender}\n\nHealth Records:\n"
       for record in self.health_records:
           report += str(record) + "\n"
       report += "\nExercises:\n"
       for exercise in self.exercises:
           report += str(exercise) + "\n"
       return report

class HealthRecord:
   def __init__(self, date, measurement, value):
       self.date = date
       self.measurement = measurement
       self.value = value

   def __str__(self):
       return f"{self.date} - {self.measurement}: {self.value}"

class Exercise:
   def __init__(self, name, duration, repetitions):
       self.name = name
       self.duration = duration
       self.repetitions = repetitions

   def __str__(self):
       return f"{self.name} - Duration: {self.duration} mins, Repetitions: {self.repetitions}"

class HealthTrackerApp(QMainWindow):
   def __init__(self):
       super().__init__()
       self.setWindowTitle("Kişisel Sağlık Takip Uygulaması")
       self.setMinimumSize(800, 600)

       self.user = None

       # Create widgets
       self.name_label = QLabel("Name:")
       self.name_input = QLineEdit()
       self.age_label = QLabel("Age:")
       self.age_input = QLineEdit()
       self.gender_label = QLabel("Gender:")
       self.gender_input = QComboBox()
       self.gender_input.addItems(["Male", "Female", "Other"])

       self.health_record_table = QTableWidget()
       self.health_record_table.setColumnCount(3)
       self.health_record_table.setHorizontalHeaderLabels(["Date", "Measurement", "Value"])
       self.health_record_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

       self.exercise_table = QTableWidget()
       self.exercise_table.setColumnCount(3)
       self.exercise_table.setHorizontalHeaderLabels(["Name", "Duration", "Repetitions"])
       self.exercise_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

       self.add_record_button = QPushButton("Add Health Record")
       self.add_record_button.clicked.connect(self.add_health_record)

       self.add_exercise_button = QPushButton("Add Exercise")
       self.add_exercise_button.clicked.connect(self.add_exercise)

       self.generate_report_button = QPushButton("Generate Report")
       self.generate_report_button.clicked.connect(self.generate_report)

       # Layout
       user_info_layout = QHBoxLayout()
       user_info_layout.addWidget(self.name_label)
       user_info_layout.addWidget(self.name_input)
       user_info_layout.addWidget(self.age_label)
       user_info_layout.addWidget(self.age_input)
       user_info_layout.addWidget(self.gender_label)
       user_info_layout.addWidget(self.gender_input)

       table_layout = QVBoxLayout()
       table_layout.addWidget(self.health_record_table)
       table_layout.addWidget(self.exercise_table)

       button_layout = QHBoxLayout()
       button_layout.addWidget(self.add_record_button)
       button_layout.addWidget(self.add_exercise_button)
       button_layout.addWidget(self.generate_report_button)

       main_layout = QVBoxLayout()
       main_layout.addLayout(user_info_layout)
       main_layout.addLayout(table_layout)
       main_layout.addLayout(button_layout)

       central_widget = QWidget()
       central_widget.setLayout(main_layout)
       self.setCentralWidget(central_widget)

   def add_health_record(self):
       if self.user is None:
           QMessageBox.warning(self, "Warning", "Please create a user profile first.")
           return

       date, ok = QInputDialog.getText(self, "Add Health Record", "Enter Date (YYYY-MM-DD):")
       if not ok:
           return

       measurement, ok = QInputDialog.getText(self, "Add Health Record", "Enter Measurement:")
       if not ok:
           return

       value, ok = QInputDialog.getText(self, "Add Health Record", "Enter Value:")
       if not ok:
           return

       record = HealthRecord(date, measurement, value)
       self.user.add_record(record)

       row_count = self.health_record_table.rowCount()
       self.health_record_table.insertRow(row_count)
       self.health_record_table.setItem(row_count, 0, QTableWidgetItem(record.date))
       self.health_record_table.setItem(row_count, 1, QTableWidgetItem(record.measurement))
       self.health_record_table.setItem(row_count, 2, QTableWidgetItem(str(record.value)))

   def add_exercise(self):
       if self.user is None:
           QMessageBox.warning(self, "Warning", "Please create a user profile first.")
           return

       name, ok = QInputDialog.getText(self, "Add Exercise", "Enter Exercise Name:")
       if not ok:
           return

       duration, ok = QInputDialog.getInt(self, "Add Exercise", "Enter Duration (minutes):")
       if not ok:
           return

       repetitions, ok = QInputDialog.getInt(self, "Add Exercise", "Enter Repetitions:")
       if not ok:
           return

       exercise = Exercise(name, duration, repetitions)
       self.user.add_exercise(exercise)

       row_count = self.exercise_table.rowCount()
       self.exercise_table.insertRow(row_count)
       self.exercise_table.setItem(row_count, 0, QTableWidgetItem(exercise.name))
       self.exercise_table.setItem(row_count, 1, QTableWidgetItem(str(exercise.duration)))
       self.exercise_table.setItem(row_count, 2, QTableWidgetItem(str(exercise.repetitions)))

   def generate_report(self):
       if self.user is None:
           QMessageBox.warning(self, "Warning", "Please create a user profile first.")
           return

       report = self.user.generate_report()
       QMessageBox.information(self, "Report", report)

   def create_user_profile(self):
       name = self.name_input.text()
       age = self.age_input.text()
       gender = self.gender_input.currentText()

       if not name or not age:
           QMessageBox.warning(self, "Warning", "Please enter name and age.")
           return

       try:
           age = int(age)
       except ValueError:
           QMessageBox.warning(self, "Warning", "Invalid age format.")
           return

       self.user = User(name, age, gender)
       QMessageBox.information(self, "Success", "User profile created successfully.")

if __name__ == "__main__":
   app = QApplication(sys.argv)
   health_tracker = HealthTrackerApp()
   health_tracker.show()
   sys.exit(app.exec_())