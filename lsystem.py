#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Python L-System
#       
#       Copyright 2011 Mateus Zitelli <zitellimateus@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import pygame
from pygame.locals import *
from math import *
from time import *
import sys

surface = pygame.display.set_mode((900, 600))
surface.fill((255,255,255))
class Instructions:
	def __init__(self,inicial_state,rules,angle,interactions):
		self.instructions = inicial_state
		self.rules = rules
		self.angle = angle
		self.inter = interactions
	def solve(self):
		self.instructions = list(self.instructions)
		for t in range(self.inter):
			for inst in range(len(self.instructions)):
				if self.instructions[inst] in self.rules:
					self.instructions[inst] = self.rules[self.instructions[inst]]
			self.instructions = "".join(self.instructions) #Tansform all into a string
			self.instructions = list(self.instructions) #And transform back into a list, but now with each caracter separate from others.

def gerar(instructions,line_size,last = (400,400,0)):
	surface.fill((255,255,255))
	last_place = []
	for inst in range(len(instructions.instructions)):
		if instructions.instructions[inst] == "F": #Go to front
			new_angle = radians(last[2])
			next = (last[0]+cos(new_angle)*line_size,last[1]+sin(new_angle)*line_size,degrees(new_angle))		

		if instructions.instructions[inst] == "-": #Turn counterclockwise
			new_angle = radians(last[2]-instructions.angle)
			next = (last[0],last[1],degrees(new_angle))

		if instructions.instructions[inst] == "+": #Turn clockwise
			new_angle = radians(last[2]+instructions.angle)
			next = (last[0],last[1],degrees(new_angle))

		r = degrees(new_angle)%180/180.0 * 255
		b = (degrees(new_angle)+90)%180/180.0 * 255
		g = (degrees(new_angle)+45)%180/180.0 * 255
		#r,g,b = 0,0,0
		pygame.draw.aaline(surface,(r,g,b), (last[0],last[1]), (next[0],next[1]))
		#pygame.draw.circle(surface, (255,0,0), (next[0],next[1]),0.1)
		last = next
		if instructions.instructions[inst] == "[":
			last_place.append(last)
		if instructions.instructions[inst] == "]":
			last = last_place[-1]
			last_place.pop()
	
def GetInput(System): #Verificacao de eventos
		global zoom,local,angle,tempo, system
		key_pressed = pygame.key.get_pressed()
		event = pygame.event.wait()
		if event.type == QUIT or key_pressed[K_ESCAPE]:
			pygame.quit() #Fim do Script
			sys.exit()
		elif key_pressed[K_KP_PLUS]:
			zoom *= 2.0
			gerar(System,zoom,local)
			pygame.display.flip()
		elif key_pressed[K_MINUS]:
			zoom /= 2.0
			gerar(System,zoom,local)
			pygame.display.flip()
		elif key_pressed[K_UP]:
			local[1] -= 100
			gerar(System,zoom,local)
			pygame.display.flip()
		elif key_pressed[K_DOWN]:
			local[1] += 100
			gerar(System,zoom,local)
			pygame.display.flip()
		elif key_pressed[K_RIGHT]:
			local[0] += 100
			gerar(System,zoom,local)
			pygame.display.flip()
		elif key_pressed[K_LEFT]:
			local[0] -= 100
			gerar(System,zoom,local)
			pygame.display.flip()
		elif event.type == MOUSEMOTION and (time() - tempo > 0.001):
			if pygame.mouse.get_pressed()[0]:
				pos = event.pos[0]
				event_2 = pygame.event.wait()
				zoom -= (event_2.pos[0]-pos) / 4.0
				gerar(System,zoom,local)
				pygame.display.flip()
			elif pygame.mouse.get_pressed()[2]:
				angle = event.pos[0]/900.0*360
				System.angle = angle
				gerar(System,zoom,local)
				pygame.display.flip()
				tempo = time()
			elif pygame.mouse.get_pressed()[1]:
				pos = event.pos
				event_2 = pygame.event.wait()
				local[0]+=(event_2.pos[0]-pos[0])*4
				local[1]+=(event_2.pos[1]-pos[1])*4
				gerar(System,zoom,local)
				pygame.display.flip()
		elif key_pressed[K_p]:
			pygame.image.save(surface, "fract.png")
		elif key_pressed[K_1]:
			system = Instructions("F",{'F':'FF-[-F+F+F]+[+F-F-F]'},22.5,3) #Tree
			system.solve()
			zoom = 6
			local = [450,450,270]
			gerar(system,zoom,local)
			pygame.display.flip()
		elif key_pressed[K_2]:
			system = Instructions("F",{'F':'F+F-F-F+F'},60,4) #koch Flock
			system.solve()
			zoom = 1
			local = [450,450,270]
			gerar(system,zoom,local)
			pygame.display.flip()
if __name__ == "__main__":
	print """- Arrows -> Move the system
- Right Click + Mouse movement -> Zoom
- Left Click + Mouse movement -> Chage the system angle
- key P -> Print screen"""
	system = Instructions("F",{'F':'FF-[-F+F+F]+[+F-F-F]'},22.5,3) #Tree
	system.solve()
	zoom = 6
	local = [450,450,270]
	gerar(system,zoom,local)
	pygame.display.flip()
	tempo = time()

	while True:
		GetInput(system)
		tempo = time()
