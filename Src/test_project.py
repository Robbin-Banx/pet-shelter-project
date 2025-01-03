import pytest
from classes import Patient
from project import create_entry
from project import search_base
from project import remove_entry
from project import database
import csv

def test_Patient_ValueError_for_species():

    with pytest.raises(ValueError, match="Patient can be a dog or a cat."):
        Patient("male", "male", "Harry", "4")

def test_Patient_ValueError_for_gender():

    with pytest.raises(ValueError, match="Patient must be male or female."):
        Patient("dog", "dog", "Harry", "4")

def test_Patient_ValueError_for_name():

    with pytest.raises(ValueError, match="Name must be at least one word"):
        Patient("dog", "male", "", "Harry")


def test_Patient_ValueError_for_age():

    with pytest.raises(ValueError, match="Age must be a number"):
        Patient("dog", "male", "Harry", "Harry")

def test_Patient_str():
    species = "Dog"
    gender = "male"
    name = "Harry"
    age = "4"
    test_patient = Patient(species, gender, name, age)
    assert str(test_patient) == f"Patient is a {gender} {species}. Patient's name is {name} and is {age} years old."

def test_Patient_eq_False():
    test_patient_1=Patient("dog", "male", "Harry", "4")
    test_patient_2=Patient("cat", "male", "Ronald", "4")
    assert (test_patient_1 == test_patient_2) == False

def test_Patient_eq_True():
    test_patient_1=Patient("dog", "male", "Harry", "4")
    test_patient_2=Patient("dog", "male", "Harry", "4")
    assert (test_patient_1 == test_patient_2) == True


def test_create_entry():
    test_patient_1 = Patient("cat", "male", "Ronald", "4")
    create_entry(test_patient_1, silent=True)
    subjects = []
    with open(database, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            species = row.get("Species")
            gender = row.get("Gender")
            name = row.get("Name")
            age = row.get("Age")
            test_patient = Patient(species, gender, name, age)
            subjects.append(test_patient)
    assert test_patient_1 in subjects


def test_remove_entry():
    test_patient_1 = Patient("cat", "male", "Ronald", "4")
    remove_entry(test_patient_1, silent=True)
    subjects = []
    with open(database, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            species = row.get("Species")
            gender = row.get("Gender")
            name = row.get("Name")
            age = row.get("Age")
            test_patient = Patient(species, gender, name, age)
            subjects.append(test_patient)
    assert test_patient_1 not in subjects
