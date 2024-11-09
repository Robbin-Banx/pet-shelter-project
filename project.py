"""
Pet Shelter Registry
=====================

This file is a basic program to keep track of the patients of a pet shelter. This is a final project for the CS50P course, led by David A. Malan.

Author: Aleksandar Kostadinov
Github: Robbin-Banx

Location: Sofia, Bulgaria
Date: 10.06.2024
Last Modified: 09.11.2024

"""

import sys
import csv
import re
import os
from tabulate import tabulate

file_name = "database.csv"


class Patient:
    """"
    A class used to represent types of patients.


    """

    def __init__(
        self, species: str = None, gender: str = None, name: str = None, age: int = None
    ):
        if species != None:
            self.species = species
        else:
            self.species = input("What is the patient's species? ").capitalize()

        if gender != None:
            self.gender = gender
        else:
            self.gender = input("What is the patient male or female? ").lower()

        if name != None:
            self.name = name
        else:
            self.name = input("What is patient's name? ").capitalize()

        if age != None:
            self.age = age
        else:
            self.age = input("What's the patient's age? ")

    def __str__(self):
        return str(f"Patient is a {self.gender} {self.species}. Patient's name is {self.name} and is {self.age} years old.")

    def __iter__(self):
        yield "Species", self.species
        yield "Gender", self.gender
        yield "Name", self.name
        yield "Age", self.age

    def __eq__(self, other):
        # don't attempt to compare against unrelated types
        if not isinstance(other, Patient):
            return NotImplemented

        return (
            self.species == other.species and
            self.gender == other.gender and
            self.name == other.name and
            self.age == other.age
        )

    @property
    def species(self):
        return self._species

    @species.setter
    def species(self, value):
        value = value.capitalize()
        if value == "Dog" or value == "Cat":
            self._species = value
        else:
            raise ValueError("Patient can be a dog or a cat.")

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        if value == "male" or value == "female":
            self._gender = value
        else:
            raise ValueError("Patient must be male or female.")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if re.search(r"\w+", value):
            self._name = value
        else:
            raise ValueError("Name must be at least one word")

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if re.search(r"\d+", value):
            self._age = value
        else:
            raise ValueError("Age must be a number")

    def write(self, silent: bool = False):

        with open(file_name, "r") as file:
            reader = csv.DictReader(file)
            file_keys = reader.fieldnames

        keys = list(dict(self).keys())

        try:
            with open(file_name, "a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=keys)
                if file_keys != keys:
                    writer.writeheader()
                writer.writerow(
                    {
                        "Species": self.species,
                        "Gender": self.gender,
                        "Name": self.name,
                        "Age": self.age,
                    }
                )
        finally:
            if silent == True:
                pass
            else:
                print("Write successful.")

    def edit(self, silent: bool = False):

        if silent == False:
            print(self)

        while True:
            match input("Do you want to edit species, gender, name or age?: ").lower():
                case "species":
                    if self.species == "Dog":
                        self.species = "Cat"
                        print("Species changed to Cat.")
                        break
                    elif self.species == "Cat":
                        self.species = "Dog"
                        print("Species changed to Dog.")
                        break
                case "gender":
                    if self.gender == "male":
                        self.gender = "female"
                        print("Gender changed to female.")
                        break
                    elif self.gender == "female":
                        self.gender = "male"
                        print("Gender changed to male.")
                        break
                case "name":
                    self.name = input("What is the new name?: ")
                    break
                case "age":
                    self.age = input("What is the new age?: ")
                    break
                case _:
                    print("Field not found")

        if silent == False:
            print("New description is: ", self)

        return self


def main():
    """Creates a file if one does not exist in the directory"""
    try:
        with open(file_name, "x") as file:
            pass
    except FileExistsError:
        pass

    """If command line arguments are preset execute them, if not prompts user for action, executes selected action"""
    while True:

        if len(sys.argv) == 2:
            match sys.argv[1]:

                case "-r":
                    route = "read"

                case "-s":
                    route = "search"

                case "-w":
                    route = "write"

                case _:
                    sys.exit("Command-line input not recognized")

        else:
            route = input("Read, Search or Write to database?: ").lower()

        match route:
            case "read":
                list = []

                with open(file_name) as file:
                    reader = csv.reader(file)
                    for row in reader:
                        list.append(row)
                if len(list) > 0:
                    print(
                        tabulate(list, headers="firstrow", showindex=False, tablefmt="grid")
                    )
                    break
                else:
                    print("The database is empty")
                    break

            case "search":
                found_patient = search_base(input("Name to search: ").capitalize())
                if (found_patient != None):
                    print(found_patient)

                    type_of_change = input(
                        "Do you want to edit or remove patient? Type 'edit', 'remove' or 'exit'! : ").lower()

                    match type_of_change:

                        case "edit":
                            try:
                                edit_entry(found_patient)
                                break
                            except ValueError as er:
                                print(er)

                        case "remove":
                            remove_entry(found_patient)
                            break
                        case "exit":
                            os.exit("Exiting.")
                        case _:
                            print("Input not recognized. Try again!")
                else:
                    print("No results found")
                    break

            case "write":
                write()
                break

            case "exit":
                sys.exit
                break

            case _:
                print("Invalid choice. Type 'Read', 'Write' or 'Exit'?")
                continue


def write():

    while True:
        try:
            patient = Patient()
            break
        except ValueError as er:
            print(er)
            if input("Do you want to try again? Type 'Y' or 'N'!").lower() == "y":
                continue
            else:
                break

    while True:
        print(patient)
        confirmation = input(
            "Review data. Commit to database? Type 'Y' or 'N'! "
        ).lower()

        if confirmation == "y":
            patient.write()
            break
        elif confirmation == "n":
            patient.edit(silent = True)
        elif input("Exit program?Type 'Y' or 'N'! ").lower() == "y":
            sys.exit
        else:
            continue


def search_base(search_condition):
    found_items: list = []

    try:
        with open(file_name, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row.get("Name")
                if search_condition == name:
                    species = row.get("Species")
                    gender = row.get("Gender")
                    age = row.get("Age")
                    found_items.append(Patient(species, gender, name, age))
                else:
                    continue

    except FileNotFoundError:
        print("File not found:", file_name)
    except Exception as ex:
        print("An error occurred:", ex)

    if len(found_items) == 0:
        return None
    elif len(found_items) == 1:
        print("Search Successful")
        return found_items[0]
    elif len(found_items) > 1:
        return multiple_search_results(found_items)


def multiple_search_results(found_items: list):
    # Handle cases where there are multiple found items from the search function
    numbering: int = 1

    # Create indexing for found results
    for i in found_items:
        print(numbering, "|", i)
        numbering += 1

    while True:
        # Ask user which match is the correct one
        try:
            user_input = int(
                input("Which patient is the one you are looking for? Type the index number: "))
            break
        except ValueError:
            print("Please input an integer")

    user_input = user_input-1
    return (found_items[user_input])

def edit_entry(patient):

    old_patient = Patient(patient.species, patient.gender, patient.name, patient.age)
    new_patient = patient.edit()

    os.rename(file_name, "database_old.csv")
    with open(file_name, "x") as _:
        pass

    try:
        with open("database_old.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                species = row.get("Species")
                gender = row.get("Gender")
                name = row.get("Name")
                age = row.get("Age")
                test_patient = Patient(species, gender, name, age)

                if test_patient == old_patient:

                    try:
                        new_patient.write(silent=True)
                        print("Patient editted")
                    except TypeError:
                        test_patient.write(silent=True)
                        print("An error occured. No changes were made.")

                else:
                    test_patient.write(silent=True)

        os.remove("database_old.csv")

    except FileNotFoundError:
        print("File not found:", file_name)
    except Exception as ex:
        print("An error occurred:", ex)
        os.rename("database_old.csv", file_name)

def remove_entry(patient):
    # Rename database to database_old and create a new database file
    os.rename(file_name, "database_old.csv")
    with open(file_name, "x") as _:
        pass

    try:
        with open("database_old.csv", "r") as file:
            reader = csv.DictReader(file)
            # Copy each patient except the one that is passed in
            for row in reader:
                species = row.get("Species")
                gender = row.get("Gender")
                name = row.get("Name")
                age = row.get("Age")
                test_patient = Patient(species, gender, name, age)

                if test_patient == patient:
                    print("Patient removed")
                    pass

                else:
                    test_patient.write(silent=True)

    except FileNotFoundError:
        print("File not found:", file_name)
    except Exception as ex:
        print("An error occurred:", ex)
    # Remove the old database
    os.remove("database_old.csv")


if __name__ == "__main__":
    main()
