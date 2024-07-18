
# Pet Shelter Registry

*Author: Aleksandar Kostadinov

*Github: Robbin-Banx

*Location: Sofia, Bulgaria

*Date: 10.06.2024

## Table of Contents

- [Description](#description)
- [Usage](#usage)
- [Operation](#operation)
- [Components](#components)

#### Description:
The project's main goal is to help create a registry for a pet shelter.
To achieve this the program creates a CSV file named "database.csv" if one does not exist in the directory already. The name of the database can be changed on line 7 before starting the program.

##### Interactive Mode
Upon starting the program the user is prompted for input. The user can:
* Type "read" to read the database, which will output a table of the contents of the csv file in a table formatting.
* Type "search" to search the database and if a match is found the user can edit or remove the database entry by typing "edit" or "remove". This will not change the order of the other entries.
* Type "write" to add a new patient to the database.
* The user can also exit the program by typing "Exit".
* These inputs are not case sensitive.

##### Command-line mode:
* "patient.py -r" to read the database, which will output a table of the contents of the csv file in a table formatting.
* "patient.py -s" to search the database and if a match is found the user can edit or remove the database entry by typing "edit" or "remove". This will not change the order of the other entries.
* "patient.py -w" to add a new patient to the database.

#### Operation
The program operates by creating a patient object using the Patient class which contains the species, gender, name and age of the pet. Then depending on the context the object can write to the database or edit the class instance by user prompts.

#### Patient Class

The `Patient` class is used to represent the pets in the shelter. Each instance of the `Patient` class includes attributes for the species, gender, name, and age of the pet. The class provides methods for:

- Initializing a patient with given or prompted values.
- Generating a string description of the patient.
- Iterating over the patient's attributes to return them as a dictionary.
- Comparing two patient objects for equality based on their attributes.
- Writing the patient's data to a CSV file.
- Editing the patient's attributes interactively.

 **Attributes:** `species`, `gender`, `name`, `age`
 **Methods:**
    - `__str__`: Returns a description of the pet.
    - `__iter__`: Returns a dictionary where the keys are `"species"`, `"gender"`, `"name"`, and `"age"`, and the values are the corresponding strings or integers.
    - `__eq__`: Supports comparison of different instances.

#### Creating Objects

- **Interactive Mode:** Call the `Patient()` function. The user is prompted to input the necessary data for creating the object.
- **Search Mode:** When a search of the CSV is conducted and a result is found, the search function creates an object by calling `Patient("species", "gender", "name", "age")` and returns the created object.

#### Main Function

The `main` function manages the primary workflow of the program. It ensures that the CSV file exists and handles user inputs through both command-line arguments and interactive prompts. The function supports reading the database, searching for and modifying entries, and adding new patients to the database.

#### Write Function

The `write` function creates a new `Patient` instance and prompts the user to review the data. If confirmed, the patient data is written to the database. It provides an option to exit the program or retry the process.

#### Search Base Function

The `search_base` function searches the database for a patient by name. It returns the matching patient object if found, allowing further actions like editing or removal. The function handles cases with no results, single results, or multiple results.

#### Multiple Search Results Function

The `multiple_search_results` function is only called by the `search_base` function in scenarios where multiple patients match the search criteria. It prompts the user to select the correct patient from the list of found items and returns the chosen patient object for further actions.

#### Edit Entry Function

The `edit_entry` function allows editing of an existing patient's details. It renames the current database file and creates a new one while preserving all other entries. The function updates the database with the edited patient information or reverts to the original if editing fails.

#### Remove Entry Function

The `remove_entry` function removes a specified patient from the database. It renames the current database file and creates a new one, excluding the removed patient's data. The function ensures the remaining data and order preserved in the new database file.
