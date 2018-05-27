from state_machine import Device

"""
Unclear:

1) How to designate BOOT UP signal?
"""


# This is the MAIN (grand/event) LOOP.
def main():
    # Instantiate SPOT device. Initial state is "Main".
    spot = Device("SPOT")

    # Create UI object.
    interface = UI()

    # Create both buttons.
    button_pair = ButtonPair()
    button_pair.configuration_1()

    # Draw the Main screen
    interface.drawMainScreen()


    """
    Need a SWITCH CASE statement
    Copy paste the code below into the switch-case
    State machine will adapt automatically
    """

    if button_1.pressed == True: # VIEW is pressed
        spot.trigger("Main->View")
        interface.drawViewScreen() # Main->View
        button_pair.configuration_2()

        if button_1.pressed == True: # CANCEL is pressed
            spot.trigger("Main->View->Cancel")
            interface.drawMainScreen() # Main
            button_pair.configuration_1()
        elif button_2.pressed == True: # SELECT is pressed
            spot.trigger("Main->View->Select")
            interface.drawSelectView() # Main->View->Selected
            button_pair.configuration_3()

            if button_1.pressed == True: # HOME is pressed
                spot.trigger("Main->View->Select->Home")
                interface.drawMainScreen() # Main
                button_pair.configuration_1()
            elif button_2.pressed == True: # GO BACK is pressed
                spot.trigger("Main->View->Select->Go Back")
                interface.drawSelectView() # Main->View->Selected
                button_pair.configuration_3()

    elif button_2.pressed == True: # MARK is pressed
        spot.trigger("Main->Mark")
        interface.drawMarkScreen() # Main->Mark
        button_pair.configuration_4()

        if button_1.pressed == True: # CANCEL is pressed
            spot.trigger("Main->Mark->Cancel")
            interface.drawMainScreen() # Main
            button_pair.configuration_1()
        elif button_2.pressed == True: # MARK is pressed
            spot.trigger("Main->Mark->Mark")
            interface.drawAfterMark() # Mark->Mark->Mark
            button_pair.configuration_5()

            if button_1.pressed == True: # CANCEL is PRESSED
                spot.trigger("Main->Mark->Mark->Cancel")
                interface.drawMarkScreen() # Main->Mark
                button_pair.configuration_4()
            elif button_2.pressed == True: # CONFIRM is pressed
                spot.trigger("Main->Mark->Mark->Confirm")
                interface.drawMainScreen() # Main
                button_pair.configuration_1()


''' Alert Screens ?????? '''
# Need some way of signaling that there is an ALERT
if ALERT_INTEREST == True: # <----- NEED TO CHANGE
    interface.drawAlertInterest() # Alert (Interest)
    button_pair.configuration_6()

    if button_1.pressed == True: # DISMISS is pressed
        spot.trigger("AlertInt->Dismiss")
        interface.drawMainScreen() # Main
        button_pair.configuration_1()
    elif button_2.pressed == True: # VIEW is pressed
        spot.trigger("AlertInt->View")
        interface.drawSelectView() # Main->View->Selected
        button_pair.configuration_3()


if ALERT_DANGER == True: # <----- NEED TO CHANGE
    interface.drawAlertDanger() # Alert (Danger)
    button_pair.configuration_6()

    if button_1.pressed == True: # DISMISS is pressed
        spot.trigger("AlertDan->Dismiss")
        interface.drawMainScreen() # Main
        button_pair.configuration_1()
    elif button_2.pressed == True: # VIEW is pressed
    spot.trigger("AlertDan->View")
        interface.drawSelectView() # Main->View->Selected
        button_pair.configuration_3()


if __name__ == '__main__':
    main()