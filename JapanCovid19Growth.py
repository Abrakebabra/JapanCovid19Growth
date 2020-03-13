
# to make daily scraper for
# covid19japan.com
#xpath
#/html/body/section[1]/div[5]/div[2] for total cases


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium

import time
import threading


def scraper():
    options = selenium.webdriver.FirefoxOptions()
    driver = selenium.webdriver.Firefox(executable_path=
        r'/Users/keithlee/Documents/Python/Selenium/geckodriver')
    
    driver.get('https://covid19japan.com')

    while True:
        try:
            findCases = driver.find_element_by_xpath('/html/body/section[1]/div[5]/div[2]')
            casesToday = findCases.text
            
            if casesToday:
                driver.close()
                return int(casesToday)
        except selenium.common.exceptions.NoSuchElementException:
            continue
    

def averageFromIndex(days: int, dataSource: list, startIndex: int):
    endIndex = startIndex + days
    total = 0
    
    for i in range(startIndex, endIndex):
        total += dataSource[i]
    
    average = round(total / days)
    return int(average)


def rollingAvgOf(days: int, dataSource: list):
    rollingAverage = []
    dataCount = len(dataSource)

    for i in range(0, dataCount - days + 1):
        average = averageFromIndex(days, dataSource, i)
        rollingAverage.append(average)

    return list(rollingAverage)


def growthRates(dataSource: list):
    growthRateList = []

    for i in range(1, len(dataSource)):
        growth = round(dataSource[i] / dataSource[i - 1], 2)
        growthRateList.append(growth)

    return list(growthRateList)


# Not used
def getAverage(sourceList: list, rounding: int):
    count = len(sourceList)
    total = 0

    for i in sourceList:
        total += i

    average = round(total / count, rounding)
    return average
# Not used


def predict(rollingAverage: list, growthRate, smoothedBy: int, daysOut: int):
    currentFromSmoothed = int(smoothedBy / 2) # rounded down
    compoundGrowth = pow(growthRate, currentFromSmoothed + daysOut)

    prediction = round(rollingAverage[-1] * compoundGrowth)
    return prediction


def displaySmoothedData(dataSource: list, smoothedBy: int):
    if smoothedBy % 2 == 0:
        print("Smooth by an odd number")
        return
    
    rollingAverage: list = rollingAvgOf(days = smoothedBy, dataSource = dataSource)
    smoothedGrowthRates: list = growthRates(rollingAverage)
    oneDayPrediction = predict(rollingAverage, smoothedGrowthRates[-1], smoothedBy, 1)
    twoDayPrediction = predict(rollingAverage, smoothedGrowthRates[-1], smoothedBy, 2)

    print(f"\nConfirmed Cases:\n{confirmedCases}\n\n")
    print(f"{smoothedBy} Day Rolling Average:\n{rollingAverage}\n\n")
    print(f"{smoothedBy} Day Growth Rates:\n{smoothedGrowthRates}\n\n")
    print('--------------------------------------------------')
    print(f"Rolling {smoothedBy} Day Growth: {smoothedGrowthRates[-1]}")
    print(f"One Day Prediction: {oneDayPrediction}")
    print(f"Two Day Prediction: {twoDayPrediction}")
    print('--------------------------------------------------')


# starting Feb 16 as daily reports from that date
# to save to text file and read from it

confirmedCases = [52, 64, 74, 84, 92, 107, 133, 147, 159, 171, 189, 214, 231,
                  240, 257, 276, 289, 329, 342, 396, 463, 499, 518, 575, 627,
                  677]

todaysNewCase = scraper()
confirmedCases.append(todaysNewCase)

displaySmoothedData(dataSource = confirmedCases, smoothedBy = 5)

