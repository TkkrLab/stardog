#solarSystem.py

from utils import *
from floaters import *
from spaceship import *
from strafebat import *
from tinyFighter import *
from planet import *
from gui import *
import stardog
from vec2d import Vec2d

class SolarSystem:
	"""A SolarSystem holds ships and other floaters."""
	boundries = ((-30000, 30000), (-30000, 30000))
	drawEdgeWarning = False
	def __init__(self, game):
		self.game = game
		self.floaters = pygame.sprite.Group()
		self.ships = pygame.sprite.Group()
		self.specialOperations = []
		self.onScreen = []
		self.bg = BG(self.game) # the background layer
		pygame.mixer.music.load("res/sound/space music.ogg")
		pygame.mixer.music.play(-1)
		pygame.mixer.music.set_volume(.15)
		self.planets = []
		self.structures = []
		self.name = ""
		
		
	def update(self):
		"""Runs the game."""
		self.floaters.update()
		
		#collision:
		# TODO: sort lists to minimize collision tests.
		floaters = self.floaters.sprites()
		for i in range(len(floaters)):
			for j in range(i + 1, len(floaters)):
				self.collide(floaters[i], floaters[j])
				#see collide() at bottom of this module.
				
		#keep ships in system for now:
		edge = self.boundries
		if self.drawEdgeWarning:
			self.drawEdgeWarning -= 1. / self.game.fps
			if self.drawEdgeWarning <=0:
				self.drawEdgeWarning = False
				
		for floater in self.floaters:
			if floater.pos.x < edge[0][0] and floater.delta.x < 0 \
			or floater.pos.x > edge[0][1] and floater.delta.x > 0:
				if isinstance(floater, Ship):
					floater.dx = 0
					if floater == self.game.player:
						self.drawEdgeWarning = 1
				else:
					try:
						floater.kill()
					except TypeError:
						print floater
			if floater.pos.y < edge[1][0] and floater.delta.y < 0 \
			or floater.pos.y > edge[1][1] and floater.delta.y > 0:
				if isinstance(floater, Ship):
					floater.delta.y = 0
					if floater == self.game.player:
						self.drawEdgeWarning = self.game.fps
				else:
					try:
						floater.kill(Floater())
					except TypeError:
						print floater
		#list floaters that are on screen now:
		self.onScreen = []
		offset = Vec2d(self.game.player.pos.x - self.game.width / 2, 
				self.game.player.pos.y - self.game.height / 2)
		for floater in self.floaters:
			r = floater.radius
			if (r + floater.pos.x > offset[0] \
				and floater.pos.x - r < offset[0] + self.game.width)\
			and (r + floater.pos.y > offset[1] \
				and floater.pos.y - r < offset[1] + self.game.height):
					self.onScreen.append(floater)
					
		#do any special actions that don't fit elsewhere:
		#(currently just laser collisions)
		for function in self.specialOperations:
			function()
		self.specialOperations = []

		for planet in self.planets:
			if not planet.ships.sprites():
				if planet.respawn > 0:#countdown the timer
					planet.respawn -= 1. / self.game.fps
					continue
				else:
					#respawn now!
					planet.respawn = self.respawnTime #reset respawn timer
					planet.numShips += 1
					for i in range(planet.numShips):
						angle = randint(0, 360)
						x = planet.pos.x + cos(angle) * (planet.radius + 300)
						y = planet.pos.y + sin(angle) * (planet.radius + 300)
						ship = Strafebat(self.game, Vec2d(x,y), color = planet.color)
						planet.ships.add(ship)
						self.add(ship)
						ship.planet = planet
		
	def draw(self, surface, offset):
		self.bg.draw(surface, self.game.player)
		for floater in self.onScreen:
				floater.draw(surface, offset)
		
	def add(self, floater):
		"""adds a floater to this game."""
		self.floaters.add(floater)
		if isinstance(floater, Ship):
			self.ships.add(floater)
		
	def empty(self):
		self.ships.empty()
		self.floaters.empty()

	def collide(self, a, b):
		if a.tangible and b.tangible and collisionTest(a, b):
			a.collide(b)
			b.collide(a)

	# def collide(self, a, b):
	# 	"""test and act on spatial collision of Floaters a and b"""
	# 	#Because this needs to consider the RTTI of two objects,
	# 	#it is an external function.  This is messy and violates
	# 	#good object-orientation, but when a new subclass is added
	# 	#code only needs to be added here, instead of in every other
	# 	#class.
	# 	if a.tangible and b.tangible and collisionTest(a, b):
	# 		if isinstance(b, Structure): a,b = b,a
	# 		if isinstance(a, Structure):
	# 			if isinstance(b, Ship):
	# 				self.structure_ship_collision(a, b)
	# 				return True

	# 		#planet/?
	# 		if isinstance(b, Planet): a,b = b,a
	# 		if isinstance(a, Planet):
	# 			if  sign(b.pos.x - a.pos.x) == sign(b.delta.x - a.delta.x) \
	# 			and sign(b.pos.y - a.pos.y) == sign(b.delta.y - a.delta.y):# moving away from planet.
	# 				return False
	# 			# planet/ship
	# 			if isinstance(b, Ship):
	# 				self.planet_ship_collision(a, b)
	# 				return True
	# 			#planet/part
	# 			if isinstance(b, Part) and b.parent == None:
	# 				self.planet_freePart_collision(a, b)
	# 				return True
	# 			#planet/planet
	# 			if isinstance(b, Planet):
	# 				self.planet_planet_collision(a,b)
	# 				return True
					
	# 		if isinstance(b, Explosion): a,b = b,a
	# 		if isinstance(a, Explosion):
	# 			self.explosion_push(a,b)
	# 			#but don't return!
	# 		#shield ship/?
	# 		if isinstance(b, Ship) and b.hp > 0: a,b = b,a
	# 		if isinstance(a, Ship) and a.hp > 0:
	# 			#shield ship/free part
	# 			if isinstance(b, Part) and b.parent == None:
	# 				self.ship_freePart_collision(a, b)
	# 				return True
	# 			#crash against ship's shields, if any:
	# 			hit = False
	# 			if b.hp >= 0 and (sign(b.pos.x - a.pos.x) == - sign(b.delta.x - a.delta.x) \
	# 							or sign(b.pos.y - a.pos.y) == - sign(b.delta.y - a.delta.y)):
	# 				# moving into ship, not out of it.
	# 				self.crash(a,b)
	# 				hit = True
	# 				#if this ship no longer has shields, start over:
	# 				if a.hp <= 0:
	# 					self.collide(a, b)
	# 					return True
	# 			#shield ship/no shield ship (or less shield than this one)
	# 			if isinstance(b, Ship) and b.hp <= 0:
	# 				for part in b.parts:
	# 					if self.collide(a, part):
	# 						#if that returned true, everything
	# 						#should be done already.
	# 						return True
	# 			return hit

	# 		#ship / ?
	# 		if isinstance(b, Ship): a,b = b,a
	# 		if isinstance(a, Ship):
	# 			#ship/free part
	# 			if isinstance(b, Part) and b.parent == None:
	# 				self.ship_freePart_collision(a, b)
	# 				return True
								
	# 			#recurse to ship parts
	# 			hit = False
	# 			for part in a.parts:
	# 				if self.collide(b, part):#works for ship/ship, too.
	# 					#if that returned true, everything
	# 					#should be done already.
	# 					hit = True
	# 			return hit
				
	# 		#free part/free part
	# 		if isinstance(b, Part) and b.parent == None \
	# 		and isinstance(a, Part) and a.parent == None:
	# 			return False #pass through each other, no crash.
			
	# 		#floater/floater (no ship, planet)
	# 		else:
	# 			self.crash(a, b)
	# 			return True
	# 	return False

	# ship - ship
	# ship - freepart
	# ship - planet
	# planet - freepart
	# bullet - freepart
	# bullet - planet
	# ship - bullet
	# explotion - floater
	# planet - planet
	# floater - floater

	def structure_ship_collision(self, structure, ship):
		angle = (structure.pos - ship.pos).get_angle()
		dx, dy = rotate(ship.delta.x, ship.delta.y, angle)
		speed = sqrt(dy ** 2 + dx ** 2)
		if speed > structure.LANDING_SPEED:
			if structure.damage.has_key(ship):
				damage = structure.damage[ship]
			else:
				if soundModule:
					setVolume(hitSound.play(), structure, structure.game.player)
				#set damage based on incoming speed and mass.
				damage = speed * ship.mass * structure.STRUCTURE_DAMAGE
			for part in ship.parts:
				if collisionTest(structure, part):
					temp = part.hp
					part.takeDamage(damage, structure)
					damage -= temp
					if damage <= 0:
						r = ship.radius + structure.radius
						ship.delta = ship.delta * (ship.pos - structure.pos) + ship.delta * -(ship.pos - structure.pos)
						if structure.damage.has_key(ship):
							del structure.damage[ship]
						return
			if damage > 0:
				structure.damage[ship] = damage
		else:
			#landing:
			if ship == structure.game.player and not ship.landed:
				structure.game.pause = True
				ship.landed = structure
				ship.game.menu.parts.reset()
			ship.delta.x, ship.delta.y = structure.delta.x, structure.delta.y

	# def planet_ship_collision(self, planet, ship):
	# 	angle = (planet.pos - ship.pos).get_angle()
	# 	dx, dy = rotate(ship.delta.x, ship.delta.y, angle)
	# 	speed = sqrt(dy ** 2 + dx ** 2)
	# 	if speed > planet.LANDING_SPEED:
	# 		if planet.damage.has_key(ship):
	# 			damage = planet.damage[ship]
	# 		else:
	# 			if soundModule:
	# 				setVolume(hitSound.play(), planet, planet.game.player)
	# 			#set damage based on incoming speed and mass.
	# 			damage = speed * ship.mass * planet.PLANET_DAMAGE
	# 		for part in ship.parts:
	# 			if collisionTest(planet, part):
	# 				temp = part.hp
	# 				part.takeDamage(damage, planet)
	# 				damage -= temp
	# 				if damage <= 0:
	# 					r = ship.radius + planet.radius
	# 					ship.delta = ship.delta * (ship.pos - planet.pos) + ship.delta * -(ship.pos - planet.pos)
	# 					if planet.damage.has_key(ship):
	# 						del planet.damage[ship]
	# 					return
	# 		if damage > 0:
	# 			planet.damage[ship] = damage
	# 	else:
	# 		#landing:
	# 		if ship == planet.game.player and not ship.landed:
	# 			planet.game.pause = True
	# 			ship.landed = planet
	# 			ship.game.menu.parts.reset()
	# 		ship.delta.x, ship.delta.y = planet.delta.x, planet.delta.y

	# def planet_freePart_collision(self,planet, part):
	# 	part.kill()
	# 	planet.inventory.append(part)
		
	# def planet_planet_collision(self, a, b):
	# 	pass
		# if a.mass > b.mass:
		# 	b.kill()
		# else:
		# 	a.kill()
			
	# def ship_freePart_collision(self,ship, part):
	# 	pass
		# part.kill()
		# ship.inventory.append(part)
		# if ship.game.player == ship:
		# 	ship.game.menu.parts.inventoryPanel.reset() #TODO: make not suck
		
	def explosion_push(self, explosion, floater):
		"""The push of an explosion.  The rest of the effect is handled by the
		collision branching, which continues."""
		force = (explosion.force / 
				not0(dist2(explosion, floater)) * explosion.radius ** 2)
		dir = atan2(floater.pos.y - explosion.pos.y, floater.pos.x - explosion.pos.x)
		accel = force / not0(floater.mass)
		floater.delta.x += accel * cos(dir) / explosion.game.fps
		floater.delta.y += accel * sin(dir) / explosion.game.fps
		
	def crash(self, a, b):
		if soundModule:
			setVolume(hitSound.play(), a, b)

		if b.hp > 0: a.takeDamage(b.hp, b)
		if a.hp > 0: b.takeDamage(a.hp, a)

class SolarA1(SolarSystem):
	tinyFighters = []
	maxFighters = 15
	respawnTime = 30
	fightersPerMinute = 2
	def __init__(self, game, player, numPlanets = 10, numStructures = 2):
		SolarSystem.__init__(self, game)
		self.sun = (Sun( game, Vec2d(0,0), radius = 2000, mass = 180000, \
					color = (255, 255, 255), image = None)) # the star
		#place player:
		angle = randint(0,360)
		distanceFromSun = randint(8000, 18000)

		player.pos.x = distanceFromSun * cos(angle)
		player.pos.y = distanceFromSun * sin(angle)
		self.add(self.sun)
		self.name = "Qbert"
		
		#add planets:
		d = 5000
		for i in range(numPlanets):
			angle = randint(0,360)
			distanceFromSun = randint(d, d + 1200)
			color = randint(40,200),randint(40,200),randint(40,200)
			radius = randint(300,700)
			mass = randnorm(radius * 10, 800)
			self.planets.append(Planet(game, Vec2d(distanceFromSun * cos(angle), \
				distanceFromSun * sin(angle)), radius = radius, mass = mass, \
				color = color))
			self.add(self.planets[i])
			d+= 1200

		for i in range(numStructures):
			angle = randint(0,360)
			distanceFromSun = randint(d, d + 2500)
			color = randint(0,100),randint(0,100),randint(0,100)
			radius = randint(100,200)
			self.structures.append(Structure( game, Vec2d(distanceFromSun * cos(angle), \
				distanceFromSun * sin(angle)), color, radius))

				
		for planet in self.planets:
			planet.numShips = 0
			planet.ships = pygame.sprite.Group()
			planet.respawn = 30
			self.add(planet)

		for structure in self.structures:
			print structure.radius
			self.add(structure)

		

		self.fighterTimer = 60
			
	# def update(self):
	# 	SolarSystem.update(self)
	# 	enemy respawning:
		
	# 	#tiny fighters
	# 	if self.fighterTimer <= 0 and len(self.tinyFighters) < self.maxFighters:
	# 		numSpawn = randint(1,3)
	# 		for i in range(numSpawn):
	# 			angle = randint(0,360)
	# 			distance = randint(1000, 4000)
	# 			x = distance * cos(angle) + self.game.player.pos.x
	# 			y = distance * sin(angle) + self.game.player.pos.y
	# 			fighter = TinyFighter(self.game, Vec2d(x, y), self.game.player.delta)
	# 			self.add(fighter)
	# 			self.tinyFighters.append(fighter)					
	# 			self.fighterTimer = 60 / self.fightersPerMinute
	# 	else:
	# 		self.fighterTimer -= 1. / self.game.fps
		
	

	
