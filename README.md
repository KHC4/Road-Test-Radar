-----------------------------------------------------------------------------------
PREREQUISITES

1. Google Chrome and Python are added to PATH
2. Python winsound, selenium, tkinter, and calendar libraries installed
3. Requires the latest version of chromedriver (update as needed)

-----------------------------------------------------------------------------------
FIRST TIME SETUP
1. Use the email button to set the default email to be used (mandatory)
2. Use the select student button to select the student you are trying to book a test for
3. To add a student, use the select student button and then "add student" then fill in the information
4. To remove a student, use the select student button then "remove student" then select the student you want to remove from the drop down menu
5. Select the test centers you want to monitor using the "Select Test Centers" button


INSTRUCTIONS
1. Run start_chrome.bat and go to the login page of the drivetest website
2. Run start_RTR.bat
3. When on the login page, click the login button on the application to automatically input the students information. If an error occurs at any point, then finish the process manually. Make sure that the "open on saturdays" box is checked
4. Use the "Select Dates" button to choose specific dates to monitor of the given test centers
5. Use the check dates button to auotmatically cycle through the selected locations and check if any of the selected dates are available an alarm will sound once a date is found, and a shutdown sound will occur if the program crashes during this proccess
6. If a date is found, a popup will appear asking if you would like to ignore the specific date (ie if the time doesnt work out for you), then program will only sound the alarm if a new time slot appears of the same date and otherwise ignore.


-----------------------------------------------------------------------------------
IMPORTANT NOTE

This program only works with windows machines.

Using this program may result in a ban from the drivetest.ca, use it at your own risk
