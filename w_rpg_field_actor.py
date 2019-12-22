from panda3d.core import (
    CollisionHandlerQueue,
    CollisionRay,
    CollideMask,
    CollisionHandlerPusher,
    CollisionNode,
    CollisionSphere,
    CollisionBox)
from direct.fsm.FSM import FSM
from direct.actor.Actor import Actor
from panda3d.ai import AICharacter


class FieldActor(FSM):
    def __init__(self, name, indexNumber, modelName, stage, actorsList, hero):
        self.indexNumber = indexNumber
        self.modelName = modelName
        self.stage = stage
        self.name = name
        self.actorsList = actorsList
        self.hero = hero
        FSM.__init__(
            self, "FSM-FieldActor-{}_{}".format(self.name, self.indexNumber))
        self.initActor()

    def initActor(self):
        faEmpty = self.stage.find(
            "**/{}_{}".format(self.name, self.indexNumber))
        faPos = faEmpty.getPos()
        self.actor = Actor("{}".format(self.modelName), {"idle": "{}-idle".format(self.modelName),
                                                         "walk": "{}-walk".format(self.modelName)})
        self.actor.reparentTo(self.stage)
        self.actor.setPos(faPos)

        cNode = CollisionNode("{}_{}".format(self.name, self.indexNumber))
        cNode.addSolid(CollisionBox(0, 1.5, 1.5, 1))
        faCollision = self.actor.attachNewNode(cNode)
        #####################################################
        # faCollision.show()
        #####################################################
        base.pusher.addCollider(
            faCollision, self.actor, base.drive.node())
        base.cTrav.addCollider(faCollision, base.pusher)
        self.actorsList.append(self)

        AIchar = AICharacter("{}_{}".format(
            self.name, self.indexNumber), self.actor, 100, 0.05, 5)
        base.AIworld.addAiChar(AIchar)
        self.AIbehaviors = AIchar.getAiBehaviors()

    # FSM ##################################################################
    def enterIdle(self):
        self.actor.loop('idle')

    def enterWander(self):
        self.actor.loop('walk')
        self.AIbehaviors.wander(5, 0, 10, 1.0)

    def enterPursue(self):
        self.actor.loop('walk')
        self.AIbehaviors.pursue(self.hero)

    def enterHide(self):
        self.actor.hide()

    def enterShow(self):
        self.actor.show()

    def enterDeleteActor(self):
        self.actor.delete()

    # FSM ##################################################################
