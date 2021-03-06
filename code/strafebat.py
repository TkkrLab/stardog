#strafebat.py

from utils import *
from spaceship import *
from parts import *
from scripts import *
import stardog
from adjectives import *

class Strafebat(Ship):
	strafeRadius = 100
	planet = None
	level = 3
	
	def __init__(self, universe, pos, color, name):
		roll = rand()
		self.target = universe.curSystem.player
		self.universe = universe
		self.circling = False
		Ship.__init__(self, universe.game, pos, Vec2d(0,0), color = color, name=name)
		self.script = StrafebatScript(universe.game)
		self.baseBonuses['damageBonus'] = .5
		cockpit =StrafebatCockpit(universe.game)
		gyro = Gyro(universe.game)
		gun = StrafebatCannon(universe.game)
		quarters = Quarters(universe.game)
		engine = Engine(universe.game)
		generator = Generator(universe.game)
		battery = Battery(universe.game)
		shield = Shield(universe.game)
		rCannon = RightCannon(universe.game)
		lCannon = LeftCannon(universe.game)
		interconnect = Interconnect(universe.game)
		missilelaunch = MissileLauncher(universe.game)
		for part in [cockpit, gyro, gun, engine, generator, battery, shield, 
						rCannon, lCannon, quarters, interconnect]:
			if rand() > .8:
				addAdjective(part)
				if rand() > .6:
					addAdjective(part)
			part.color = color
		self.addPart(cockpit)
		cockpit.addPart(gun, 0)
		cockpit.addPart(gyro, 2)
		gyro.addPart(engine, 1)
		gyro.addPart(generator, 0)
		if .9 < roll:
			generator.addPart(battery, 0)
			gyro.addPart(shield, 2)
		else: 
			gyro.addPart(battery, 2)
		if .8 < roll < .9:
			generator.addPart(rCannon, 0)
		if .7 < roll < .8:
			battery.addPart(lCannon, 0)
		if .6 < roll < .7:
			battery.addPart(quarters, 0)
		if .5 < roll < .6:
			battery.addPart(interconnect, 0)
			interconnect.addPart(missilelaunch, 2)
			self.energy = self.maxEnergy


class StrafebatScript(AIScript):
	"""A scripts with basic physics calculation functions."""
	interceptSpeed = 100.
	returnSpeed = 50.
	acceptableError = 2
	sensorRange = 10000
	shootingRange = 400
	
	def update(self, ship):
		# if too close to planet
		if dist2(ship.planet, ship) < (300 + ship.planet.radius) ** 2:
			if self.turnTowards(ship, ship.planet, 180):
				ship.forward()# move away from planet.
				return
				
		# find closest ship:
		ships = ship.universe.curSystem.ships.sprites()
		target, distance2 = self.closestShip(ship, ships)
		
		if not target:# no target
			self.intercept(ship, ship.planet, self.returnSpeed)
			return
		
		if distance2 < self.shootingRange ** 2 \
		and ship.guns: # within range.
			self.interceptShot(ship, target)
			return
			
		self.intercept(ship, target, self.interceptSpeed)
			
	def closestShip(self, ship, ships):
		"""finds the closest ship not-friendly to this one."""
		target = None
		distance2 = self.sensorRange ** 2
		for ship2 in ships:
			tmp = dist2(ship2, ship)
			if tmp < distance2 \
			and ship2 != ship \
			and (not isinstance(ship2, Strafebat) \
				or ship2.planet != ship.planet):
					distance2 = tmp
					target = ship2
		return target, distance2
		
class StrafebatCockpit(Cockpit):
	pass
