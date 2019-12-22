from direct.fsm.FSM import FSM
from direct.actor.Actor import Actor
import y_helpers


class FightActor(FSM):
    def __init__(self, fightObj, position, lookAtPosition):
        self.fightObj = fightObj
        self.name = fightObj['name']
        self.modelName = fightObj['model']
        self.pos = position
        self.lookAt = lookAtPosition
        FSM.__init__(self, "FSM-FightActor-{}".format(self.name))
        self.actor = Actor("{}".format(self.modelName), {"idle": "{}-battleIdle".format(self.modelName),
                                                         "strike": "{}-strike".format(self.modelName),
                                                         "defend": "{}-defend".format(self.modelName),
                                                         "blowback": "{}-blowback".format(self.modelName)})
        self.actor.setPos(self.pos)
        self.lookAtFix()
        self.initAnimation()

    def initAnimation(self):
        if y_helpers.is_character_KOed(self.fightObj):
            self.request('KOed')
        else:
            self.request('Idle')

    def lookAtFix(self):
        # heading to face opponent with a small hack
        # ths is due to how models are best rendered in blender
        self.actor.headsUp(self.lookAt)
        self.actor.setH(self.actor.getH()-180)

    def reparentTo(self, container):
        self.actor.reparentTo(container)

    # FSM ##################################################################
    def enterIdle(self):
        taskMgr.remove('check-{}'.format(self.modelName))
        self.actor.loop('idle')

    def enterAttacking(self):
        self.actor.play('strike')
        taskMgr.add(self.checkIfEnded, 'check-{}'.format(self.modelName))

    def enterItem(self):
        self.actor.play('strike')
        taskMgr.add(self.checkIfEnded, 'check-{}'.format(self.modelName))

    def enterMagic(self):
        self.actor.play('strike')
        taskMgr.add(self.checkIfEnded, 'check-{}'.format(self.modelName))

    def enterPoison(self):
        self.actor.play('strike')
        taskMgr.add(self.checkIfEnded, 'check-{}'.format(self.modelName))

    def enterAttacked(self):
        self.actor.play('blowback')
        taskMgr.add(self.checkIfEnded, 'check-{}'.format(self.modelName))

    def enterDefending(self):
        self.actor.loop('defend')

    def enterQuit(self):
        taskMgr.remove('check-{}'.format(self.modelName))

    # FSM ##################################################################

    def checkIfEnded(self, task):
        animationName = self.actor.getCurrentAnim()
        if animationName:
            return task.cont
        self.initAnimation()
        return task.done


class FightActorEnemy(FightActor):
    def __init__(self, fightObj, position, lookAtPosition):
        FightActor.__init__(self, fightObj, position, lookAtPosition)

    def enterKOed(self):
        self.actor.hide()


class FightActorHero(FightActor):
    def __init__(self, fightObj, position, lookAtPosition):
        FightActor.__init__(self, fightObj, position, lookAtPosition)

    def enterKOed(self):
        self.actor.setH(180)
