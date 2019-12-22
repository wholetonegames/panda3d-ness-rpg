import abc
from panda3d.core import (
    CollisionHandlerQueue,
    CollisionRay,
    CollideMask,
    CollisionHandlerPusher,
    CollisionNode,
    CollisionSphere,
    CollisionBox)
from direct.actor.Actor import Actor
from panda3d.ai import AICharacter
from w_gui_dialog import GUIDialog
from w_rpg_field_actor import FieldActor
from y_better_dice import BetterThanDice
from w_rpg_field_grid import StageGrid


class IStage(metaclass=abc.ABCMeta):
    def __init__(self):
        self.charHeading = {"up": 180, "down": 0, "left": 90, "right": 90}
        self.pusher = base.pusher
        self.heroGroundHandler = CollisionHandlerQueue()
        self.dialogBox = GUIDialog()
        self.stage = None
        self.hero = None
        self.enemyActors = []
        self.npcActors = []
        self.bossActors = []

    def initStage(self):
        if self.stage:
            self.stage.removeNode()
        this_map = base.mapData.maps[base.gameData.currentMap]
        self.stage = loader.loadModel(this_map['model'])
        if "pattern" in this_map:
            self.stage_grid = StageGrid(
                this_map['pattern'], self.stage, this_map['blockTypes'])
            self.startPos = self.stage_grid.startPosList[base.gameData.heroPos]
        else:
            self.startPos = self.stage.find(
                "**/" + base.gameData.heroPos).getPos()
        self.stage.reparentTo(render)
        self.stage.hide()

    def setup(self):
        self.initStage()
        self.initHero()
        self.initEnemy()
        self.initBoss()
        self.initNPC()

    def initHero(self):
        self.hero = loader.loadModel("charaRoot")
        self.hero.reparentTo(self.stage)
        model = base.gameData.heroModel
        self.heroArmature = Actor(
            "{}".format(model), {
                "idle": "{}-idle".format(model),
                "walk": "{}-run".format(model)
            })
        self.heroArmature.reparentTo(self.hero)
        self.hero.setPos(self.startPos)
        cNode = CollisionNode('hero')
        cNode.addSolid(CollisionSphere(0, 0, 1.5, 1))
        heroCollision = self.hero.attachNewNode(cNode)
        #########################################################
        # heroCollision.show()

        self.pusher.addCollider(
            heroCollision, self.hero, base.drive.node())
        base.cTrav.addCollider(heroCollision, self.pusher)

        heroGroundRay = CollisionRay()
        heroGroundRay.setOrigin(0, 0, 9)
        heroGroundRay.setDirection(0, 0, -1)
        heroGroundCol = CollisionNode('heroRay')
        heroGroundCol.addSolid(heroGroundRay)
        heroGroundCol.setFromCollideMask(CollideMask.bit(0))
        heroGroundCol.setIntoCollideMask(CollideMask.allOff())
        heroGroundColNp = self.hero.attachNewNode(heroGroundCol)
        #########################################################
        # heroGroundColNp.show()

        base.cTrav.addCollider(heroGroundColNp, self.heroGroundHandler)
        self.controlCamera()

    def fixActorsHPR(self):
        for e in self.enemyActors:
            if not e:
                continue
            h, p, r = e.actor.getHpr()
            e.actor.setHpr(h, 0, 0)

    def AIUpdate(self, task):
        base.AIworld.update()
        self.fixActorsHPR()
        return task.cont

    def initEnemy(self):
        this_map = base.mapData.maps[base.gameData.currentMap]
        if not "enemyList" in this_map:
            return
        enemyNumber = len(this_map["enemyList"])
        if enemyNumber <= 0:
            return
        self.enemyActors = []
        die = BetterThanDice(2)
        for enemyIndex in list(range(0, enemyNumber)):
            enemyModel = this_map["enemyList"][enemyIndex]['model']
            fa = FieldActor('enemy', enemyIndex, enemyModel,
                            self.stage, self.enemyActors, self.hero)
            if die.getValue() == 0:
                fa.request('Pursue')
            else:
                fa.request('Wander')

    def initBoss(self):
        this_map = base.mapData.maps[base.gameData.currentMap]
        if not "bossList" in this_map:
            return
        bossNumber = len(this_map["bossList"])
        if bossNumber <= 0:
            return
        self.bossActors = []
        for bossIndex in list(range(0, bossNumber)):
            if not base.gameData.flags[this_map["bossList"][bossIndex]['flag']]:
                continue
            bossModel = this_map["bossList"][bossIndex]['model']
            fa = FieldActor('boss', bossIndex, bossModel,
                            self.stage, self.bossActors, self.hero)

    def initNPC(self):
        this_map = base.mapData.maps[base.gameData.currentMap]
        if not "npcList" in this_map:
            return
        npcNumber = len(this_map["npcList"])
        if npcNumber == 0:
            return
        self.npcActors = []
        for npcIndex in list(range(0, npcNumber)):
            npcModel = this_map["npcList"][npcIndex]['model']
            fa = FieldActor('npc', npcIndex, npcModel,
                            self.stage, self.npcActors, self.hero)
            fa.request('Idle')

    def controlCamera(self):
        base.camera.setPos(self.hero.getX(), self.hero.getY() - 50, 55)
        base.camera.lookAt(self.heroArmature)

        base.sunNp.setPos(self.hero.getX()-4, self.hero.getY()-4, 50)
        base.sunNp.lookAt(self.hero)

    def moveHero(self, task):
        animName = self.heroArmature.getCurrentAnim()

        if self.dialogBox.isShowing:
            if animName != "idle":
                self.heroArmature.loop("idle")
            self.controlDialogBox()
            return task.cont

        keysPressed = sum(base.directionMap.values())

        if keysPressed == 0:
            if animName != "idle":
                self.heroArmature.loop("idle")

            if base.commandMap["confirm"]:
                pass
            elif base.commandMap["cancel"]:
                self.cancelCommand()

            base.resetButtons()
            return task.cont

        self.heroHandleFloor()
        self.heroCalculateDisplacement()
        self.heroHeading(keysPressed)
        self.controlCamera()

        if animName != "walk":
            self.heroArmature.loop("walk")

        return task.cont

    def heroCalculateDisplacement(self):

        dt = globalClock.getDt()

        xSpeed = 0.0
        ySpeed = 0.0
        speed = 25
        if base.directionMap["left"]:
            xSpeed -= speed
        elif base.directionMap["right"]:
            xSpeed += speed

        if base.directionMap["up"]:
            ySpeed += speed
        elif base.directionMap["down"]:
            ySpeed -= speed

        self.hero.setX(self.hero, xSpeed * dt)
        self.hero.setY(self.hero, ySpeed * dt)

    def heroHandleFloor(self):
        entries = list(self.heroGroundHandler.getEntries())
        entries.sort(key=lambda x: x.getSurfacePoint(render).getZ())

        if len(entries) > 0 and entries[0].getIntoNode().getName() == "floor":
            self.hero.setZ(entries[0].getSurfacePoint(render).getZ())

    def controlDialogBox(self):
        if self.dialogBox.isChoices:
            pass
        else:
            if base.commandMap["confirm"] or base.commandMap["cancel"]:
                self.dialogBox.next()
                base.resetButtons()

    def heroHeading(self, keysPressed=None):
        if not keysPressed:
            return
        heading, pitch, roll = self.heroArmature.getHpr()

        sumAngles = 0

        for key, value in base.directionMap.items():
            if value:
                sumAngles += self.charHeading[key]

        direction = -1 if base.directionMap["left"] else 1

        heading = (sumAngles * direction) / keysPressed

        self.heroArmature.setHpr(heading, pitch, roll)

    def setHeroCollision(self):
        inEvent = "{}-into-{}".format('hero', 'world')
        self.pusher.addInPattern(inEvent)
        base.accept(inEvent, self.intoEvent)

        # againEvent = "{}-again-{}".format(enemyColName, heroColName)
        # self.pusher.addAgainPattern(againEvent)
        # base.accept(againEvent, self.printAgain)

        # outEvent = "{}-out-{}".format(enemyColName, heroColName)
        # self.pusher.addOutPattern(outEvent)
        # base.accept(outEvent, self.printOut)

    def changeMap(self):
        base.callLoadingScreen()
        self.resetMap()

    def resetMap(self):
        self.setup()
        self.start()
        base.initController()

    def start(self):
        render.setLight(base.alnp)
        render.setLight(base.sunNp)

        self.controlCamera()

        self.stage.show()
        self.hero.show()
        for enemy in self.enemyActors:
            if enemy:
                enemy.request('Show')
        for boss in self.bossActors:
            if boss:
                boss.request('Show')
        for npc in self.npcActors:
            npc.request('Show')
        # change how to play different music later
        base.messenger.send("playMap")
        base.removeLoadingScreen()

    def stop(self):
        self.stage.hide()
        self.hero.hide()
        for enemy in self.enemyActors:
            if enemy:
                enemy.request('Hide')
        for boss in self.bossActors:
            if boss:
                boss.request('Hide')
        for npc in self.npcActors:
            npc.request('Hide')
        render.clearLight()

    def quit(self):
        self.stage.removeNode()
        self.dialogBox.removeNode()

    @abc.abstractmethod
    def cancelCommand(self):
        raise NotImplementedError('subclass must define this method')

    @abc.abstractmethod
    def intoEvent(self, entry):
        raise NotImplementedError('subclass must define this method')
