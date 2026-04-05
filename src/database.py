from sys import argv


# CREATE
def creating_table(second, creating_table_data, database):
    table_name = second

    try:
        if table_name in database:            # Check if the table already exists
            print("###################### CREATE #########################")
            print(f"Table '{table_name}' already exists.")
            print("#######################################################")
            print()

        elif table_name not in database:
            database[table_name] = {}        # Initialize table structure

            database[table_name]["columns"] = creating_table_data.split(",")  # change to form of it str to list

            print("###################### CREATE #########################")
            print("Table '{}' created with columns: {}".format(table_name, creating_table_data.split(",")))
            print("#######################################################")
            print()  # space for other functions


    except Exception:
        print("###################### CREATE #########################")
        print("invalid input for commands")
        print("#######################################################")
        print()
    return database


# INSERT
def inserting_table(second, inserting_table_data, database):
    inserting_table_name = second
    try:

        if "rows" not in database[inserting_table_name]:  # does not reset the rows if it exists
            database[inserting_table_name]["rows"] = []  # data's form is str in list

        user_input_list = []  # list of input
        user_input_list.extend(inserting_table_data.split(","))  # change the form list to str

        if len(database[inserting_table_name]["columns"]) != len(
                user_input_list):  # fills with space if the entered value is less
            difference = len(database[inserting_table_name]["columns"]) - len(user_input_list)
            for i in range(difference):
                user_input_list.append(" ")

        new_row = dict(zip(database[inserting_table_name]["columns"], user_input_list))  # making dict with columns and input
        database[inserting_table_name]["rows"].append(new_row)  # transfer to rows

        print("###################### INSERT #########################")
        print("Inserted into '{}': {}".format(inserting_table_name, tuple(inserting_table_data.split(","))))
        print()
        print(f"Table: {inserting_table_name}")

        print_table_new(inserting_table_name, database)

        print("#######################################################")
        print()

        return database

    except KeyError:
        print("###################### INSERT #########################")
        print("Table {} not found".format(inserting_table_name))
        print("Inserted into '{}': {}".format(inserting_table_name, tuple(inserting_table_data.split(","))))
        print("#######################################################")
        print()
        return database

    except Exception:
        print("###################### INSERT #########################")
        print("invalid input for commands")
        print("#######################################################")
        print()


# SELECT                                                                                 /id,name,age {'major': 'CS', 'age': '21'}
def select(second, select_data, database):  # select_data = <columns> <conditions> / id,name {"major": "CS"}
    selecting_table_name = second

    missing_columns = []     # Track missing columns for error handling
    desired_rows = []
    try:

        conditions_4print = select_data.split()[1:]
        conditions_4print = " ".join(conditions_4print)  # form of str {'major': 'CS', 'age': '21'}
        conditions_4print = conditions_4print.replace('"', "'")  # specify with " ' "

        list_of_select_data = select_data.split()

        if not list_of_select_data[0] == "*":           # control of "*"
            desired_rows = str(list_of_select_data[0])  # desired_rows is a list
            desired_rows = desired_rows.split(",")      # listed the desired columns one by one / ['id', 'name', 'age']

        if list_of_select_data[0] == "*":               # " * " means take all everything
            desired_rows = database[selecting_table_name]["columns"].copy()

        # Validate column existence
        for column in desired_rows:
            if column not in database[selecting_table_name]["columns"]:
                missing_columns.append(column)

        if not missing_columns == []:
            raise ValueError        # error for missing columns



        list_of_conditions = []    # all the operations below are for this / ['CS', '21']
        list_of_columns = []       # all the operations below are for this / ['major', 'age']
        conditions = list_of_select_data[1:]
        conditions = " ".join(conditions)
        conditions = conditions.split(",")
        for condition in conditions:
            key_value = condition.split(":")
            condition = key_value[1]
            column = key_value[0]
            condition = condition.strip()
            column = column.strip()
            condition = condition.strip(' " \' {}')
            column = column.strip(' " \' {}')

            list_of_conditions.append(condition)
            list_of_columns.append(column)

        # Check for missing columns in conditions
        for column in list_of_columns:
            if column not in database[selecting_table_name]["columns"]:
                missing_columns.append(column)

        if not missing_columns == []:
            raise ValueError

        # Filter rows based on conditions
        ok4_conditions = []  # list of those who meet the requirement
        for user_data in database[selecting_table_name]["rows"]:
            if set(list_of_conditions).issubset(set(user_data.values())):  # checking to see if there are all conditions
                ok4_conditions.append(user_data)

        # Collect selected data
        selected_things = []
        for things in ok4_conditions:  # we look for users who meet the requirements
            temp_list = []
            for key, value in things.items():  # we list the desired conditions
                if key in desired_rows:
                    temp_list.append(value)
            if len(temp_list) != 0:
                selected_things.append(tuple(temp_list))  # desired format tuple

        print("###################### SELECT #########################")
        print(f"Condition: {conditions_4print}")
        print("Select result from '{}': {}".format(selecting_table_name, selected_things))
        print("#######################################################")
        print()

    except KeyError:
        print("###################### SELECT #########################")
        print(f"Table {selecting_table_name} not found")
        print(f"Condition: {conditions_4print}")
        print("Select result from '{}': {}".format(selecting_table_name, "None"))
        print("#######################################################")
        print()

    except ValueError:
        if len(missing_columns) > 1:
            missing_columns = ",".join(missing_columns)
        else:
            missing_columns = missing_columns[0]

        print("###################### SELECT #########################")
        print(f"Column {missing_columns} does not exist")
        print(f"Condition: {conditions_4print}")
        print("Select result from '{}': {}".format(selecting_table_name, "None"))
        print("#######################################################")
        print()

    except Exception:
        print("###################### SELECT #########################")
        print("invalid input for commands")
        print("#######################################################")
        print()

    return database


# UPDATE
def update(second, update_data,database):  # update_data string   update_data = UPDATE students {"major": "SE"}  {"name": "John Doe"}
    updating_table_name = second

    dict_of_conditions = {}     # Conditions for selecting rows to update
    dict_of_updates = {}        # Updates to apply
    missing_columns = []        # Tracks missing columns for error reporting

    try:
        # Parse the update data to separate updates and conditions
        update_data = update_data.split()  # multiple spaces turned into a single spaces
        update_data = " ".join(update_data)

        # Extract and format updates and conditions
        update_data = update_data.split()
        updates_conditions = " ".join(update_data)                             # string {"major": "SE"}  {"name": "John Doe"}
        updates_conditions = updates_conditions.replace("{", "}")  # }"major": "SE"}  }"name": "John Doe"}
        updates_conditions = updates_conditions.split("}")                     # ['', '"major": "SE"', ' ', '"name": "John Doe"', '']

        clear_updates_conditions = []  # ['"major": "SE"', '"name": "John Doe"']
        for i in updates_conditions:
            if not i.strip() == "":
                clear_updates_conditions.append(i)

        updates = clear_updates_conditions[0]  # "major": "SE"
        dictform_of_updates = "{" + updates + "}"
        dict_of_updates = eval(dictform_of_updates)  # dict  / {'major': 'SE'}

        conditions = clear_updates_conditions[1]  # "name": "John Doe"
        dictform_of_conditions = "{" + conditions + "}"
        dict_of_conditions = eval(dictform_of_conditions)  # dict  /  {'name': 'John Doe'}

        # Validate if columns in updates or conditions exist in the table
        missing_columns = []
        for key in dict_of_updates.keys():
            if key not in database[updating_table_name]["columns"]:
                missing_columns.append(key)

        for key in dict_of_conditions.keys():
            if key not in database[updating_table_name]["columns"]:
                missing_columns.append(key)

        if not missing_columns == []: # Raise error if any columns are missing
            raise ValueError

        updating_rows = 0  # for writing

        for data_dictionary in database[updating_table_name]["rows"]:
            matching = 0  # for controlling
            for key, value in dict_of_conditions.items():

                if key in data_dictionary and str(data_dictionary[key]) == str(
                        value):  # it is str in rows then we changed for true compression
                    matching += 1
                    updating_rows += 1

            if matching == len(dict_of_conditions):  # replace if the number of matches is the same
                data_dictionary.update(dict_of_updates)

        print("###################### UPDATE #########################")
        print(f"Updated '{updating_table_name}' with {dict_of_updates} where {dict_of_conditions}")
        print(f"{updating_rows} rows updated.")
        print()
        print(f"Table: {updating_table_name}")

        print_table_new(updating_table_name, database)
        print("#######################################################")
        print()

    except KeyError:
        print("###################### UPDATE #########################")
        print(f"Updated '{updating_table_name}' with {dict_of_updates} where {dict_of_conditions}")
        print(f"Table {updating_table_name} not found")
        print("0 rows updated.")

        print("#######################################################")
        print()

    except ValueError:
        missing_columns = ",".join(missing_columns)

        print("###################### UPDATE #########################")
        print(f"Updated '{updating_table_name}' with {dict_of_updates} where {dict_of_conditions}")
        print(f"Column {missing_columns} does not exist")
        print("0 rows updated.")
        print()
        print(f"Table: {updating_table_name}")

        print_table_new(updating_table_name, database)
        print("#######################################################")
        print()

    except Exception:
        print("###################### UPDATE #########################")
        print("invalid input for commands")
        print("#######################################################")
        print()

    return database


# DELETE
def delete(second, deleting_data, database):  # {"age": 30, "name": Alan}
    deleting_table_name = second
    missing_columns = []    # Tracks missing columns for error reporting
    try:
        # If no conditions are provided, delete all rows
        if deleting_data == None:
            deleted_things = database[deleting_table_name]["rows"].copy()
            conditions_4print = ""

            database[deleting_table_name]["rows"].clear()

        else:
            conditions_4print = deleting_data.replace('"', "'")  # specify  with " ' "

            list_of_conditions = []  # all the operations below are for this   ['30', 'Alan']
            list_of_columns = []  # all the operations below are for this   ['age', 'name']

            conditions = deleting_data.split(",")
            for condition in conditions:
                key_value = condition.split(":")
                condition = key_value[1]
                column = key_value[0]
                condition = condition.strip()
                column = column.strip()
                condition = condition.strip(' " \' {}')
                column = column.strip(' " \' {}')

                list_of_conditions.append(condition)
                list_of_columns.append(column)


            for column in list_of_columns:
                if column not in database[deleting_table_name]["columns"]:
                    missing_columns.append(column)

            if not missing_columns == []:
                raise ValueError

            deleted_things = []  # list of deleted
            for user_data in database[deleting_table_name]["rows"]:  # checking to see if there are all conditions
                if set(list_of_conditions).issubset(set(user_data.values())):
                    deleted_things.append(user_data)
                    database[deleting_table_name]["rows"].remove(user_data)

        print("###################### DELETE #########################")
        print(f"Deleted from '{deleting_table_name}' where {conditions_4print}")
        print(f"{len(deleted_things)} rows deleted.")
        print()
        print(f"Table: {deleting_table_name}")

        print_table_new(deleting_table_name, database)
        print("#######################################################")
        print()

    except KeyError:
        conditions_4print = deleting_data.replace('"', "'")  # specify  with " ' "

        print("###################### DELETE #########################")
        print(f"Deleted from '{deleting_table_name}' where {conditions_4print}")
        print(f"Table {deleting_table_name} not found")
        print("0 rows deleted.")
        print("#######################################################")
        print()

    except ValueError:
        conditions_4print = deleting_data.replace('"', "'")  # specify  with " ' "
        missing_columns = ",".join(missing_columns)

        print("###################### DELETE #########################")
        print(f"Deleted from '{deleting_table_name}' where {conditions_4print}")
        print(f"Column {missing_columns} does not exist")
        print("0 rows deleted.")
        print()
        print(f"Table: {deleting_table_name}")

        print_table_new(deleting_table_name, database)
        print("#######################################################")
        print()

    except Exception:
        print("###################### DELETE #########################")
        print("invalid input for commands")
        print("#######################################################")
        print()

    return database


# JOIN
def join(table_1, table_2, column, database):
    try:
        if column not in database[table_1]["columns"]:
            raise ValueError

        # get columns
        table1_columns = database[table_1]["columns"]
        table2_columns = database[table_2]["columns"]

        # create common columns
        common_colum = []
        common_colum.extend(table1_columns)
        common_colum.extend(table2_columns)

        # get rows
        table1_rows = database[table_1]["rows"]
        table2_rows = database[table_2]["rows"]

        # list of things to print
        ok4_printing = []

        # adds to the list if the column requested from us is the same
        for rows_1 in table1_rows:

            for rows_2 in table2_rows:
                if rows_1[column] == rows_2[column]:
                    temp_list = []
                    temp_list.extend(list(rows_1.values()))
                    temp_list.extend(list(rows_2.values()))
                    ok4_printing.append(temp_list)

        print("####################### JOIN ##########################")
        print(f"Joın tables {table_1} and {table_2}")
        print(f"Join result ({len(ok4_printing)} rows):")
        print()
        print("Table: Joined Table")
        print_table4_join(common_colum, ok4_printing)
        print("#######################################################")
        print()

    except KeyError:
        a = [table_1, table_2]
        not_exist_table = []
        for table in a:
            if table not in database:
                not_exist_table.append(table)
        not_exist_table = ",".join(not_exist_table)

        print("####################### JOIN ##########################")
        print(f"Joın tables {table_1} and {table_2}")
        print(f"Table {not_exist_table} does not exist")
        print("#######################################################")
        print()

    except ValueError:
        print("####################### JOIN ##########################")
        print(f"Joın tables {table_1} and {table_2}")
        print(f"Column {column} does not exist")
        print("#######################################################")
        print()

    except Exception:
        print("###################### JOIN #########################")
        print("invalid input for commands")
        print("#######################################################")
        print()


# COUNT
def count(second, counting_data, database):  # COUNT students WHERE {"name": "Alan", "age": "20"}
    counting_table_name = second
    missing_columns = []
    counting_things = []
    try:
        # controlling the " * "
        if counting_data == "*":
            counting_things = database[counting_table_name]["rows"].copy()

        if not counting_data == "*":
            counting_things = []

            list_of_conditions = []  # all the operations below are for this ['20', 'Alan']
            list_of_columns = []  # all the operations below are for this ['age', 'name']

            conditions = counting_data.split(",")
            for condition in conditions:
                key_value = condition.split(":")
                condition = key_value[1]
                column = key_value[0]
                condition = condition.strip()
                column = column.strip()
                condition = condition.strip(' " \' {}')
                column = column.strip(' " \' {}')

                list_of_columns.append(column)
                list_of_conditions.append(condition)


            for column in list_of_columns:
                if column not in database[counting_table_name]["columns"]:
                    missing_columns.append(column)

            if not missing_columns == []:
                raise ValueError

            for user_data in database[counting_table_name]["rows"]:  # checking to see if there are all conditions
                if set(list_of_conditions).issubset(set(user_data.values())):
                    counting_things.append(user_data)

        print("###################### COUNT #########################")
        print(f"Count: {len(counting_things)}")
        print(f"Total number of entries in '{counting_table_name}' is {len(counting_things)}")
        print("#######################################################")
        print()

    except KeyError:
        print("###################### COUNT #########################")
        print(f"Table {counting_table_name} not found")
        print(f"Total number of entries in '{counting_table_name}' is 0")
        print("#######################################################")
        print()

    except ValueError:
        missing_columns = ",".join(missing_columns)
        print("###################### COUNT #########################")
        print(f"Column {missing_columns} does not exist")
        print(f"Total number of entries in '{counting_table_name}' is 0")
        print("#######################################################")
        print()

    except Exception as e:
        print("###################### COUNT #########################")
        print("invalid input for commands")
        print("#######################################################")
        print()

    return database


def main():
    database = {}
    with open(argv[1], "r") as f_in:
        inputs = f_in.readlines()

        for line in inputs:
            line = line.strip()
            if line == "":
                continue

            user_input = line.split()  # change the input for first and second
            first = user_input[0]
            second = user_input[1]

            if first == "CREATE_TABLE":
                new_data = " ".join(user_input[2:])  # form of str
                creating_table(second, new_data, database)

            elif first == "INSERT":
                new_data = " ".join(user_input[2:])  # form of str
                inserting_table(second, new_data, database)

            elif first == "SELECT":

                select_where = user_input.pop(3)
                select_data = " ".join(user_input[2:])  # form of str
                select(second, select_data, database)

            elif first == "UPDATE":

                update_data = " ".join(user_input[2:])
                update_data = update_data.replace("WHERE", "")  # {'major': 'SE'}  {'name': 'John Doe'}
                update(second, update_data, database)

            elif first == "DELETE":

                if len(user_input) <= 3:
                    delete(second, None, database)

                else:
                    delete_data = " ".join(user_input[3:])  # string {"age": "30", "name": "Alan"}
                    delete(second, delete_data, database)

            elif first == "JOIN":
                column = user_input[3]
                tables = second.split(",")
                table_1, table_2 = tables[0], tables[1]

                join(table_1, table_2, column, database)

            elif first == "COUNT":

                counting_data = " ".join(user_input[3:])  # string {"age": "30", "name": "Alan"}
                count(second, counting_data, database)


# table printing except JOIN
def print_table_new(table_name, database):
    rows_copy = database[table_name]["rows"].copy()
    columns_copy = database[table_name]["columns"].copy()

    length_of_table = []

    for column in columns_copy:
        column_length_list = [column]  # we saved each title as a list

        for row in rows_copy:
            if column in row:
                column_length_list.append(row[column])  # we have also listed the value for that title

        length_of_table.append(column_length_list)

    for i in range(len(length_of_table)):  # we chose the longest one
        the_longest = max(length_of_table[i], key=len)  # by the number of titles and made that list only that one
        length_of_table[i] = [the_longest]

    max_lengths = []

    for columns in length_of_table:  # we took the length of what was chosen as the longest
        for i in columns:
            maximum = len(i)
            max_lengths.append(maximum)

    # writing "+" and "-" for table
    def plus_mines():
        for i in range(len(max_lengths)):
            if i == len(max_lengths) - 1:
                print("+" + "-" * (max_lengths[i] + 2) + "+")
            else:
                print("+" + "-" * (max_lengths[i] + 2), end="")

    # writing title
    def title():
        for i in range(len(columns_copy)):
            value = columns_copy[i]
            print(f"| {value:<{max_lengths[i]}} ", end="")
        print("|")

    # writing value
    def writing_value():
        for row in rows_copy:
            for i in range(len(columns_copy)):
                if i != len(columns_copy) - 1:
                    value = row.get(columns_copy[i])
                    print(f"| {str(value):<{max_lengths[i]}} ", end="")

                if i == len(columns_copy) - 1:
                    value = row.get(columns_copy[i])
                    print(f"| {str(value):<{max_lengths[i]}} |")

    plus_mines()
    title()
    plus_mines()
    writing_value()
    plus_mines()


# table printing for JOIN
def print_table4_join(common_colum, ok4_printing):
    columns_copy = common_colum
    rows_copy = ok4_printing

    length_of_table = []

    for column_index, column in enumerate(columns_copy):

        column_length_list = [column]  # we saved each title as a list

        for row in rows_copy:
            column_length_list.append(row[column_index])  # we have also listed the value for that title

        length_of_table.append(column_length_list)

    for i in range(len(length_of_table)):  # we chose the longest one
        the_longest = max(length_of_table[i], key=len)  # by the number of titles and made that list only that one
        length_of_table[i] = [the_longest]

    max_lengths = []

    for longest in length_of_table:  # we took the length of what was chosen as the longest
        maximum = len(longest[0])
        max_lengths.append(maximum)

    # writing "+" and "-" for table
    def plus_mines():
        for i in range(len(max_lengths)):
            if i == len(max_lengths) - 1:
                print("+" + "-" * (max_lengths[i] + 2) + "+")
            else:
                print("+" + "-" * (max_lengths[i] + 2), end="")

    # writing title for table
    def title():
        for i in range(len(columns_copy)):
            value = columns_copy[i]
            print(f"| {value:<{max_lengths[i]}} ", end="")
        print("|")

    # writing value for table
    def writing_value():
        for row_index, row in enumerate(rows_copy):
            for i in range(len(columns_copy)):
                if i != len(columns_copy) - 1:
                    value = row[i]
                    print(f"| {str(value):<{max_lengths[i]}} ", end="")
                if i == len(columns_copy) - 1:
                    value = row[i]
                    print(f"| {str(value):<{max_lengths[i]}} |")

    plus_mines()
    title()
    plus_mines()
    writing_value()
    plus_mines()


if __name__ == '__main__':
    main()

