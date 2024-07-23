from datetime import datetime  # datetime module allows us to work with date and time
import random  # random module allows us to generate item from a list
import os  # os module provides functions for interacting with the operating system

# START SCREEN
#
today = datetime.now().date()  # Display the current time in the appropriate format
start_active = 1  # Maintains starting screen
start_func = ""  # Determines the user start selection
dis_hold = ""  # Display holder, allows for reading time
omit_list = []  # Used to omit unnecessary data in a list
time = []  # Time from cancel function

# ADD RESERVATION VARIABLES
#
# Add Reservation Screen Maintenance
rsv_date = 0  # Maintains display
rsv_name = 0  # Maintains display
rsv_add_pax = 0  # Maintains display
rsv_session = 0  # Maintains display
rsv_mail = 0  # Maintains display
rsv_number = 0  # Maintains display

# Add Reservation Data
rsv_list = []  # Stores all reservation data into a list
rsv_format_list = ""  # List formatting to be pasted into the txt file

# Reservation Data
slot_1 = 0  # Stores quantity in Slot 1
slot_2 = 0  # Stores quantity in Slot 2
slot_3 = 0  # Stores quantity in Slot 3
slot_4 = 0  # Stores quantity in Slot 4

# CANCEL RESERVATION VARIABLES
#
# Cancel Reservation Values
can_date = 0  # Maintains display
can_name = 0  # Maintains display
can_user_date = ""  # User written Date
can_user_name = ""  # User written Name
can_new_list = []  # Updates the list after cancelling
can_format_list = ""  # Formats the list to be printed
can_name_check = 0  # Checks for an existing valid name on the list
can_display = ""  # Used to display the cancelled reservation

# UPDATE RESERVATION VARIABLES
#
# Update Reservation Values
upd_choice = 0  # Maintains display
upd_date = 0  # Maintains display
upd_name = 0  # Maintains display
upd_name_check = 0  # Checks for an existing valid name on the list
upd_reservation = []  # Updates the list after updating the reservation
upd_format_list = ""  # Formats the list to be printed


# EXCEPTION CASES
#
# Types of error
class SlotError(Exception):
    pass  # Informs the user with an explanation for error


# STORED FUNCTIONS
#
# Clears screen
def clear():
    os.system('cls')


# Requests user date
def def_user_date():
    user_date = input("\n============================================\n"
                      "                  Booking date"
                      "\n============================================\n"
                      "Enter the requested date (YYYY-MM-DD): ")  # User enters the date for the reservation
    req_date = datetime.strptime(user_date, "%Y-%m-%d").date()  # Formats the date user entered into appropriate format
    date_diff = req_date - today  # Calculate the difference between the date that user entered and the current date

    try:
        with open("reservation_22002620.txt", "r") as file:
            data_list = file.readlines()

            for reservation in data_list:
                data = reservation.strip().split(" | ")

                if data[0] == user_date:
                    omit_list.append(reservation)

            slot_counts = {
                "Slot_1": 0,
                "Slot_2": 0,
                "Slot_3": 0,
                "Slot_4": 0
            }

            for reservation in omit_list:
                data = reservation.strip().split(" | ")
                slots = data[1]

                if slots in slot_counts:
                    slot_counts[slots] += 1

    except Exception as e:
        print(f"\n ## {e} ##\n")

    if date_diff.days <= 4:
        raise ValueError

    if all(slot_no > 7 for slot_no in [slot_1, slot_2, slot_3, slot_4]):
        raise SlotError()

    return user_date


# Requests user session
def def_user_session():
    user_session = int(input("\n============================================\n"
                             "                  Sessions"
                             "\n============================================\n"
                             "1. 12:00 pm — 2:00 pm\n"
                             "2. 2:00 pm — 4:00 pm\n"
                             "3. 6:00 pm — 8:00 pm\n"
                             "4. 8:00 pm — 10:00 pm\n"
                             "============================================\n"
                             "Type a number corresponding to the function: "))

    slot_counts = {
        1: slot_1,
        2: slot_2,
        3: slot_3,
        4: slot_4
    }
    # Checks if the entered user session is valid
    if user_session not in slot_counts:
        raise ValueError

    # Checks if the session entered by the user has exceeded its limit
    # If user session is more than 8 by the time of input than an error is raised
    if slot_counts[user_session] >= 8:
        raise ValueError
    user_formatted_session = f"Slot {user_session}"
    return user_formatted_session


# Requests user name
def def_user_name():
    user_name = input("\n============================================\n"
                      "                Reservation Name"
                      "\n============================================\n"
                      "May i know who is this table under: ")
    user_name = user_name.upper()  # Converts the string entered by the user to uppercase
    return user_name


# Requests user mail
def def_user_mail():
    user_mail = input("\n============================================\n"
                      "                Reservation Email"
                      "\n============================================\n"
                      "Please type in your mail for contact: ")

    # Ensure that the mail entered by the user is in the appropriate format
    if "@" not in user_mail:
        raise ValueError
    user, domain = user_mail.split("@")

    if not user:
        raise ValueError

    if "." not in domain:
        raise ValueError
    user_mail = user_mail.lower()
    return user_mail


# Requests user phone
def def_user_phone():
    user_phone = input("\n============================================\n"
                       "               Reservation number"
                       "\n============================================\n"
                       "Enter your number without spaces for contact: ")

    # Ensure that the user's phone number has the correct amount of numbers
    if len(user_phone) != 10:
        raise ValueError

    # Ensure that all the values input by the user is in digits
    for char in user_phone:
        if not char.isdigit():
            raise ValueError
    return user_phone


# Request user pax
def def_user_pax():
    user_pax = int(input("\n============================================\n"
                         "               Reservation seats"
                         "\n============================================\n"
                         "How many seats will there be in the table: "))

    # To not allow for more than 4 people per table
    if user_pax > 4:
        raise ValueError
    return user_pax


# Main menuItems_22002620.txt Screen, returns to this page on every end till specified.
while start_active == 1:
    try:
        rsv_list = []
        print("\nToday's date is", today)  # Display the current date

        start_func = int(input("============================================\n"
                               "    Welcome to Charming Thyme Trattoria!\n"
                               "============================================\n"
                               " 1. Add a reservation\n"
                               " 2. Cancel a reservation\n"
                               " 3. Update a reservation\n"
                               " 4. Display all reservations\n"
                               " 5. Generate a meal recommendation\n"
                               " 6. Exit\n"
                               "============================================\n"
                               "Type a number corresponding to the function: "))

    # If value input by user does not correspond to the functions return an error
    except ValueError:
        print("\n## Invalid input, please try again! ##\n")

    # Function 1, Add a reservation
    # Enters the reservation display
    if start_func == 1:
        rsv_date = 1
        clear()

        # Requests user date
        # Appends the user date into the reservation list
        while rsv_date == 1:
            try:
                # Carry out the def_user_date() function
                # Append the user's date into rsv_list
                # Moves onto display that would request for user's session
                rsv_list.append((def_user_date()))
                clear()
                rsv_date = 0
                rsv_session = 1

            # Will not append if reservation date is not 5 days in advance
            # Will not append if reservation on that date is full
            except ValueError as e:
                clear()
                print("\n## The reservation has to be 5 days in advance! ##\n")
            except SlotError as e:
                clear()
                print("\n## The selected date has no available slots! ##\n")

        # Requests user session in a given list and compares with amount
        while rsv_session == 1:
            try:
                # Carry out the def_user_session() function
                # Append the user's session into rsv_list
                # Moves onto display that would request for user's name
                rsv_list.append(def_user_session())
                clear()
                rsv_session = 0
                rsv_name = 1

            # Will not append if slot is invalid
            except ValueError:
                clear()
                print("\n## The slot you tried is unavailable! ##\n")
            except Exception as e:
                clear()
                print(f"\n## {e} ##\n")

        # Requests user name
        while rsv_name == 1:
            try:
                # Carry out the def_user_name() function
                # Append the user's name into rsv_list
                # Moves onto display that would request for user's email address
                rsv_list.append(f"{def_user_name()}")
                clear()
                rsv_mail = 1
                rsv_name = 0

            # Will not append if user's name is invalid
            except Exception as e:
                clear()
                print(f"\n ## {e} ##\n")

        # Requests user mail
        while rsv_mail == 1:
            try:
                # Carry out the def_user_mail() function
                # Append the user's email address into rsv_list
                # Moves onto display that would request for user's phone number
                rsv_list.append(f"{def_user_mail()}")
                clear()
                rsv_number = 1
                rsv_mail = 0

            # Will not append if user's email address is invalid
            except ValueError:
                clear()
                print("\n ## Invalid email address! Please try again! ##\n")
            except Exception as e:
                clear()
                print(f"\n## {e} ##\n")

        # Requests user phone number
        while rsv_number == 1:
            try:
                # Carry out the def_user_phone() function
                # Append the user's phone number into rsv_list
                # Moves onto display that would request for user's number of seats
                rsv_list.append(f"{def_user_phone()}")
                clear()
                rsv_add_pax = 1
                rsv_number = 0

            # Will not append if user's phone number is invalid
            except ValueError as e:
                clear()
                print("\n ## Invalid phone number! Please try again! ##\n")
            except Exception as e:
                clear()
                print(f"\n## {e} ##\n")

        # Requests user pax
        while rsv_add_pax == 1:
            try:
                # Carry out the def_user_pax() function
                # Append the user's number of seats into rsv_list
                rsv_list.append(f"{def_user_pax()}")
                clear()
                rsv_add_pax = 0

            # Will not append if user's number of seat is invalid
            except ValueError:
                clear()
                print("\n## The reservation cannot exceed 4 members! ##\n")
            except Exception as e:
                clear()
                print(f"\n ## {e} ##\n")

        # Converts the list into string format
        # Paste the string into the textfile
        if rsv_add_pax == 0:
            rsv_format_list = " | ".join(rsv_list)
            with open("reservation_22002620.txt", "a") as file:
                file.write(f"{rsv_format_list}\n")

        clear()
        # Display the user's reservation
        # Returns to display that asks user to input their needed function
        dis_hold = input(f"\n============================================\n"
                         f"               Your Reservation                 "
                         f"\n============================================\n"
                         f"{rsv_format_list}"
                         f"\n============================================\n"
                         f"Have you finished reading? Type anything to exit! [ANY]: ")
        clear()
        start_func = 0

    # Function 2, Cancels a reservation
    elif start_func == 2:
        can_date = 1
        # Opens and reads the reservation textfile
        # Reads the textfile as list
        with open("reservation_22002620.txt", "r") as file:
            can_list = file.readlines()
        can_format_list = "".join(can_list)  # Display list as string
        # Displays this message if there are no reservations
        if can_list == "":
            clear()
            dis_hold = input("\n============================================\n"
                             "          No Reservations on List!"
                             "\n============================================\n"
                             "Have you finished reading? Type anything to exit! [ANY]: ")
            clear()
            can_date = 0

        clear()
        while can_date == 1:
            try:
                print(f"\n============================================\n"
                      f"                Reservation date"
                      f"\n============================================\n"
                      f"{can_format_list}"
                      f"============================================\n")
                can_user_date = input(
                    "What was your reservation date? [YYYY-MM-DD]:")  # Asks for user's reservation date
                datetime.strptime(can_user_date,
                                  "%Y-%m-%d").date()  # Formats the user's date into the appropriate format

                # Goes through each line in can_list
                # Split each line with " | "
                for reservation in can_list:
                    data = reservation.strip().split(" | ")

                    # Checks to see if user's date matches data
                    # If yes, then the reservation is appended to omit.list
                    # Move onto the next display
                    if data[0] == can_user_date:
                        omit_list.append(reservation)
                        can_format_list = "".join(omit_list)  # Display list as string
                can_date = 0

            # Display this message if user's date is invalid
            except ValueError:
                clear()
                print("\n## Incorrect date format, please try again! ##\n")

            # Display this message if there are no reservations on the date user entered
            if can_format_list == "":
                clear()
                dis_hold = input("\n============================================\n"
                                 "          No Reservations on Day!"
                                 "\n============================================\n"
                                 "Have you finished reading? Type anything to exit! [ANY]: ")
                clear()
                # Return to previous display that asks for user's date
                can_date = 1
            else:
                # Moves onto next display that asks for user's name
                can_name = 1

            clear()
            while can_name == 1:
                try:
                    # Display all active reservations that are available on the date that has been input
                    print(f"\n============================================\n"
                          f"            Active Reservations on Day"
                          f"\n============================================\n"
                          f"{can_format_list}"
                          f"============================================")
                    can_user_name = input("Which is your reservation? [NAME]: ")  # Asks for user's name
                    can_user_name = can_user_name.upper()  # Format the user's input name into uppercase

                    # Goes through each line in omit_list
                    # Split each line with " | "
                    for reservation in omit_list:
                        data = reservation.strip().split(" | ")

                        # Checks if user's name matches with data
                        # If yes can_name_check = 1
                        if data[2] == can_user_name:
                            can_name_check = 1
                    can_name = 0

                    # Raises an error if user's name does not match
                    # Display this message
                    if can_name_check != 1:
                        raise ValueError
                except ValueError:
                    print("\n## Name not present, please try again! ##\n")

            # Remove the user's reservation from can_list
            for reservation in can_list:
                data = reservation.strip().split(" | ")
                if data[0] == can_user_date and data[2] == can_user_name:
                    can_display = reservation
                    can_list.remove(reservation)

            # Write the current reservation list into the textfile
            # Overwriting the old textfile with new reservations
            with open("reservation_22002620.txt", "w") as file:
                for reservation in can_list:
                    file.write(str(reservation))

            # Display this message once reservation has been successfully canceled
            # Display all the current active reservations
            if can_date == 0 and can_name == 0:
                clear()
                dis_hold = input(f"\n============================================\n"
                                 f"                Cancelled Reservation"
                                 f"\n============================================\n"
                                 f"{can_display}"
                                 f"============================================\n"
                                 f"Done reading? Type anything to exit [ANY]: ")
                clear()

    # Function 3, Updates a reservation
    elif start_func == 3:
        upd_date = 1
        # Opens and reads the reservation textfile
        # Reads the textfile as list
        with open("reservation_22002620.txt", "r") as file:
            upd_list = file.readlines()

        upd_format_list = "".join(upd_list)  # Display list as string
        # Display this message if there are no reservations
        if upd_list == "":
            clear()
            dis_hold = input("\n============================================\n"
                             "          No Reservations on List!"
                             "\n============================================\n"
                             "Have you finished reading? Type anything to exit! [ANY]: ")
            clear()
            upd_date = 0

        clear()
        while upd_date == 1:
            try:
                print(f"\n============================================\n"
                      f"                Reservation date"
                      f"\n============================================\n"
                      f"{upd_format_list}"
                      f"============================================\n")
                upd_user_date = input(
                    "What was your reservation date? [YYYY-MM-DD]:")  # Ask for user's reservation date
                datetime.strptime(upd_user_date,
                                  "%Y-%m-%d").date()  # Formats the user's input date into appropriate format

                # Goes through each line in upd_list
                # Split each line with " | "
                for reservation in upd_list:
                    data = reservation.strip().split(" | ")

                    # Checks if user's date matches with data
                    # If yes, reservations are appended to omit_list
                    # Moves onto next display
                    if data[0] == upd_user_date:
                        omit_list.append(reservation)
                        upd_format_list = "".join(omit_list)  # Display list as string
                upd_date = 0

            # Display this error message if user's date is invalid
            except ValueError:
                clear()
                print("\n## Incorrect date format, please try again! ##\n")

            # Display message if there are no reservations
            if upd_format_list == "":
                clear()
                dis_hold = input("\n============================================\n"
                                 "          No Reservations on Day!"
                                 "\n============================================\n"
                                 "Have you finished reading? Type anything to exit! [ANY]: ")
                clear()
                # Return to previous display that asks for user's date
                upd_date = 1
            else:
                # Moves onto next display that asks for user's name
                upd_name = 1

            clear()
            while upd_name == 1:
                try:
                    # Display all active reservations on date that user entered
                    # Ask for user's name
                    print(f"\n============================================\n"
                          f"            Active Reservations on Day"
                          f"\n============================================\n"
                          f"{upd_format_list}"
                          f"============================================")
                    upd_user_name = input("Which is your reservation? [NAME]: ")
                    upd_user_name = upd_user_name.upper()  # Format user's input name into uppercase

                    # Goes through each line in upd_list
                    # Split each line with " | "
                    for reservation in omit_list:
                        data = reservation.strip().split(" | ")

                        # Check if user's name matches with data
                        # If yes, upd_name_check = 1
                        if data[2] == upd_user_name:
                            upd_name_check = 1

                    # If user's name does not match, raise an error
                    if upd_name_check != 1:
                        raise ValueError

                    # Moves onto next display that ask for user's update choice
                    upd_choice = 1
                    upd_name = 0

                # Display this message if user's name is invalid
                except ValueError:
                    clear()
                    print("\n## Name not present, please try again! ##\n")

            # Checks if user's date and name matches
            # If yes, remove the previous reservation
            for reservation in upd_list:
                data = reservation.strip().split(" | ")
                if data[0] == upd_user_date and data[2] == upd_user_name:
                    upd_reservation = data
                    upd_list.remove(reservation)

            # Write the current reservation list into the textfile
            # Overwriting the old textfile with new reservations
            with open("reservation_22002620.txt", "w") as file:
                for reservation in upd_list:
                    file.writelines(reservation)

            clear()
            while upd_choice == 1:
                # Display this message that contains all the choices that users can choose
                # Ask for user's update choice
                upd_decision = int(input(f"\n============================================\n"
                                         f"           Change Reservation Details"
                                         f"\n============================================\n"
                                         f"{upd_reservation}"
                                         f"\n============================================\n"
                                         f"1. Reservation Date\n"
                                         f"2. Reservation Slot\n"
                                         f"3. Reservation Name\n"
                                         f"4. Email\n"
                                         f"5. Phone Number\n"
                                         f"6. Pax\n"
                                         f"7. Save and Exit"
                                         f"\n============================================\n"
                                         f"What would you like to do? [NUMBER]: "))


                # Match user's update decision
                match upd_decision:
                    # Update user's reservation date
                    case 1:
                        upd_change_date = 1
                        while upd_change_date == 1:
                            try:
                                # Carry out the def_user_date function
                                # Replace old reservation date with new date
                                # Move onto next display that shows updated reservation
                                upd_reservation[0] = str(def_user_date())
                                clear()
                                upd_change_date = 0
                            # Display error message if updated reservation date is not 5 days away from current date
                            # Display error message if number of reservation in new date has reached its limit
                            except ValueError as e:
                                clear()
                                print("\n## The reservation has to be 5 days in advance! ##\n")
                            except SlotError as e:
                                clear()
                                print("\n## The selected date has no available slots! ##\n")
                            upd_choice = 0
                    # Update user's session
                    case 2:
                        upd_change_session = 1
                        while upd_change_session == 1:
                            try:
                                # Carry out the def_user_session function
                                # Replace old session with new session
                                # Move onto next display that shows updated reservation
                                upd_reservation[1] = str((def_user_session()))
                                clear()
                                upd_change_session = 0
                            # Display error message if new session is invalid
                            except ValueError:
                                clear()
                                print("\n## The slot you tried is unavailable! ##\n")
                            except Exception as e:
                                clear()
                                print(f"\n## {e} ##\n")
                    # Update user's name
                    case 3:
                        upd_change_name = 1
                        while upd_change_name == 1:
                            try:
                                # Carry out the def_user_name function
                                # Replace old name with new name
                                # Move onto next display that shows updated reservation
                                upd_reservation[2] = str(def_user_name())
                                clear()
                                upd_change_name = 0
                            # Display error message if user's new name is invalid
                            except Exception as e:
                                clear()
                                print(f"\n ## {e} ##\n")
                    # Update user's email address
                    case 4:
                        upd_change_mail = 1
                        while upd_change_mail == 1:
                            try:
                                # Carry out the def_user_mail function
                                # Replace old email address with new email address
                                # Move onto next display that shows updated reservation
                                upd_reservation[3] = str(def_user_mail())
                                clear()
                                upd_change_mail = 0
                            # Display error message if user's new email address is invalid
                            except ValueError:
                                clear()
                                print("\n ## Invalid email address! Please try again! ##\n")
                            except Exception as e:
                                clear()
                                print(f"\n## {e} ##\n")
                    # Update user's phone number
                    case 5:
                        upd_change_phone = 1
                        while upd_change_phone == 1:
                            try:
                                # Carry out the def_user_phone function
                                # Replace old phone number with new phone number
                                # Move onto next display that shows updated reservation
                                upd_reservation[4] = str(def_user_phone())
                                clear()
                                upd_change_phone = 0
                            # Display error message if user's new phone number is invalid
                            except ValueError as e:
                                clear()
                                print("\n ## Invalid phone number! Please try again! ##\n")
                            except Exception as e:
                                clear()
                                print(f"\n## {e} ##\n")
                    # Update user's number of seats
                    case 6:
                        upd_change_pax = 1
                        while upd_change_pax == 1:
                            try:
                                # Carry out the def_user_pax function
                                # Replace old number of seats with new number of seats
                                # Move onto next display that shows updated reservation
                                upd_reservation[5] = str(def_user_pax())
                                clear()
                                upd_change_pax = 0
                            # Display error message if user's new number of seats exceed 4 or is invalid
                            except ValueError:
                                clear()
                                print("\n## The reservation cannot exceed 4 members! ##\n")
                            except Exception as e:
                                clear()
                                print(f"\n ## {e} ##\n")
                    case 7:
                        # Display updated list as string
                        upd_format_list = " | ".join(upd_reservation)
                        with open("reservation_22002620.txt", "a") as file:
                            file.write(f"{upd_format_list}\n")
                        upd_choice = 0
                    # Display this error message if user's choice does not match with any of the options
                    case _:
                        clear()
                        print("\n## Invalid Input! Please try again! ##\n")

                # Display message along with updated list
                if upd_date == 0 and upd_name == 0:
                    clear()
                    dis_hold = input(f"\n============================================\n"
                                     f"          Your Updated Reservation"
                                     f"\n============================================\n"
                                     f"{upd_reservation}"
                                     f"\n============================================\n"
                                     f"Have you finished reading? Type anything to exit! [ANY]: ")
                    clear()

    # Function 4, Displays all active reservation
    elif start_func == 4:
        try:
            # Opens the reservation textfile and read it
            with open("reservation_22002620.txt", "r") as file:
                data_list = file.read()

            # Checks if list is empty
            # If not empty, display this message along with all active reservations
            if data_list != "":
                clear()
                dis_hold = input(f"\n============================================\n"
                                 f"            Active Reservations"
                                 f"\n============================================\n"
                                 f"{data_list}"
                                 f"============================================\n"
                                 f"Have you finished reading? Type anything to exit! [ANY]: ")
                clear()

            # If list is empty, display this message
            else:
                clear()
                dis_hold = input("\n============================================\n"
                                 "          No Reservations on List!"
                                 "\n============================================\n"
                                 "Have you finished reading? Type anything to exit! [ANY]: ")
                clear()

        except Exception as e:
            clear()
            print(f"\n## {e} ##\n")

    # Function 5, Generate a Meal recommendation
    elif start_func == 5:
        try:
            # Opens the menu textfile and reads it
            # Calculate the number of items in menu and display it as menu_len
            # Moves onto next display that shows menu item
            with open("menuItems_22002620.txt", "r") as menu:
                menu_data = menu.read()
            menu_form = menu_data.split('\n')
            menu_len = len(menu_form)
            menu_rec_active = 1

            # Generate a random item from the menu
            while menu_rec_active == 1:
                clear()
                # Generate a random integer between zero and the number of items in menu minus by one
                # Display this message with a random menu item
                # Ask if the user would like another recommendation
                menu_rec = random.randint(0, menu_len - 1)
                menu_decision = input(f"\n============================================\n"
                                      f"How about trying {menu_form[menu_rec]} for today?"
                                      f"\n============================================\n"
                                      f"Would you like another recommendation [Y/N]:")
                menu_decision = menu_decision.lower()  # Formats the user's decision into lowercase

                # Match the user's menu decision
                match menu_decision:
                    # Generate another menu item
                    # Ask if user would like another recommendation
                    case "y":
                        menu_rec_active = 1
                    # Stop generating a menu item
                    # Return to main display
                    case _:
                        clear()
                        menu_rec_active = 0
        # Display error message if user's menu decision is invalid
        except Exception as e:
            clear()
            print(f"\n## {e} ##\n")

    # Function 6, Exits the program
    elif start_func == 6:
        clear()
        dis_hold = input("Thank you, and have a nice day! :D"
                         "Type anything to exit! [ANY]: ")
        start_active = 0

    else:
        clear()
        print("\n## Invalid input, please try again! ##\n")
