from functions.funct import getCityList, getDistanceBetweenTwoCities, getDistance, savePDCSV
import random
import pandas as pd

numCities = 250

if __name__ == "__main__":
    dataList, cityList = getCityList('Ontario')
    randomCitySample = random.sample(dataList, numCities)

    dataMatrix = [[0 for j in range(len(randomCitySample) + 1)] for i in range(len(randomCitySample) + 1)]
    dataMatrix[0][0] = 'x'

    for i in range(len(randomCitySample)):
        dataMatrix[i + 1][0] = randomCitySample[i].get("city")
        dataMatrix[0][i + 1] = randomCitySample[i].get('city')

    seen = set()
    seenDistance = {}
    for i in range(len(randomCitySample)):
        for j in range(len(randomCitySample)):
            print(i, '-', j)
            city1 = randomCitySample[i]
            city2 = randomCitySample[j]

            t1 = tuple([city1.get('city'), city2.get('city')])
            t2 = tuple([city2.get('city'), city1.get('city')])

            if t1 not in seen and t2 not in seen:
                if city1.get('city') == city2.get('city'):
                    distance = 0
                else:
                    distance = getDistanceBetweenTwoCities(city1, city2)

                seen.add(t1)
                seen.add(t2)

                seenDistance[city1.get('city') + city2.get('city')] = distance
                seenDistance[city2.get('city') + city1.get('city')] = distance

                dataMatrix[i + 1][j + 1] = distance
            else:
                dataMatrix[i + 1][j + 1] = seenDistance[city1.get('city') + city2.get('city')]

    df = pd.DataFrame(dataMatrix)
    print( df )
    savePDCSV( df )