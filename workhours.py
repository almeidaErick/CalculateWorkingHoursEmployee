#!/usr/bin/env python3
from datetime import datetime
from operator import le
import argparse
import os
import sys
import time

# Using hardcoded hours range and hourly payment, this could be cleaner if stored in a db for example sqlite
weekhours = ["00:00", "09:00", "18:00"]
weekDayPay = [25, 15, 20]
weekendPay = [30, 20, 25]

# Used to get full name of the Day with the initials given
nameDays = {"MO": "Monday", "TU": "Tuesday", "WE": "Wednesday", "TH": "Thursday", "FR": "Friday", "SA": "Saturday", "SU": "Sunday"}

# Set mandatory arguments needed
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", dest="file", help="File that contains information of the times work by one or many Employees", required=True)
args, unknown = parser.parse_known_args()

# Check if file provided exists
isFile = os.path.isfile(args.file)
if (not isFile):
    print("File does not exists")
    sys.exit()

class CalculateHourPayment:
    def __init__(self):
        self.weekDayPayment = weekDayPay
        self.weekendPayment = weekendPay
        self.weekHours = weekhours
        self.totalHoursWorked = 0.0
        self.totalPayment = 0.0

    def __CalcHours(self, dayType, hours):
        # Remove spaces from hours to simplify calculations
        splitHours = hours.replace(" ", "").replace("\n", "").split("-")
        indexFirstTime = 0
        indexSecondTime = 0
        firstTime = datetime.strptime(splitHours[0], "%H:%M")
        secondTime = datetime.strptime(splitHours[1], "%H:%M")
        paymentRange = []

        if(len(splitHours) != 2):
            # More than 2 times were provided, raise an error
            # 10:00-11:00-12:00
            print("Raise error here")

        if (firstTime > secondTime):
            # First time given is later than the second time
            # 11:00-10:00
            print("Incorrect hours provided")

        # We want to know where the first and second time provided lies in which payment range
        for indexRange in range(len(self.weekHours)):
            timeRange = self.weekHours[indexRange]
            if (datetime.strptime(timeRange, "%H:%M") < firstTime):
                indexFirstTime = indexRange
            
            if (datetime.strptime(timeRange, "%H:%M") < secondTime):
                indexSecondTime = indexRange

            if (datetime.strptime(timeRange, "%H:%M") > firstTime and datetime.strptime(timeRange, "%H:%M") > secondTime):
                break

        # Get the payment list depending on the day of the week
        if (dayType == "WEEKDAY"):
            paymentRange = self.weekDayPayment
            
        else:
            paymentRange = self.weekendPayment

        # Calculate the working hours depending on which intervals exist
        if (indexFirstTime == indexSecondTime):
            timeDifference = secondTime - firstTime
            timeDifferenceFloat = timeDifference.seconds / 3600.00
            self.totalPayment += timeDifferenceFloat * paymentRange[indexFirstTime]
            # Add total hours worked
            self.totalHoursWorked += timeDifferenceFloat
        else:
            # Calculate the difference between the first interval with the first time provided
            timeDifferenceFloat = (datetime.strptime(self.weekHours[indexFirstTime + 1], "%H:%M") - firstTime).seconds / 3600
            self.totalPayment += timeDifferenceFloat * paymentRange[indexFirstTime]
            self.totalHoursWorked += timeDifferenceFloat

            # Assuming we have consecutive intervals provided
            # 08:00-12:00 (from 00:00-09:00 and 09:01-18:00)
            if (indexSecondTime - indexFirstTime) == 1:
                timeDifferenceFloat = (secondTime - datetime.strptime(self.weekHours[indexSecondTime], "%H:%M")).seconds / 3600
                self.totalPayment += timeDifferenceFloat * paymentRange[indexSecondTime]

                # Add total hours worked
                self.totalHoursWorked += timeDifferenceFloat
            else:
                # If the range provided is going across more than one time interval, this section will check that case
                for indexBase in range(indexFirstTime, indexSecondTime, 1):
                    # Get the time difference between our time and the next interval after our first time provided
                    timeDifferenceFloatSecond = (secondTime - datetime.strptime(self.weekHours[indexBase + 1], "%H:%M")).seconds / 3600
                    timeDifferenceConsecutive = (datetime.strptime(self.weekHours[indexBase + 1], "%H:%M") - datetime.strptime(self.weekHours[indexBase], "%H:%M")).seconds / 3600
                    
                    # If the difference calculated for our second time is greater than the difference between the next interval after the first time
                    # then we are sure the finish time (second time) is not in this interval 
                    if timeDifferenceFloatSecond > timeDifferenceConsecutive:
                        timeDifferenceFloatSecond = timeDifferenceConsecutive

                    # Calculate the time difference with respect on the current interval being iterated
                    self.totalPayment += timeDifferenceFloatSecond * paymentRange[indexBase + 1]

                    # Add total hours worked
                    self.totalHoursWorked += timeDifferenceFloatSecond

    def AddHoursWorked(self, dayRangeData):
        dayInitials = dayRangeData[0:2]
        if (dayInitials in nameDays):
            if (dayInitials == "SA" or dayInitials == "SU"):
                self.__CalcHours("WEEKEND", dayRangeData[2:])
            else:
                self.__CalcHours("WEEKDAY", dayRangeData[2:])
        else:
            # RAISE ERROR HERE
            print("NO EXISTE")

    def GetTotalPaymentWorked(self):
        return self.totalPayment

    def GetTotalhoursWorked(self):
        return self.totalHoursWorked

class Employee:
    def __init__(self, stringInfo):
        self.splitInfo = stringInfo.replace(" ", "").split("=")
        if (len(self.splitInfo) != 2):
            print ("Add Error Here")
        self.employeeName = self.splitInfo[0]
        self.hoursCalculation = CalculateHourPayment()
        self.ProcessHoursWorked(self.splitInfo[1])
    
    def ProcessHoursWorked(self, hourString):
        for section in self.splitInfo[1].split(","):
            self.hoursCalculation.AddHoursWorked(section)

    def GetEmployeeTotalHours(self):
        return print("The total hours worked by {} are {}".format(self.employeeName, self.hoursCalculation.GetTotalhoursWorked()))

    def GetEmployeeTotalPayment(self):
        return print("The amount to pay {} is: {} USD".format(self.employeeName, self.hoursCalculation.GetTotalPaymentWorked()))

if __name__ == '__main__':
    # print(datetime.strptime("00:03", "%H:%M") - datetime.strptime("00:01", "%H:%M"))
    # new = Employee("RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00")
    with open(args.file) as fp:
        lines = fp.readlines()
        for line in lines:
            newEmployee = Employee(line)
            newEmployee.GetEmployeeTotalPayment()
            newEmployee.GetEmployeeTotalHours()
    