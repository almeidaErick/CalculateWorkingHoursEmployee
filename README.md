Employee Hour and Payment Calculation

We have the following information for hourly payment depending on each day of the week

Monday - Friday

00:01 - 09:00 25 USD

09:01 - 18:00 15 USD

18:01 - 00:00 20 USD

Saturday and Sunday

00:01 - 09:00 30 USD

09:01 - 18:00 20 USD

18:01 - 00:00 25 USD

We also have the abbreviations for each day, to simplify the input line of the input text file

MO: Monday

TU: Tuesday

WE: Wednesday

TH: Thursday

FR: Friday

SA: Saturday

SU: Sunday

We need to calculate how much an employee earns every day. I considered the following scenarios

1.- The format of each line in the input file is expected to be like this
"RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00"
If the name of the Employee is not separated by the character "=" from the hours and days, the program will rise an error (not implemented yet, instead, a message will be shown in the console).

2.- Only 2 times are allowed to each day (START TIME and END TIME), in this case, the program is not considering different time ranges on the same day.

3.- Start and End time of a period or work belongs to the same hourly rate
3.1.- In this case, I didn't need to do much logic in the process of getting the total hours, since this can be calculated by the difference of the "END TIME" and "START TIME". 

4.- A user can work many hours every day that belongs to different payment ranges, for example, a user can work from 8am to 7pm on TUESDAY for example, and the logic to calculate this is:
4.1.- 1 hour for (25 USD each hour), 9 hours for (15 USD each hour), and 1 hour for (20 USD each hour).
4.2.- Total hours: 11 hours
4.3.- Total payment: 180 USD

5.- A user cannot end a working day before the START TIME, for example
5.1.- a User starts working on MONDAY at 8am, and finishes working at 7am on MONDAY (same day), this will result in an error for the input data (not implemented yet), for now, it is showing a message in the console.

6.- A file is mandatory and needs to be provided in the console (full path of the file), an example of this is:
python c:/.../Projects/PythonHoursCalculation/workhours.py -f c:/.../Projects/PythonHoursCalculation/employeesExampleHours.txt

DESIGN

2 classes were considered

Employee
* Separates the name of the Employee from the hours specified on each line in the text file.
* Call the method AddHoursWorked in CalculateHourPayment to add the hours worked to the total for this specific Employee.
* Get the total Hours and Payment for this user to display in the console

CalculateHourPayment
* Separate the input by ",", to calculate the hours of each day.
* Calculate the payment for each hour specified depending on which payment range this hour belongs.
* Separate hourly payment depending on the day of the week, "WEEK ENDS - SATURDAY AND SUNDAY" and "WEEK DAY - FROM MONDAY TO FRIDAY".
* Converts the time in string to a more friendly format so we can calculate the time difference between 2 periods, and the accuracy of this difference is in minutes.
* Returns the total hours worked by an Employee
* Returns the total payment for an Employee.

STILL IN PROGRESS
* Completing unittest file, due to time constraints.
* Give a nicer format to README.
* Give a better explanation on each variable used in the code, in the meantime, a comment was added on each line where there is a calculation to explain how I am doing the calculation.

CONTACT
Any feedback, please write me to my personal email: almeida.ericks29@gmail.com
I'll be completing the unittest if I am given more time, thank you.

