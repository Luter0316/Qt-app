class painter:
    def __init__(self, index, name, yearsOfLife, style, country, link, paintCount):
        self.__index = index
        self.name = name
        self.yearsOfLife = yearsOfLife
        self.style = style
        self.country = country
        self.link = link
        self.paintCount = paintCount

    def getIndex(self):
        return self.__index

    def getName(self):
        return self.name

    def getYearsOfLife(self):
        return self.yearsOfLife

    def getStyle(self):
        return self.style

    def getCountry(self):
        return self.country

    def getLink(self):
        return self.link

    def getPaintCount(self):
        return self.paintCount

    def getAge(self):
        time = self.getYearsOfLife().strip().split('-')
        bornDate = time[0].strip()
        deathDate = time[1].strip()
        return str(int(deathDate) - int(bornDate))


def createListOfPainters():
    listOfPainters = []
    countryLst = []
    styleLst = []
    timeLst = []
    with open("data_painter.txt", 'r', encoding="utf-8") as file:
        lines = len(file.readlines())
        file.seek(0)
        for i in range(0, lines, 7):
            listOfPainters.append(
                painter(file.readline(), file.readline(), file.readline(), file.readline(), file.readline(),
                        file.readline(), file.readline()))

            country = listOfPainters[-1].getCountry().strip().split(',')
            for c in country:
                if not (c in countryLst):
                    countryLst.append(c)

            style = listOfPainters[-1].getStyle().strip().split(',')
            for s in style:
                if not (s in styleLst):
                    styleLst.append(s)

            time = listOfPainters[-1].getYearsOfLife().strip().split('-')
            bornDate = time[0].strip()
            deathDate = time[1].strip()
            if not ((int(bornDate) - 1) // 100 + 1) in timeLst:
                timeLst.append((int(bornDate) - 1) // 100 + 1)
            if not ((int(deathDate) - 1) // 100 + 1) in timeLst:
                timeLst.append((int(deathDate) - 1) // 100 + 1)

        timeLst.sort()
        timeLst = list(map(str, timeLst))

    return [listOfPainters, countryLst, timeLst, styleLst]
