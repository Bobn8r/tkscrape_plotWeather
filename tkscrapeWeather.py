#!/usr/bin/env python3
from bs4 import BeautifulSoup as soup
import requests
import lxml
from tkinter import *
from sys import *
from time import *

def getulist():
	
	f = open('/home/pi/ulist.csv','r')
	dump=f.readlines()
	f.close()
	l=len(dump)	
	n=int(dump.pop())
	print (n, dump[n])
	dump.append(str(n+1))
	if n>=l-1:
		n=0
	f=open('ulist.csv','w')
	f.writelines(dump)
	f.close()
	return 'https://weather.com/weather/today/l/'+dump[n]

def dismantle(whdppv):
	returnlist=[]
	for i in range(0,len(whdppv)):
		if whdppv[i]=='H':
			returnlist.append(i)
		if whdppv[i]=='P':
			returnlist.append(i)
		if whdppv[i]=='V':
			returnlist.append(i)
	return returnlist

def main():	
	bgc=''
	ulist=[]
	ulist =getulist()
	
	url=ulist
	print(url)
	r=requests.get(url)
	page_soup=soup(r.content)
	dl=[]		
	try:
		temp=page_soup.find('div',{"class":'today_nowcard-temp'}).text
		cond=page_soup.find('div',{'class':'today_nowcard-phrase'}).text
	except AttributeError:
		pass
	tnscp=page_soup.find('div',{'class':'today_nowcard-sidecar component panel'})
	try:
		whdppv=tnscp.text
		dl=dismantle(whdppv)
		wind =whdppv[13:dl[0]]
		hmdt =whdppv[dl[0]+8:dl[1]-4]
		dewp =whdppv[dl[1]+5:dl[2]]
		prss =whdppv[dl[2]+8:dl[3]-1]
		Vis=whdppv[dl[3]+10:len(whdppv)]
		print('Temp: %s Wind: %s Humidity: %s \nDew Point: %s Barometer: %s Visibility: %s' %\
				(temp,wind,hmdt,dewp,prss,Vis))
		if cond=='Cloudy':
			bgc='grey'
		elif cond=='Mostly Cloudy':
			bgc='lightgray'
		elif cond=='Partly Cloudy':
			bgc='cornflowerblue'
		elif cond=='Fair':
			bgc='lightsteelblue'
		elif cond=='Clear':
			bgc='royalblue'
		elif cond=='Sunny':
			bgc='yellow'
		elif cond=='Rain':
			bgc='Purple'
		elif cond=='Light Rain':
			bgc='lavender'
		if bgc=='':
			bgc='gray'				
		labt.config(text='Temp: '+temp)
		labc.config(text='Conditions: '+cond,bg=bgc)
		labw.config(text='Wind: '+wind)
		labh.config(text='Humidity: '+hmdt)
		labd.config(text='Dew Point: '+dewp)
		labp.config(text='Barometer: '+prss)
		labV.config(text='Visibility: '+Vis)
		labi.config(text=strftime('Time: %H:%M',localtime()))
		labV.after(30000,main)
	except:
		pass
	
lblfont='helvetica 15'
root=Tk()
root.title(argv[0])
root.geometry('300x230+550+00')

labt=Label(root,text='',font=lblfont)
labc=Label(root,text='',font=lblfont)
labw=Label(root,text='',font=lblfont)
labh=Label(root,text='',font=lblfont)
labd=Label(root,text='',font=lblfont)
labp=Label(root,text='',font=lblfont)
labV=Label(root,text='',font=lblfont)
labi=Label(root,text='',font=lblfont)
labt.pack()
labc.pack()
labw.pack()
labh.pack()
labd.pack()
labp.pack()
labV.pack()
labi.pack()
main()
root.mainloop()
