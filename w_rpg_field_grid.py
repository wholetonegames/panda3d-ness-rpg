from panda3d.core import (
    NodePath,
    PandaNode)


class StageGrid:
    START_POS = '*'
    DOOR_LIST = ['N', 'E', 'W', 'S']
    NPC = 'n'
    ENEMY = 'e'
    BOSS = 'b'

    def __init__(self, map_str, stage, blockTypes):
        self.stage = stage
        self.door_index = 0
        self.npc_index = 0
        self.enemy_index = 0
        self.boss_index = 0
        self.rawList = map_str
        self.startPosList = []
        self.optimize = NodePath(PandaNode("optimization node"))
        self.blockTypes = blockTypes
        self.loadBlocks()
        self.optimizeGeometry()

    def loadBlocks(self):
        index = 0
        for blockKey in self.rawList:
            block = self.blockTypes[blockKey]
            if not block:
                index += 1
                continue
            blockModel = base.loader.loadModel("{}".format(block))

            index_str = str(index).zfill(5)
            blockName = self.stage.find(
                '**/block.{}'.format(index_str))
            blockPos = blockName.getPos()
            blockModel.setPos(blockPos)
            if blockKey == self.START_POS:
                self.startPosList.append(blockPos)
            elif blockKey in self.DOOR_LIST:
                self.addDoor(blockModel)
            elif blockKey == self.NPC:
                self.addNPC(blockName)
            elif blockKey == self.ENEMY:
                self.addEnemy(blockName)
            elif blockKey == self.BOSS:
                self.addBoss(blockName)
            else:
                blockModel.reparentTo(self.optimize)
                index += 1
                continue

            blockModel.reparentTo(self.stage)
            index += 1

    def addBoss(self, blockName):
        blockName.setName('boss_{}'.format(self.boss_index))
        self.boss_index += 1

    def addEnemy(self, blockName):
        blockName.setName('enemy_{}'.format(self.enemy_index))
        self.enemy_index += 1

    def addNPC(self, blockName):
        blockName.setName('npc_{}'.format(self.npc_index))
        self.npc_index += 1

    def addDoor(self, blockModel):
        doorBlock = blockModel.find('**/door')
        doorBlock.setName('door_{}'.format(self.door_index))
        self.door_index += 1

    def optimizeGeometry(self):
        self.optimize.flattenMedium()
        self.optimize.reparentTo(self.stage)
