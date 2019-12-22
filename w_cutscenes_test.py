from w_i_stage import IStage
from direct.interval.IntervalGlobal import Sequence, Func, Wait


class CutsceneTest(IStage):
    def __init__(self):
        IStage.__init__(self)

    def setup(self):
        self.previousMap = base.gameData.currentMap
        base.gameData.currentMap = 'city'
        self.previousPos = base.gameData.heroPos
        base.gameData.heroPos = 'startPos'
        self.initStage()
        self.initHero()
        taskMgr.add(self.moveHero, "moveTask")
        self.start()
        self.animate()

    def animate(self):
        seq = Sequence(
            Func(self.heroNorth),
            Wait(2.0),
            Func(self.heroStop),
            Wait(1.0),
            Func(base.requestWithFade, 'RPGField')
        )
        seq.start()

    def heroNorth(self):
        base.directionMap["up"] = True

    def heroStop(self):
        base.directionMap["up"] = False

    def quit(self):
        render.clearLight()
        taskMgr.remove("moveTask")
        self.stage.removeNode()
        base.gameData.currentMap = self.previousMap
        base.gameData.heroPos = self.previousPos

    def cancelCommand(self):
        pass

    def intoEvent(self, entry):
        pass
