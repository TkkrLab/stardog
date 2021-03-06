#tinyFighter.py


from utils import *
from spaceship import *
from parts import *
from scripts import *
import stardog
from adjectives import *

class TinyFighter(Ship):
	strafeRadius = 100
	planet = None
	stage = 0
	timeOut = 30
	level = .5
	
	def __init__(self, game, pos, delta, color = (70, 180,0)):
		pass
		# self.target = game.player
		# self.circling = False
		# Ship.__init__(self, game, pos, delta, 
		# 				script = TinyFighterScript(game), color = color)
		# self.baseBonuses['damageBonus'] = .5
		# self.addPart(Drone(game))
		# self.energy = self.maxEnergy
		# self.inventory.append(randItem(self.game, self.level))


class TinyFighterScript(AIScript):
	"""a script for tiny fighters."""
	swarmRadius = 280
	retreatRadius = 300
	acceptableError = 8
	shootingRange = 280
	interceptSpeed = 200
	
	def update(self, ship):
		pass
		# target = ship.target
		# if self.game.debug: print ship.stage
		# if ship.stage == 0:
		# 	dx = target.delta.x - ship.delta.x
		# 	dy = target.delta.y - ship.delta.y
		# 	dir = atan2(dy, dx)
		# 	if self.turn(ship, dir):
		# 		ship.forward()
		# 	if -50 < dx < 50 and -50 < dy < 50:
		# 		ship.stage = 1
		# if ship.stage == 1:
		# 	if ship.timeOut <= 0:
		# 		ship.stage = 0
		# 	ship.timeOut -= 1. / ship.game.fps
		# 	speed = self.relativeSpeed(ship, target)
		# 	accel = ship.forwardThrust / ship.mass
		# 	distance = dist(ship.pos.x, ship.pos.y, target.pos.x, target.pos.y) - self.swarmRadius
		# 	turnTime = ship.moment / ship.torque * 180
		# 	if speed > - self.interceptSpeed:
		# 		if self.turnTowards(ship, target):
		# 			ship.forward()
		# 	# elif speed < - self.interceptSpeed:
		# 		# if self.turnTowards(ship, target, 180):
		# 			# ship.forward()
		# 	if distance <= self.shootingRange:
		# 			ship.shoot()
		# 	if distance <= self.retreatRadius - self.swarmRadius:
		# 		ship.stage = 2
		# if ship.stage == 2:
		# 	distance = dist(ship.pos.x, ship.pos.y, target.pos.x, target.pos.y)
		# 	if distance < self.retreatRadius:
		# 		if self.turnTowards(ship, target, 180):
		# 			ship.forward()
		# 	if distance > self.swarmRadius:
		# 		ship.stage = 0
					
