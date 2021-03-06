#planet.py

from utils import *
from floaters import Floater
from adjectives import randItem
from parts import *
from spaceship import *
import stardog
from vec2d import Vec2d


class Planet(Floater):
	maxRadius = 1000000 # no gravity felt past this (approximation).
	PLANET_DAMAGE = .0004
	LANDING_SPEED = 200 #pixels per second. Under this, no damage.
	firstname = "Planet"
	secondname = "Unknown"
	
	def __init__(self, starsystem, pos, delta = Vec2d(0,0), grav=5000, radius = 100, mass = 10000, \
					color = (100,200,50), image = None, race = None):
		Floater.__init__(self, starsystem.game, pos, delta, radius = radius, image = image)
		self.mass = mass #determines gravity.
		self.color = color
		self.starSystem = starsystem
		self.g = grav
		self.damage = {}	
		#see solarSystem.planet_ship_collision
		self.race = None #race that owns this planet
		if image == None:
			self.image = None
		self.inventory = []
		for x in range(randint(1,8)):
			self.inventory.append(randItem(self.game, 1))
	
	def update(self):
		for other in self.starSystem.floaters.sprites():
			if other != self \
			and not isinstance(other, Structure) \
			and not isinstance(other, Planet) \
			and not collisionTest(self, other) \
			and abs(self.pos.get_distance(other.pos)) < self.maxRadius: # remove planets test for gravity sensitive planets
				#accelerate that floater towards this planet:
				accel = self.g * (self.mass) / (dist2(self, other))
				angle = (self.pos - other.pos).get_angle()
				other.delta += Vec2d(0,0).rotatedd(angle,accel) / self.game.fps

		# Floater.update(self) # for gravity sensitive planets update
	
	def draw(self, surface, offset = Vec2d(0,0)):
		if self.image:
			pos = (int(self.pos.x - self.image.get_width()  / 2 - offset[0]), 
				  int(self.pos.y - self.image.get_height() / 2 - offset[1]))
			surface.blit(self.image, pos())
		else:
			pos = self.pos - offset
			pygame.draw.circle(surface, self.color, pos.inttup(), int(self.radius))

	def takeDamage(self, damage, other):
		pass

	def collision(self, other):
		if  sign(other.pos.x - self.pos.x) == sign(other.delta.x - self.delta.x) \
			and sign(other.pos.y - self.pos.y) == sign(other.delta.y - self.delta.y):# moving away from planet.
				return False
		# planet/ship
		#planet/part
		elif isinstance(other, Part) and other.parent == None:
			self.freepartCollision(other)
			return True
		elif isinstance(other, Ship):
			if isinstance(self, Gateway):
				other.gatewayCollision(self)
			else:	
				other.planetCollision(self)
		#planet/planet
		elif isinstance(other, Planet):
			self.planetCollision(other)
			return True
		else:
			other.crash(self)

	def freepartCollision(self, part):
		part.kill()
		if rand() > .8 and not isinstance(part, Scrap):
			part.dir = 0
			part.image = colorShift(pygame.transform.rotate(part.baseImage, part.dir), part.color).convert()
		else:
			part = Scrap(self.game)
		self.inventory.append(part)

	def planetCollision(self, planet):
		if self.mass > planet.mass:
			planet.kill()
		else:
			self.kill()



class Star(Planet):
	PLANET_DAMAGE = 300
	LANDING_SPEED = -999
	firstname = "Star Unknown"
	
	def __init__(self, starsystem, pos, delta = Vec2d(0,0), grav=5000, radius = 3000, image = None):

		mass = radius * 100
		color = bulletColor((mass+.1)/250000)

		Planet.__init__(self, starsystem, pos, delta, grav, radius, mass, color, image)



class Structure(Planet):
	LANDING_SPEED = 200 #pixels per second. Under this, no damage.
	PLANET_DAMAGE = .0004
	firstname = "Structure Unknown"
	
	def __init__(self, starsystem, pos, delta, grav=5000, color = (100,200,50), radius = 100, image = None):
		Floater.__init__(self, starsystem.game, pos, Vec2d(0,0), 0, image=image)
		self.color = (0,0,255)
		self.g = grav
		self.starsystem = starsystem
		self.damage = {}	
		self.radius = radius
		#see solarSystem.planet_ship_collision
		self.race = None #race that owns this planet
		if image == None:
			self.image = None
		self.inventory = []

	def update(self):
		for other in self.starsystem.floaters.sprites():
			if  not isinstance(other, Planet) \
			and not isinstance(other, Structure) \
			and not collisionTest(self, other) \
			and abs(self.pos.get_distance(other.pos)) < self.maxRadius:
				#accelerate that floater towards this planet:
				accel = self.g * 100 / dist2(self, other)
				angle = (self.pos - other.pos).get_angle()
				other.delta.x += cos(angle) * accel / self.game.fps
				other.delta.y += sin(angle) * accel / self.game.fps

	def draw(self, surface, offset = Vec2d(0,0)):
		if self.image:
			pos = (int(self.pos.x - self.image.get_width()  / 2 - offset[0]), 
				  int(self.pos.y - self.image.get_height() / 2 - offset[1]))
			surface.blit(self.image, pos())
		else:
			pos = self.pos - offset
			rect = Rect(pos.x-self.radius*0.875,pos.y-self.radius*0.875,self.radius*1.75,self.radius*1.75)
			pygame.draw.rect(surface, self.color, rect)

	def takeDamage(self, damage, other):
		pass

class Gateway(Planet):
	maxRadius = 50000 # no gravity felt past this (approximation).
	tangible = True
	g = 5000 # the gravitational constant.
	firstname = "Gateway Unknown"
	rect = None
	image = None
	sister = None
	
	def __init__(self, starsystem, pos, radius = 100, mass = 10000, \
					color = (100,200,50), image = None, race = None):
		image = pygame.Surface((radius * 4, radius * 4), flags = hardwareFlag).convert()
		image.set_colorkey((0,0,0))
		Floater.__init__(self, starsystem.game, pos, Vec2d(0,0), radius = radius, image = image)
		self.mass = mass #determines gravity.
		self.starsystem = starsystem
		self.color = color
		self.race = None #race that owns this planet
		if image == None:
			self.image = None
		self.inventory = []
	
	def setSister(self, gateway):
		if instance(gateway, Gateway):
			self.sister = gateway

	def update(self):
		for other in self.starsystem.floaters.sprites():
			if  not isinstance(other, Planet) \
			and not isinstance(other, Structure) \
			and not collisionTest(self, other) \
			and abs(self.pos.get_distance(other.pos)) < self.radius * 1.2:
				#accelerate that floater towards this planet:
				accel = self.g * (self.mass) / dist2(self, other)
				angle = (self.pos - other.pos).get_angle()
				other.delta += Vec2d(0,0).rotatedd(angle, accel) / self.game.fps
				# other.delta.y += sin(angle) * accel / self.game.fps

	def getSister(self):
		return self.sister
	
	def draw(self, surface, offset = Vec2d(0,0)):
			self.image.fill((0, 0, 0, 0))

			pos = self.pos - offset
			pygame.draw.circle(self.image, self.color, pos.inttup(), int(self.radius))
			pygame.draw.circle(self.image, (0,0,0,0), pos.inttup(), int(self.radius)-30)
			Floater.draw(self, surface, offset)

	def takeDamage(self, damage, other):
		pass
