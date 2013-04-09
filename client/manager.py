#Used by server and client to do updates and shit

import pygame
import types
import pymunk
import math
from pygame.locals import*
from pygame.color import *
from twisted.python.filepath import FilePath
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from pymunk import Vec2d

class Manager():

	def __init__(self, seconds, level=None):
		self.level = level
		self.seconds = seconds
		self.client = None #can refer to client or server
		self.players = {}
		self.projectiles = pygame.sprite.Group()
		self.resolution = None

		self.space = pymunk.Space()

		self.createSpace()


	#temporary set-up
	def createSpace(self):
		staticLines = [pymunk.Segment(self.space.static_body, (50, 50), (50, 550), 5),
						pymunk.Segment(self.space.static_body, (50, 550), (550, 550), 5),
						pymunk.Segment(self.space.static_body, (550, 550), (550, 50), 5)]
		for line in staticLines:
			line.color = THECOLORS['lightgray']
			line.elasticity = .95

		self.space.add(staticLines)
		
	def update(self):
		#self.space._space.contents.elasticIterations = 10
		self.client.update()
		self.updateProjectiles()
		self.updateObjPos()

		self.space.step(1.0/60)

	def updateObjPos(self):
		#start with client move on from there in future

		obj = self.client
		rad = obj.toRadians()
		x = math.cos(rad)
		y = math.sin(rad)
		thrust = obj.thrust * -obj.direction[1]
		force = pymunk.Vec2d(thrust * x, thrust * y)
		print force
		offset = [0, 0]
		obj.body.apply_impulse(force, r=offset)
		pos = obj.body.position
		obj.rect.center = (pos.x, self.flipy(pos.y))

		for observer in obj.observers:
			observer.posChanged(obj)

	def updateProjectiles(self):
		for proj in self.projectiles:
			if not proj.updatePos():
				proj.kill()
			#add collision detection
		
	def addClient(self, client):
		self.client = client
		
	def addPlayer(self, player):
		self.players[id(player)] = player
		player.id = id(player)
		self.space.add(player.body, player.shape)

	def removePlayer(self, player):
		del self.players[player.id]

	def addProjectile(self, proj):
		self.projectiles.add(proj)

	def flipy(self, y):
	#Used to flip y coordinate, pymunk and pygame are inverted :/
		return -y + self.resolution[1]

				