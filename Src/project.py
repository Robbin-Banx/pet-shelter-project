"""
Pet Shelter Registry
=====================

This file is a basic program to keep track of the patients of a pet shelter.
This started as a final project for the CS50P course, led by David A. Malan.
The project was successfully submitted to CS50P on 10.06.2024.
Currently it's developed for research purposes.

Author: Aleksandar Kostadinov
Github: Robbin-Banx

Location: Sofia, Bulgaria
Date: 10.06.2024
Last Modified: 19.12.2024

"""

import sys
import csv
import os
from tabulate import tabulate
from classes import Patient
from configparser import ConfigParser

# Instantiate
config = ConfigParser()

# Construct the path to config.ini
config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Config', 'config.ini')

# Parse existing file
config.read(config_file_path)

# Get database name from config file
database_name = config.get('section a', 'database_name')
database_folder = config.get('section a', 'database_folder')
database = os.path.join(os.path.dirname(os.path.dirname(__file__)), database_folder, database_name)

def main():
    """Creates a file if one does not exist in the directory"""
    try:
        with open(database, "x") as _:
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
                list_from_file = []

                with open(database) as file:
                    reader = csv.reader(file)
                    for row in reader:
                        list_from_file.append(row)
                if len(list_from_file) > 0:
                    print(
                        tabulate(list_from_file, headers="firstrow", showindex=False, tablefmt="grid")
                    )
                    break
                else:
                    print("The database is empty")
                    break

            case "search":
                found_patient = search_base(input("Name to search: ").capitalize())
                if found_patient is not None:
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
                            sys.exit("Exiting.")
                        case _:
                            print("Input not recognized. Try again!")
                else:
                    print("No results found")
                    break

            case "write":
                create_entry()
                break

            case "exit":
                sys.exit()

            case _:
                print("Invalid choice. Type 'Read', 'Write' or 'Exit'?")
                continue


def write_to_database(patient, silent=False):
    with open(database, "r") as file:
        reader = csv.DictReader(file)
        file_keys = reader.fieldnames

    keys = list(dict(patient).keys())

    try:
        with open(database, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=keys)

            if file_keys != keys:
                writer.writeheader()

            writer.writerow(
                {
                    'Species': patient.species,
                    'Gender': patient.gender,
                    'Name': patient.name,
                    'Age': patient.age
                }
            )
    finally:
        if silent:
            pass
        else:
            print("Write successful.")


def create_entry(patient=None, silent=False):
    if patient == None:
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
        if not patient:
            break
        if silent == True:
            write_to_database(patient, silent=True)
            break
        print(patient)
        confirmation = input(
            "Review data. Commit to database? Type 'Y' or 'N'! "
        ).lower()

        if confirmation == "y":
            write_to_database(patient)
            break
        elif confirmation == "n":
            patient.edit(silent = True)
        elif input("Exit program?Type 'Y' or 'N'! ").lower() == "y":
            sys.exit()
        else:
            continue


def search_base(search_condition):
    found_items: list = []

    try:
        with open(database, "r") as file:
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
        print("File not found:", database)
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
        print(f'{numbering}, "|", {i}')
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
    return found_items[user_input]

def edit_entry(patient):

    old_patient = Patient(patient.species, patient.gender, patient.name, patient.age)
    new_patient = patient.edit()

    os.rename(database, "database_old.csv")
    with open(database, "x") as _:
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
                        create_entry(new_patient, silent=True)
                        print("Patient editted.")
                    except TypeError:
                        create_entry(test_patient, silent=True)
                        print("An error occured. No changes were made.")

                else:
                    create_entry(test_patient, silent=True)

        os.remove("database_old.csv")

    except FileNotFoundError:
        print("File not found:", database)
    except Exception as ex:
        print("An error occurred:", ex)
        os.rename("database_old.csv", database)


def remove_entry(patient, silent=False):
    # Rename database to database_old and create a new database file
    os.rename(database, "database_old.csv")
    with open(database, "x") as _:
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
                    if silent == False:
                        print("Patient removed")
                    pass

                else:
                    write_to_database(test_patient, silent=True)

    except FileNotFoundError:
        print("File not found:", database)
    except Exception as ex:
        print("An error occurred:", ex)
    # Remove the old database
    os.remove("database_old.csv")


if __name__ == "__main__":
    main()
