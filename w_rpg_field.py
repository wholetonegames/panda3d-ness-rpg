from w_i_stage import IStage


class RPGField(IStage):
    def __init__(self):
        IStage.__init__(self)
        self.setup()
        self.setHeroCollision()
        self.stop()
        self.enemyIndexToBeDeleted = -1
        self.previousIntoEvent = ''

    def intoEvent(self, entry):
        if not entry.hasInto():
            return
        intoName = entry.getIntoNode().getName()
        if self.previousIntoEvent == intoName:
            return

        self.previousIntoEvent = intoName

        if "enemy" in intoName:
            self.intoEnemy(intoName, entry)
        elif "boss" in intoName:
            self.intoBoss(intoName, entry)
        elif "door" in intoName:
            self.intoDoor(intoName)
        elif "cutscene" in intoName:
            self.intoCutscene(intoName)
        elif "npc" in intoName:
            self.intoNPC(intoName)

    def intoDoor(self, intoName):
        base.disableController()
        oldMap = base.gameData.currentMap
        if 'pattern' in base.mapData.maps[oldMap]:
            door_index = int(intoName.split('_')[1])
            mapName = base.mapData.maps[oldMap]['doorList'][door_index]
        else:
            mapName = base.mapData.maps[oldMap][intoName]
        base.gameData.currentMap = mapName['map']
        base.gameData.heroPos = mapName['pos']
        if "model" in mapName:
            base.gameData.heroModel = mapName['model']
        self.changeMap()

    def intoEnemy(self, intoName, entry):
        fromName = entry.getFromNode().getName()
        if not "hero" in fromName:
            return
        base.disableController()
        self.enemyIndexToBeDeleted = self.getIndexFromEvent(intoName)
        enemy = base.mapData.maps[base.gameData.currentMap]["enemyList"][self.enemyIndexToBeDeleted]
        base.enemy_label = enemy['label']
        self.enemyActors[self.enemyIndexToBeDeleted].request('Hide')
        base.fadeInOutSequence(base.messenger.send, "Field-Fight")
        
    def intoBoss(self, intoName, entry):
        pass
        fromName = entry.getFromNode().getName()
        if not "hero" in fromName:
            return
        base.disableController()
        boss_index = self.getIndexFromEvent(intoName)
        boss = base.mapData.maps[base.gameData.currentMap]["enemyList"][boss_index]
        base.enemy_label = boss['label']
        base.gameData.flags[boss['flag']] = not base.gameData.flags[boss['flag']]
        base.fadeInOutSequence(base.messenger.send, "Field-Fight")

    def intoCutscene(self, intoName):
        base.disableController()
        base.gameData.heroPos = base.mapData.maps[base.gameData.currentMap][intoName]['pos']
        base.callScene(
            base.mapData.maps[base.gameData.currentMap][intoName]['scene'])

    def intoNPC(self, intoName):
        npcIndex = self.getIndexFromEvent(intoName)
        npc = base.mapData.maps[base.gameData.currentMap]["npcList"][npcIndex]
        if not 'label' in npc:
            return
        self.dialogBox.setLabel(npc['label'])

    def cancelCommand(self):
        base.messenger.send("Field-Menu")

    def getIndexFromEvent(self, eventName):
        l = eventName.split("_")
        return int(l[1])

    def deleteEnemyByIndex(self):
        if self.enemyIndexToBeDeleted <= -1:
            return
        self.enemyActors[self.enemyIndexToBeDeleted].request('DeleteActor')
        # can't remove enemy with del as not to disturb indexes
        self.enemyActors[self.enemyIndexToBeDeleted] = None
        self.enemyIndexToBeDeleted = -1
