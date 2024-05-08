from PyQt6.QtWidgets import *
from gui import *
import csv
import os.path
import re


class Logic(QMainWindow, Ui_MainWindow):
    """ A class to request voting information through a GUI and output the information into a CSV file."""

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        # First get current data in csv file
        self.data_dictionary: dict = {}
        self.read_data()

        # Save new data to csv file
        self.button_submit.clicked.connect(lambda: self.submit())
        self.button_unchecked.hide()

    def read_data(self) -> csv:
        file_exists: bool = os.path.exists('vote_list.csv')
        if not file_exists:
            file = open('vote_list.csv', 'x')
            file.close()
        else:
            with open('vote_list.csv', 'r') as csv_file:
                content = csv.reader(csv_file, delimiter=',')
                for line in content:
                    voter_id: str = line[0]
                    voter_candidate: str = line[1]
                    self.data_dictionary[voter_id] = voter_candidate  # {'123': John, '345': Jane}

    def submit(self) -> csv:
        vote_id: str = self.input_id.text()
        if vote_id.isnumeric():
            pass
        else:
            self.label_Error.setText('Invalid Voter ID')
            return

        # Checking candidate vote
        vote_candidate = 'Invalid'
        if self.radio_candidate_1.isChecked():
            vote_candidate = 'Jane'
        elif self.radio_candidate_2.isChecked():
            vote_candidate = 'John'
        else:
            self.label_Error.setText('Please Select a Candidate')
            return

        # Checking if user already voted
        if vote_id in self.data_dictionary.keys():
            self.label_Error.setText('Already Voted')
            return

        # Save data to file
        with open('vote_list.csv', 'a', newline='') as write_file:
            vote_info = csv.writer(write_file)
            vote_info.writerow([vote_id, vote_candidate])
            self.label_Error.setText('Your vote has been recorded.')

        self.input_id.clear()
        self.button_unchecked.setChecked(True)
