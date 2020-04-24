#!/usr/bin/env python3
import sys


class Completed(Exception):
    pass


class CorruptedMaze(Exception):
    pass


class Maze:
    directionsValues = {
        "UP": (0, 1),
        "Down": (0, -1),
        "Right": (1, 0),
        "Left": (-1, 0)
    }

    def __init__(self):
        self.file = sys.argv[1]
        self.maze = self.setMaze()
        self.frontier = []
        self.search = True
        self.path = []
        self.A = self.starPoint()
        self.usedFrontier = []
        self.maxsteps = self.maxStepsinMaze()

    def setMaze(self):
        with open(self.file, "r") as f:
            f = f.readlines()
            for i in range(len(f)):
                f[i] = f[i].replace("\n", "")
        return f

    def starPoint(self):
        for x in range(len(self.maze)):
            for y in range(x):
                if self.maze[x][y] == "A":
                    return [x, y]

    def seeAround(self, point):
        got = []
        indexes = []
        for i in list(self.directionsValues.values()):
            i = list(i)
            i[0] = point[0] + i[0]
            i[1] = point[1] + i[1]
            try:
                got.append(self.maze[i[0]][i[1]])
                indexes.append(i)
            except IndexError:
                got.append("out")
                indexes.append(i)
                pass
        return got, indexes

    @staticmethod
    def add_EndPoint(views_, indexes, path):
        for i in range(len(views_)):
            if views_[i] == "B":
                path.append(indexes[i])

    def start_digging(self, point, func):
        self.path.append(point)
        aroundPoint, indexes = self.seeAround(point)

        localPath = []
        try:
            if point != localPath[-1]:
                localPath.append(point)
        except IndexError:
            pass

        if aroundPoint.count("B") == 1:
            self.add_EndPoint(aroundPoint, indexes, self.path)
            raise Completed

        if aroundPoint.count(" ") == 3:
            if point not in self.frontier and point not in self.usedFrontier:
                self.frontier.append(point)
        elif aroundPoint.count(" ") > 3:
            if point not in self.frontier and point not in self.usedFrontier:
                num = aroundPoint.count(" ") - 2
                for i in range(num):
                    self.frontier.append(point)

        if aroundPoint.count(" ") == 1:
            return

        return func(point)

    def maxStepsinMaze(self):
        counter = 0
        for line in self.maze:
            for _ in line:
                counter += 1
        sys.setrecursionlimit(counter)
        return counter

    def drawPath(self):
        get_draw = self.maze
        print("Throw path : ", self.path)
        print("\nExplored", len(self.path))
        # Uncomment (below lines) to print the original Map
        # print("Maze: ")
        # for i in get_draw:
        #     print(i)
        for i in range(len(get_draw)):
            get_draw[i] = list(get_draw[i])
            for y in range(len(get_draw[i])):
                if [i, y] in self.path[1:-1]:
                    get_draw[i][y] = "^"
            get_draw[i] = "".join(get_draw[i])

        print("\n\nMazeSolution:")
        for i in get_draw:
            print(i)


class SearchInDepth(Maze):
    def __init__(self):
        super().__init__()
        self.path.append(self.A)
        self.steps = 0
        self.searchInDepth()

    def searchInDepth(self):
        try:
            while self.steps <= self.maxsteps:
                if len(self.frontier) == 0:
                    try:
                        self.EvaluateNextPoint(self.path[-1])
                    except IndexError:
                        self.EvaluateNextPoint(self.A)

                else:
                    last_point = self.frontier.pop()
                    self.usedFrontier.append(last_point)
                    self.EvaluateNextPoint(last_point)
                self.steps += 1
            raise CorruptedMaze
        except Completed:
            print("Search In Depth solution .. ")
            pass

    def EvaluateNextPoint(self, point):
        newPoint = [0, 0]
        go = False
        for direct, val in self.directionsValues.items():
            newPoint[0] = point[0] + val[0]
            newPoint[1] = point[1] + val[1]
            try:
                x = self.maze[newPoint[0]][newPoint[1]]
                if x == " " and newPoint not in self.path and newPoint[0] >= 0 and newPoint[1] >= 0:
                    go = True
                    break
            except IndexError:
                pass
        if go:
            point = newPoint
            self.start_digging(point, self.EvaluateNextPoint)
        else:
            return


class SearchInBreadth(Maze):
    def __init__(self):
        super().__init__()
        self.swapPath = []
        self.path.append(self.A)
        self.steps=0
        self.searchInBreadth_()

    def searchInBreadth_(self):
        try:
            while self.steps <= self.maxsteps:
                try:
                    self.EvaluatePoints(self.path)
                except RecursionError:
                    self.steps = self.maxsteps + 1
                self.steps += 1
            raise CorruptedMaze
        except Completed:
            print("Search In Breadth solution .. ")
            self.path = self.swapPath[1:]
            pass

    def EvaluatePoints(self, points_):
        points = self.path
        self.swapPath += points_
        self.path = []
        self.start_digging(points, self.EvaluatePoints)

    def start_digging(self, points, func):
        for point in points:
            aroundPoint, indexes = self.seeAround(point)

            if aroundPoint.count("B") == 1:
                self.swapPath.append(point)
                self.add_EndPoint(aroundPoint, indexes, self.swapPath)
                raise Completed
            for i in range(len(aroundPoint)):
                if aroundPoint[i] == " ":
                    if not indexes[i] in self.path and not indexes[i] in self.swapPath:
                        self.path.append(indexes[i])

        return func(points)


if len(sys.argv) == 1:
    name_maze = input("Enter Name Of Maze File : ")
    sys.argv.append(name_maze)
try:
    SearchInDepth().drawPath()
    SearchInBreadth().drawPath()
except CorruptedMaze:
    print("Corrupted Maze")
