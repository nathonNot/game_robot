#!/usr/bin/python
#coding=utf-8
 
import math
import win32gui
import win32con
import win32api
# import autopy
from PIL import ImageGrab
from PIL import Image
import time
import threading
 
# game window handler		
g_game_window = None
 
# upper-left corner coordinate of game window
g_game_window_x = None
g_game_window_y = None
g_game_rect = None
 
# upper-left corner coordinate of arrows box
g_input_box_x = None
g_input_box_y = None
g_input_box_width = 330
g_input_box_height = 44
 
# const numbers
k_window_name = u"QQ炫舞"
k_input_offset_x = 366
k_input_offset_y = 486
 
 
k_arrow_width = 25
k_arrow_height = 25
#k_arrow_space = 9
k_arrow_space = 10
k_arrow_first_offset_x = 33
k_arrow_first_offset_y = 10
k_max_arrows_count = 8
 
# enum of dir
k_dir_up = 0
k_dir_down = 1
k_dir_left= 2
k_dir_right = 3
k_dir_unknown = 4
 
# color of flag 
k_flag_r = 255
k_flag_g = 125
k_flag_b = 90
 
# flag pos
start_x = 539 
start_y = 464
 
dest_x = 652
dest_y = 464
 
check_offset = 100
 
def getGameWindow():
	print('getGameWindow')
	global k_window_name
	wind = win32gui.FindWindow(None,k_window_name)
	return wind
 
'''
初始化 参数值
'''
def initSettings():
	global g_game_window
	global g_game_window_x
	global g_game_window_y
	global g_input_box_x
	global g_input_box_y
	global k_input_offset_x
	global k_input_offset_y
 
	# get window handle
	g_game_window = getGameWindow()
	if g_game_window == 0:
		print("Please launch game before run this script!")
		return False
	print("Game window handle: " + str(g_game_window))
	
	# place window to foreground
	win32gui.ShowWindow(g_game_window,win32con.SW_RESTORE)
	win32gui.SetForegroundWindow(g_game_window)
	
	# get game window aabb box
	g_game_rect = win32gui.GetWindowRect(g_game_window)
	g_game_window_x = g_game_rect[0]
	g_game_window_y = g_game_rect[1]
	
	# input box coordinate
	g_input_box_x = g_game_window_x + k_input_offset_x
	g_input_box_y = g_game_window_y + k_input_offset_y
	print("input box coordinate: (" + str(g_input_box_x) + "," + str(g_input_box_y) + ")")
	return True
 
	
	
'''
判断是否是箭头的颜色
'''
def isArrowColor(colorVal):
	if colorVal[2] >= 190 and colorVal[0] < 140:	# blue 210?
		return True
	return False
 
'''
检查箭头数量是否是奇数
'''
def isArrowsNumOdd(imgInputBox):
	global g_input_box_x
	global g_input_box_y
	
	# for curCheckBoxNum in range(k_max_arrows_count):
		# for eachPt in range()
	
	isOdd = False
	imgWidth = imgInputBox.size[0]
	imgHeight = imgInputBox.size[1]
		
	if isArrowColor(imgInputBox.getpixel((imgWidth/2,imgHeight/2))):
		isOdd = True
	return isOdd
		
'''
获取箭头坐标列表
'''
def getArrowsList(img,isOdd):
	imgWidth = img.size[0]
	imgHeight = img.size[1]
	
	length = 0
	loopTimes = int(k_max_arrows_count / 2)
	if isOdd:
		length = 1
		loopTimes = loopTimes - 1
	
	baseCoordX = 0
	baseCoordY = imgHeight / 2 - k_arrow_height / 2
	if isOdd:
		baseCoordX = imgWidth / 2 - k_arrow_width/2 - loopTimes * (k_arrow_width + k_arrow_space)
	else:
		baseCoordX = imgWidth / 2 - k_arrow_space / 2 - (loopTimes - 1) * k_arrow_space - loopTimes * k_arrow_width
		
	#baseCoordX = baseCoordX + g_input_box_x
	baseCoordX = baseCoordX + g_input_box_x + 1	# +1 fix offset
	baseCoordY = baseCoordY + g_input_box_y
	
	arrowsList = []
	for i in range(k_max_arrows_count):
		curX = baseCoordX + i * (k_arrow_width + k_arrow_space)
		curY = baseCoordY
		arrowBox = (curX,curY,curX + k_arrow_width,curY + k_arrow_height)
		image = ImageGrab.grab(arrowBox)
		#image.save("./output/" + str(i) + ".png","png")
		arrowsList.append(image)
	return arrowsList
	
'''
箭头截图
'''
def grabArrows():
	print('grabArrows')
	global g_input_box_x
	global g_input_box_y
	global k_arrow_space
	global k_arrow_width
	global k_arrow_height
	global k_max_arrows_count
	global g_input_box_width
	global g_input_box_height
	
	inputBox = (g_input_box_x,g_input_box_y,g_input_box_x + g_input_box_width , g_input_box_y + g_input_box_height)
	imgInputBox = ImageGrab.grab(inputBox)
	#imgInputBox.save("./output/inputBox.png","png")
	
	isOdd = isArrowsNumOdd(imgInputBox)
	return getArrowsList(imgInputBox,isOdd)
	
'''
根据图片,检测是哪个方向键
'''
def checkDir(img):
	'''
		key points coordinate:
		(6,8) 	(18,8)
		(6,17) 	(18,17)
	'''
	if isArrowColor(img.getpixel((6,8))) and isArrowColor(img.getpixel((18,8))):
		print("up")
		return k_dir_up
	elif isArrowColor(img.getpixel((6,17))) and isArrowColor(img.getpixel((18,17))):
		print("down")
		return k_dir_down
	elif isArrowColor(img.getpixel((6,8))) and isArrowColor(img.getpixel((6,17))):
		print("left")
		return k_dir_left
	elif isArrowColor(img.getpixel((18,8))) and isArrowColor(img.getpixel((18,17))):
		print("right")
		return k_dir_right
		
	print("unknown")
	return k_dir_unknown
 
'''
根据箭头列表，确定方向键列表
'''
def getArrowsKeys(arrowsList):
	print("keys -------------------- ")
	keysList = []
	for i in range(len(arrowsList)):
		checkResult = checkDir(arrowsList[i])
		if checkResult != k_dir_unknown:
			keysList.append(checkResult)
	return keysList
	
 
def pressDirKey(keyList):
	for i in range(len(keyList)):
		dir = keyList[i]
		keyCode = 0
		if dir == k_dir_up:
			keyCode = 38
		elif dir == k_dir_down:
			keyCode = 40
		elif dir == k_dir_left:
			keyCode = 37
		elif dir == k_dir_right:
			keyCode = 39
		hardwareScanCode = win32api.MapVirtualKey(keyCode,0)
		win32api.keybd_event(keyCode,hardwareScanCode,0,0)
		win32api.keybd_event(keyCode,hardwareScanCode,win32con.KEYEVENTF_KEYUP,0)
 
def pressSpaceKey():
	keyCode = 32
	hardwareScanCode = win32api.MapVirtualKey(keyCode,0)
	win32api.keybd_event(keyCode,hardwareScanCode,0,0)
	win32api.keybd_event(keyCode,hardwareScanCode,win32con.KEYEVENTF_KEYUP,0)
	
'''
检测是否是 flag 节奏标 的 颜色
'''
def isFlagColor(colorVal):
	# for i in range(len(colorVal)):
		# print colorVal[i]
	#if colorVal[0] == k_flag_r and colorVal[1] == k_flag_g and colorVal[2] == k_flag_b:
	
	#if colorVal[0] < 255:
	if colorVal[0] < 240:
		return False
	if colorVal[1] <= 90 or colorVal[1] >= 120:
		return False
	if colorVal[2] <= 50 or colorVal[2] >= 85:
		return False
	return True
 
is_in_turn = True
def startTurn():
	print("start turn")
	global is_in_turn
	is_in_turn = True
	
	arrowsList = grabArrows()
	keyList = getArrowsKeys(arrowsList)
	pressDirKey(keyList)
		
	
def endTurn():
	print("end turn")
	global is_in_turn
	is_in_turn = False
	
	
def triggerSpace():
	print("trigger space")
	pressSpaceKey()
	
'''
todo 
检测 什么时候 开始新一轮，什么时候 要按  space 键
# 并且按下 空格键
'''
def checkTimer():
	global start_x
	global start_y
	global dest_x
	global dest_y
	global is_in_turn
	start_x = start_x + g_game_window_x
	start_y = start_y + g_game_window_y
	dest_x = dest_x + g_game_window_x
	dest_y = dest_y + g_game_window_y
	
	# startBlockImg = ImageGrab.grab((start_x,start_y,start_x + check_offset,start_y + check_offset))
	# startBlockImg.save("./output/check.png","png")
	
	while True:
		# time.sleep(0.01)
		# print "is in turn?" + str(is_in_turn)
		if not is_in_turn:
			startBlockImg = ImageGrab.grab((start_x,start_y,start_x + check_offset,start_y + check_offset))
			if isFlagColor(startBlockImg.getpixel((1,3))):
				startTurn()
		else:
			destBlockImg = ImageGrab.grab((dest_x,dest_y,dest_x + check_offset,dest_y + check_offset))
			if isFlagColor(destBlockImg.getpixel((1,3))):
				triggerSpace()
				endTurn()
 
				
 
def mainFunc():
	if not initSettings():
		return
		
	checkTimer()
	# th = threading.Thread(target = checkTimer)
	# th.setDaemon(True)
	# th.start()
	# dealFunc()
	
if __name__ == '__main__':
	print('AutoDance')
	mainFunc()
	print('AutoDance exit!')