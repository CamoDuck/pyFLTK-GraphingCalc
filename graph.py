from fltk import *
import math

'''
known bugs:
* Domain, Range, x-intercepts, and y-intercepts only work for a few functions
* Sometimes lines wont be drawn near asymptotes
'''


def settings_cb(wid):
	if wid == dxSetting:
		app.dx = int(dxSetting.value())
	app.redraw()

def eqShow_cb(wid):
	if wid.label() == ">":
		wid.label("<")
		leftMenu.show()
		wid.position(leftMenu.w(),wid.y())
		app.redraw()
		but.show()
		for i in inputList:
			i.show()
			i.info.show()
	else:
		wid.label(">")
		leftMenu.hide()
		wid.position(0,wid.y())
		app.redraw()
		but.hide()
		for i in inputList:
			i.hide()
			i.info.hide()

def keyShow_cb(wid):
	if wid.label() == "^":
		wid.label("v")
		botMenu.show()
		wid.position((app.w()-wid.w())//2,app.h()-wid.h()-keylist[0].h()*4)
		app.redraw()
		numbers.show()
		gridLine.show()
		dxSetting.show()
		for i in keylist:
			i.show()
	else:
		wid.label("^")
		botMenu.hide()
		wid.position((app.w()-wid.w())//2,app.h()-wid.h())
		app.redraw()
		numbers.hide()
		gridLine.hide()
		dxSetting.hide()
		for i in keylist:
			i.hide()	
	
def fToI(n):
	if str(n)[-2:] == ".0":
		return int(n)
	return round(n*50)/50


def sign(num):
	if num == 0 or num == None or type(num) == complex:
		return None
	elif num > 0:
		return True
	return False

class keys(Fl_Button):
	def __init__(self, x, y, w, h,label=None):
		app.begin()
		super().__init__(x, y, w, h, label)
		self.callback(self.keys_cb)
		self.hide()

		app.end()

	def keys_cb(self, wid):
		if self.label() != "<-":
			selected.insert(self.label())
		else:
			selected.cut(-1)


class inputCalc(Fl_Input):
	def __init__(self, x, y, w, h, label=None):
		global selected
		selected = self
		app.begin()
		super().__init__(x, y, w, h, label)
		self.box(FL_PLASTIC_UP_BOX)
		self.callback(self.input_cb)
		self.when(FL_WHEN_CHANGED)
		self.info = Fl_Button(x+w,y,round(w/2.5),h, "info")
		self.info.callback(self.info_cb)
		app.end()
	def value(self):
		return super().value().replace("y=", "").replace(" ", "")

	def draw(self):
		app.redraw()
		super().draw()
	def input_cb(self, wid):
		global selected
		selected = self
		self.redraw()
		app.redraw()
		self.info_cb(self.info, "close")
	def handle(self, event):
		r=super().handle(event)
		if event == FL_PUSH:
			global selected
			selected = self
		return r
	def info_cb(self, wid, action=None): 
		if wid.h() == self.h() and action != "close":
			try:
				wid.size(self.w()*2, self.h()*4)
				val1 ="domain:" + self.getdomain() + "\n"
				val2 ="range:" + self.getrange() + "\n"
				val3 ="x-intercepts:" + self.intx() + "\n"
				val4 ="y-intercepts:" + self.inty()
				wid.label(val1 + val2 + val3 + val4)
				for i in inputList:
					if i != self:
						i.info.hide()
						i.redraw()
			except RecursionError:
				self.info_cb(wid)
		else:
			wid.size(round(self.w()/2.5),self.h())
			wid.label("info")
			for i in inputList:
				if i != self:
					i.info.show()
					i.redraw()
			
		wid.redraw()
		self.redraw()
		app.redraw()
	def getdomain(self): 
		length = 10000
		max = None
		min = None
		for x in range(-length, length+1):
			y = app.graph(self.value(), x*app.dx)
			if y == None:
				continue
			if min == None:
				max = x
				min = x
			elif max < x:
				max = x
			elif min > x:
				min = x
		
		if (min == -length and max == length) or (max == -length and min == length):
			return "x = R"
		elif max == -length or max == length:
			return "x >" + str(fToI(min))
		elif min == -length or min == length:
			return "x <" + str(fToI(max))
		else:
			return str(fToI(max)) + " > x > " + str(fToI(min))
		return ""
		
		
	def getrange(self):
		length = 10000
		max = None
		min = None
		for x in range(-length, length+1):
			y = app.graph(self.value(), x*app.dx)
			if y == None:
					continue
			if min == None:
				max = y
				min = y
			elif max < y:
				max = y
			elif min > y:
				min = y
		
		if (min == app.graph(self.value(), -length*app.dx) and max == app.graph(self.value(), length*app.dx)) or (max == app.graph(self.value(), -length*app.dx) and min == app.graph(self.value(), length*app.dx)):
			return "y = R"
		elif max == app.graph(self.value(), -length*app.dx) or max == app.graph(self.value(), length*app.dx):
			return "y >" + str(fToI(min))
		elif min == app.graph(self.value(), -length*app.dx) or min == app.graph(self.value(), length*app.dx):
			return "y <" + str(fToI(max))
		else:
			return str(fToI(max)) + " > y > " + str(fToI(min))

	def intx(self, eq=None): 
		if eq == None:
			eq=self.value()
			found = eq.find("/")
			if found != -1:
				eq = eq[:found]
		roots = []
		endx = 10000
		add=-1
		tol = 0.000001
		for x in range(2):
			add = -add
			a = 0
			b = 0
			while b<endx and b>-endx:
				if sign(app.graph(eq, a*app.dx)) != sign(app.graph(eq, b*app.dx)):
					while True:
						
						c = (a + b)/2
						if (app.graph(eq, c*app.dx)) != None:
							if app.graph(eq, c*app.dx) < tol and app.graph(eq, c*app.dx) > -tol:
								a = c+(add*tol)
								b = c+(add*tol)
								roots.append(fToI(round(c*50)/50))
								break
						if sign(app.graph(eq,c*app.dx)) == sign(app.graph(eq,a*app.dx)):
							a = c
						else:
							b = c
				b+=add
		if 0.0 in roots:
			roots.remove(0.0)
		
		for x in roots:
			if (self.value(), x) == None:
				roots.remove(x)
		
		return str(roots)
	def inty(self):

		return "[" + str(fToI(app.graph(self.value(), 0))) + "]"


class MyApp(Fl_Window):
	def __init__(self, x,y, w, h, label=None):
		super().__init__( x, y, w, h, label)
		self.color(FL_WHITE)
		self.end()
		self.scale = 1
		self.sep=50
		self.xOffset=(size-1)/2
		self.yOffset=(size-1)/2
		self.lastx=None
		self.lasty=None
		self.dx = 200

	def handle(self, event):
		r=super().handle(event)
		
		if event==FL_MOUSEWHEEL:
			if self.sep <= 70 and self.sep >= 30: 
				xchange = self.xOffset/self.sep-((Fl.event_x()-self.xOffset)/self.sep*Fl.event_dy())
				ychange = (Fl.event_y()-self.yOffset)/self.sep*Fl.event_dy()
				self.xOffset +=(Fl.event_x()-self.xOffset)/self.sep*Fl.event_dy()
				self.yOffset +=(Fl.event_y()-self.yOffset)/self.sep*Fl.event_dy()
				self.sep -=Fl.event_dy()  
				self.redraw()
				if self.sep > 70:
					self.sep = 30
					self.scale/=2
				elif self.sep < 30:
					self.sep = 70
					self.scale*=2
			return 1
		elif event == FL_DRAG:
			self.xOffset -= self.lastx-Fl.event_x()
			self.yOffset -= self.lasty-Fl.event_y()  
			self.lastx = Fl.event_x()
			self.lasty = Fl.event_y()      
			self.redraw()
			return 1
			
		elif event == FL_PUSH:
			self.lastx = Fl.event_x()
			self.lasty = Fl.event_y()
			return 1
		return r
	def draw(self): 
		
		Fl_Window.draw(self)
		fl_color(FL_BLUE)
		
		fl_color(FL_GRAY)
		fl_line_style(FL_DASH)
		fl_font(fl_font(),8)

		left = 0
		bot = 0
		if botMenu.visible() == True:
			bot = botMenu.h()
		if leftMenu.visible() == True:
			left = leftMenu.w()
		fl_pop_clip()
		fl_push_clip(left,0,self.w(),self.h()-bot)
			

		for x in range(round(self.xOffset%self.sep),self.w()+1,self.sep):
			if gridLine.value() == 1:
				fl_color(FL_GRAY)
				fl_line(x,0,x,self.h())
			if round((x-self.xOffset)/self.sep) != 0 and numbers.value() == 1:
				fl_color(FL_BLACK)
				fl_draw(str(self.scale*round((x-self.xOffset)/self.sep)),round(x)-15,round(self.yOffset), 30, 30, FL_ALIGN_INSIDE)
		for y in range(round(self.yOffset%self.sep),self.h()+1,self.sep):
			if gridLine.value() == 1:
				fl_color(FL_GRAY)
				fl_line(0,y,self.w(),y) 
			if round((y-self.yOffset)/self.sep) != 0 and numbers.value() == 1:
				fl_color(FL_BLACK)
				fl_draw(str(self.scale*round((y-self.yOffset)/self.sep)),round(self.xOffset)-30, round(y)-15, 30, 30, FL_ALIGN_INSIDE)
			
		fl_color(FL_BLACK)
		fl_line_style(FL_SOLID,3)
		if (self.xOffset>0 and self.xOffset<self.w()):
			fl_line(round(self.xOffset),0,round(self.xOffset),self.h())
		if (self.yOffset>0 and self.yOffset<self.h()):
			fl_line(0,round(self.yOffset),self.w(),round(self.yOffset))
		
		
		fl_line_style(FL_SOLID, 2)
		
		for i in range(len(inputList)):
			prevx = None
			prevy = None
			equation = inputList[i].value()
			fl_color(colorList[i])

			for x in range(-round(self.xOffset*self.scale/self.sep)*self.dx, (round((self.w()-self.xOffset)*self.scale/self.sep)+1)*self.dx):
				try:
					y = self.graph(equation,x)
					if y == None:
						prevx = None
						prevy = None
						continue
						
					x = round((self.xOffset)+(x/self.dx*self.sep/self.scale))
					y = round((self.yOffset)-(y*self.sep/self.scale))
					if prevy != None and y != None :
						if (y < self.h() and y > 0) or (prevy < self.h() and prevy > 0):
							fl_line(prevx, prevy, x, y)
					prevy = y
					prevx = x
				except RecursionError:
					break
			
			
			
		
		
	def graph(self, s, x, extra=None):
		if s.replace('.','').isdigit():
			return float(s)
		elif s == "x":
			return x/self.dx
		scopy = s
		tot = 0
		while ")" in s and "(" in s: 
			if s[0] == "(":
				tot+= s.find(")") - s.find("(") + 1
			s = s[:s.find("(")] + s[s.find(")")+1:]
			
		if "+" in s:
			found = s.find("+")
			result1 = self.graph(scopy[:found+tot],x)
			result2 = self.graph(scopy[found+tot+1:],x)
			if result1 == None or result2 == None:
				return None
			return result1 + result2
		elif "-" in s:
			found = s.find("-")
			result1 = self.graph(scopy[:found+tot],x)
			result2 = self.graph(scopy[found+tot+1:],x)
			if result1 == None or result2 == None:
				return None
			return result1 - result2
		elif "*" in s:
			found = s.find("*")
			result1 = self.graph(scopy[:found+tot],x)
			result2 = self.graph(scopy[found+tot+1:],x)
			if result1 == None or result2 == None:
				return None
			return result1 * result2
		elif "/" in s:
			found = s.find("/")
			result1 = self.graph(scopy[:found+tot],x)
			result2 = self.graph(scopy[found+tot+1:],x)
			if result1 == None or result2 == None or result2 == 0:
				return None
			return result1 / result2
		elif "^" in s:
			found = s.find("^")
			result1 = self.graph(scopy[:found+tot],x)
			result2 = self.graph(scopy[found+tot+1:],x)
			if result1 == None or result2 == None:
				return None
			return result1 ** result2
		elif "√" in s:
			found = s.find("√")
			result1 = self.graph(scopy[found+tot+1:],x)
			result2 = self.graph(scopy[:found+tot],x)
			if result1 == None or result2 == None or result1 < 0 or result2 == 0:
				return None
			return result1 ** (1/result2)
		elif "sin" in s: 
			found = s.find("sin")
			result1 = self.graph(scopy[found+tot+3:],x)
			if result1 == None:
				return None
			return math.sin(result1)
		elif "cos" in s:
			found = s.find("cos")
			result1 = self.graph(scopy[found+tot+3:],x)
			if result1 == None:
				return None
			return math.cos(result1)
		elif "tan" in s:
			found = s.find("tan")
			result1 = self.graph(scopy[found+tot+3:],x)
			if result1 == None:
				return None
			return math.tan(result1)
		elif "log" in s:
			found = s.find("log")
			result1 = self.graph(scopy[found+tot+3:],x)
			result2 = self.graph(scopy[:found+tot],x)
			
			if result1 <= 0 or result2 <= 0 or result2 == 1 or result1 == None or result2 == None:
				return None
			return math.log(result1,result2)

		return self.graph(scopy.replace(")","").replace("(",""),x)
	

def but_cb(wid):
	app.begin()
	inputList.append(inputCalc(0,(len(inputList))*app.h()//10,round(app.w()/5),app.h()//10))
	wid.clear()
	wid.position(0,len(inputList)*app.h()//10)
	wid.redraw()
	app.redraw()

size=501
selected = None
inputList=[]
colorList = [FL_RED,FL_GREEN, FL_MAGENTA ,FL_YELLOW, FL_CYAN, FL_BLUE, FL_DARK_MAGENTA, FL_DARK_YELLOW]

app = MyApp(0,0, size, size)
app.resizable(app)
app.begin()

keyShow = Fl_Button((size-50)//2, size-20, 50, 20, "^")
keyShow.callback(keyShow_cb)

eqShow = Fl_Button(0, size//2-25, 20, 50, ">")
eqShow.callback(eqShow_cb)

keylist = ["1", "2", "3", "+", "-", "sin", "<-",
"4", "5", "6", "*", "/", "cos", "(",
"7", "8", "9", "^", "√", "tan", ")",
"", "0", ".", "x", "y", "log", "="]

leftMenu = Fl_Box(0,0,140,size)
leftMenu.box(FL_PLASTIC_DOWN_BOX)
leftMenu.hide()

botMenu = Fl_Box(0,size-120,size,120)
botMenu.box(FL_PLASTIC_DOWN_BOX)
botMenu.hide()

but = Fl_Button(0,0, 50,50, "+")
but.callback(but_cb)
but.hide()

numbers = Fl_Light_Button(400, botMenu.y()+20, 80,20, "Numbers")
gridLine = Fl_Light_Button(400, botMenu.y()+50, 80,20, "Grid lines")
dxSetting = Fl_Input(400, botMenu.y()+80, 80, 20)
numbers.value(1)
gridLine.value(1)
dxSetting.value(str(app.dx))
numbers.hide()
gridLine.hide()
dxSetting.hide()
numbers.callback(settings_cb)
gridLine.callback(settings_cb)
dxSetting.callback(settings_cb)
dxSetting.when(FL_WHEN_CHANGED)


for i in range(len(keylist)):
	keylist[i] = keys(size//2-105+i%7*30,(i//7*30)+(size-120), 30, 30, keylist[i])


app.end()
app.show()

Fl.run() 