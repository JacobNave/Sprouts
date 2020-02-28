import tkinter as tk
import math

graph = {(150, 250): [], (350, 250): []}

master = tk.Tk()

canvas = tk.Canvas(master, width = 500, height = 500)
canvas.configure(background = "black")
canvas.pack()

firstPoint = None 
secondPoint = None
thirdPoint = None
coefficient = 0
constant = 0
paintedPoint = None 
arc = None 
showTemp = False

def dist(point1, point2):
    	return math.sqrt(math.pow(point2[0] - point1[0], 2) + math.pow(point2[1] - point1[1], 2))

def getThirdPoint(xPos, yPos):
	global thirdPoint
	if coefficient == "y":
		midPoint = ((secondPoint[0] + firstPoint[0])/2, (secondPoint[1] + firstPoint[1])/2)
		thirdPoint = (midPoint[0], yPos)
	elif coefficient == "x":
		midPoint = ((secondPoint[0] + firstPoint[0])/2, (secondPoint[1] + firstPoint[1])/2)
		thirdPoint = (xPos, midPoint[1])
	else:
		thirdPoint = (xPos, coefficient * xPos + constant)

def getLine():
	global coefficient
	if (secondPoint[1] - firstPoint[1]) == 0:
		coefficient = "y"
	elif(secondPoint[0] - firstPoint[0]) == 0:
		coefficient = "x"
	else:
		coefficient = 1/((secondPoint[1] - firstPoint[1])/(secondPoint[0] - firstPoint[0]))
		midPoint = ((secondPoint[0] + firstPoint[0])/2, (secondPoint[1] + firstPoint[1])/2)
		constant = midPoint[1] - coefficient*midPoint[0]

def getCenter():
	if firstPoint != None and secondPoint != None and thirdPoint != None:
		m1 = (thirdPoint[1] - firstPoint[1])/(thirdPoint[0] - firstPoint[0])
		m2 = (secondPoint[1] - thirdPoint[1])/(secondPoint[0] - thirdPoint[0])

		if m1 == m2:
			return None

		x = (m1*m2*(firstPoint[1] - secondPoint[1]) + m2*(firstPoint[0] + thirdPoint[0]) - m1*(thirdPoint[0] + secondPoint[0]))/(2*(m2 - m1))
		y = (-1/m1)*(x - (firstPoint[0] + thirdPoint[0])/2) + (firstPoint[1] + thirdPoint[1])/2

		return (x,y)

def drawPoints():
	for point in graph:
		x1, y1 = (point[0] - 3), (point[1] - 3)
		x2, y2 = (point[0] + 3), (point[1] + 3)
		canvas.create_oval(x1, y1, x2, y2, fill= "white")

def drawTargetPoints():
	for point in graph: 
		if len(graph[point]) < 3 and point != firstPoint:
			x1, y1 = (point[0] - 3), (point[1] - 3)
			x2, y2 = (point[0] + 3), (point[1] + 3)
			canvas.create_oval(x1, y1, x2, y2, fill= "red")
		elif point == firstPoint:
			x1, y1 = (point[0] - 3), (point[1] - 3)
			x2, y2 = (point[0] + 3), (point[1] + 3)
			canvas.create_oval(x1, y1, x2, y2, fill= "green")

def minLines(point1, point2):
	if len(graph[point1]) > len(graph[point2]):
		return len(graph[point2])
	else:
		return len(graph[point1])

def drawTemp():
	global paintedPoint 
	global arc
	if thirdPoint != None:
		x1, y1 = (thirdPoint[0] - 3), (thirdPoint[1] - 3)
		x2, y2 = (thirdPoint[0] + 3), (thirdPoint[1] + 3)
		paintedPoint = canvas.create_oval(x1, y1, x2, y2, fill= "green")

		center = getCenter()

		
		#line should be straight
		if center == None:
			midPoint = ((secondPoint[0] + firstPoint[0])/2, (secondPoint[1] + firstPoint[1])/2)
			x1, y1 = (midPoint[0] - 3), (midPoint[1] - 3)
			x2, y2 = (midPoint[0] + 3), (midPoint[1] + 3)
			paintedPoint = canvas.create_oval(x1, y1, x2, y2, fill= "blue")
			arc = canvas.create_line(firstPoint[0], firstPoint[1], secondPoint[0], secondPoint[1], fill = "white")
		#should be arc
		else:
			x1, y1 = (center[0] - 3), (center[1] - 3)
			x2, y2 = (center[0] + 3), (center[1] + 3)
			paintedPoint = canvas.create_oval(x1, y1, x2, y2, fill= "blue")

			radius = abs(dist(center, thirdPoint))
			startAngle = math.atan2(firstPoint[1] - center[1], firstPoint[0] - center[0])
			endAngle = math.atan2(secondPoint[1] - center[1], secondPoint[0] - center[0])
			startAngle = (startAngle*180) / math.pi
			endAngle = (endAngle*180) / math.pi

			print("start: " + str(startAngle) + "\nend: " + str(endAngle))

			arc = canvas.create_arc(center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius, start = startAngle, extent = 180 - endAngle, outline = "white")

def deleteTemp():
	global paintedPoint
	global arc
	if arc != None:
		canvas.delete(arc)
	if paintedPoint != None:
		canvas.delete(paintedPoint)
	
def selectPoint(event):
	global firstPoint
	global secondPoint
	global graph
	global showTemp

	def nearestPoint(x, y):
		for point in graph:
			if abs(point[0] - x) < 7 and abs(point[1] - y) < 7 and len(graph[point]) < 3:
				return point
		return None

	if firstPoint == None:
		firstPoint = nearestPoint(event.x, event.y)
		if firstPoint == None:
			return
		drawTargetPoints()
	elif secondPoint == None: 
		if nearestPoint(event.x, event.y) == None:
			firstPoint = None
			drawPoints()
			return
		if nearestPoint(event.x, event.y) == firstPoint:
			return
		secondPoint = nearestPoint(event.x, event.y)
		drawPoints()
		
		showTemp = True
		getLine()
		thirdPoint = getThirdPoint(event.x, event.y)
		drawTemp()

def mouseMove(event):
	if showTemp:
		deleteTemp()
		if firstPoint != None and secondPoint != None:
			getLine()
			thirdPoint = getThirdPoint(event.x, event.y)
			drawTemp()

drawPoints()

canvas.bind("<Button-1>", selectPoint)
canvas.bind("<Motion>", mouseMove)
tk.mainloop()
