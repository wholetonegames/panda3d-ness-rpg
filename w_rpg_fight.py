from direct.fsm.FSM import FSM
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from w_rpg_fight_actor import FightActorHero, FightActorEnemy
from w_rpg_fight_input import RPGFightInput
from w_rpg_fight_target import RPGFightTarget
from w_rpg_fight_magic import RPGFightMagic
from w_rpg_fight_item import RPGFightItem
from w_rpg_fight_round import FightRound
from w_gui_dialog import GUIDialog
import y_helpers


class RPGFight(FSM):
    def __init__(self, hero_party, enemyModel, label):
        self.hero_party = hero_party
        self.enemyModel = enemyModel
        self.enemy_party = self.enemyModel.enemy_party(label)
        self.dialogBox = GUIDialog()
        FSM.__init__(self, "FSM-RPGFight")
        self.defaultTransitions = {
            'SelectInput': ['SelectTarget', 'SelectItem', 'SelectMagic', 'ShowAnimation', 'Quit', 'Defend'],
            'SelectTarget': ['SelectInput', 'ShowAnimation', 'Quit'],
            'SelectItem': ['SelectTarget', 'SelectInput', 'Quit'],
            'SelectMagic': ['SelectTarget', 'SelectInput', 'Quit'],
            'ShowAnimation': ['SelectInput', 'Quit'],
            'Defend': ['SelectInput', 'ShowAnimation', 'Quit'],
            'Quit': ['SelectInput']
        }
        self.animationModels = []
        self.initStage()
        self.initHero()
        self.initEnemy()
        self.instructionList = []

        self.request("SelectInput")

    @property
    def itemInventory(self):
        arr = []
        for item in base.gameData.items:
            if not item['amount']:
                continue
            ItemInfo = y_helpers.find_by_id(item['id'], base.itemData.items)
            if 'equips' in ItemInfo:
                continue
            arr.append(ItemInfo)
        return arr

    def initStage(self):
        self.stage = loader.loadModel("battleField")
        self.stage.reparentTo(render)
        cameraPos = self.stage.find("**/cameraPos").getPos()
        self.cameraFocus = self.stage.find("**/cameraFocus").getPos()

        base.camera.setPos(cameraPos)
        base.camera.lookAt(self.cameraFocus)
        lightPos = self.stage.find("**/cameraFocus")
        base.sunNp.setPos(lightPos.getX()-4, lightPos.getY()-4, 50)
        base.sunNp.lookAt(self.cameraFocus)

        self.stage.hide()

    def start(self):
        render.setLight(base.alnp)
        render.setLight(base.sunNp)

        self.stage.show()
        base.messenger.send("playFight")

    def quit(self):
        self.stage.removeNode()
        self.request("Quit")

        render.clearLight()

    def initHero(self):
        for hero in self.hero_party:
            heroIndex = self.hero_party.index(hero)
            heroPos = self.stage.find(
                "**/heroPos{}".format(heroIndex+1)).getPos()
            heroM = FightActorHero(hero, heroPos, self.cameraFocus)
            heroM.reparentTo(self.stage)
            self.animationModels.append(heroM)

        self.heroIndex = 0

    def initEnemy(self):
        for enemy in self.enemy_party:
            enemyIndex = self.enemy_party.index(enemy)
            enemyPos = self.stage.find(
                "**/enemyPos{}".format(enemyIndex+1)).getPos()
            enemyM = FightActorEnemy(enemy, enemyPos, self.cameraFocus)
            enemyM.reparentTo(self.stage)
            self.animationModels.append(enemyM)

    # FSM ##################################################################

    def enterSelectInput(self):
        self.findHero()
        self.rpgFightInput = RPGFightInput(self.hero_party, self.enemy_party)
        self.rpgFightInput.playerInfo(self.heroIndex)
        self.accept("Fight-Attack", self.request, ["SelectTarget"])
        self.accept("Fight-Magic", self.request, ["SelectMagic"])
        self.accept("Fight-Items", self.request, ["SelectItem"])
        self.accept("Fight-Defend", self.request, ["Defend"])
        taskMgr.add(self.rpgFightInput.readKeys, "readKeysTask")
        self.currentInstruction = {}

    def exitSelectInput(self):
        base.resetButtons()
        taskMgr.remove("readKeysTask")
        self.ignore("Fight-Attack")
        self.ignore("Fight-Magic")
        self.ignore("Fight-Items")
        self.ignore("Fight-Defend")
        self.rpgFightInput.quit()

    def enterSelectTarget(self):
        self.rpgFightTarget = RPGFightTarget(self.enemy_party)
        self.manageTasks(self.enemy_party, "Target-{}", self.chooseTarget)
        taskMgr.add(self.rpgFightTarget.readKeys, "readKeysTask")

    def exitSelectTarget(self):
        base.resetButtons()
        taskMgr.remove("readKeysTask")
        self.manageTasks(self.enemy_party, "Target-{}")
        self.rpgFightTarget.quit()

    def enterSelectMagic(self):
        self.rpgFightMagic = RPGFightMagic(
            self.hero_party[self.heroIndex]['magic'])
        self.manageTasks(
            self.hero_party[self.heroIndex]['magic'], "Magic-{}", self.chooseMagic)
        taskMgr.add(self.rpgFightMagic.readKeys, "readKeysTask")

    def exitSelectMagic(self):
        base.resetButtons()
        taskMgr.remove("readKeysTask")
        self.manageTasks(self.hero_party[self.heroIndex]['magic'], "Magic-{}")
        self.rpgFightMagic.quit()
        del self.rpgFightMagic

    def enterSelectItem(self):
        self.rpgFightItem = RPGFightItem(self.itemInventory)
        self.manageTasks(self.itemInventory, "Item-{}", self.chooseItem)
        taskMgr.add(self.rpgFightItem.readKeys, "readKeysTask")

    def exitSelectItem(self):
        base.resetButtons()
        taskMgr.remove("readKeysTask")
        self.manageTasks(self.itemInventory, "Item-{}")
        self.rpgFightItem.quit()

    def enterDefend(self):
        taskMgr.doMethodLater(.1, self.chooseDefense, 'def')

    def exitDefend(self):
        base.resetButtons()
        taskMgr.remove("readKeysTask")

    def enterShowAnimation(self):
        taskMgr.doMethodLater(.1, self.processInstructions, 'instruction')

    def exitShowAnimation(self):
        base.resetButtons()
        self.instructionList = []

    def enterQuit(self):
        pass

    def exitQuit(self):
        base.resetButtons()
        for model in self.animationModels:
            model.request('Quit')

    # FSM ##################################################################

    def manageTasks(self, characterList, eventName, functionName=None):
        for index in range(len(characterList)):
            if functionName:
                self.accept(eventName.format(index), functionName, [index])
            else:
                self.ignore(eventName.format(index))

    def chooseDefense(self, task):
        self.currentInstruction['agent'] = self.hero_party[self.heroIndex]
        self.currentInstruction['type'] = y_helpers.TYPE_DEFENSE
        self.instructionList.append(self.currentInstruction)
        self.nextHero()
        return task.done

    def findHero(self):
        while y_helpers.is_character_KOed(self.hero_party[self.heroIndex]):
            self.heroIndex += 1

    def nextHero(self):
        if self.heroIndex < len(self.hero_party) - 1:
            self.heroIndex += 1
            if y_helpers.is_character_KOed(self.hero_party[self.heroIndex]):
                self.nextHero()
            else:
                self.request("SelectInput")
        else:
            self.heroIndex = 0
            self.request("ShowAnimation")

    def chooseTarget(self, enemyIndex):
        self.currentInstruction['agent'] = self.hero_party[self.heroIndex]
        self.currentInstruction['target'] = [self.enemy_party[enemyIndex]]
        if not 'type' in self.currentInstruction.keys():
            self.currentInstruction['type'] = y_helpers.TYPE_ATTACK

        self.instructionList.append(self.currentInstruction)
        self.nextHero()

    def chooseMagic(self, index):
        magicIndex = self.hero_party[self.heroIndex]['magic'][index]
        magic = y_helpers.find_by_id(magicIndex, base.magicData.items)
        self.currentInstruction['type'] = y_helpers.TYPE_MAGIC
        self.currentInstruction['spell'] = magic
        self.request('SelectTarget')

    def chooseItem(self, index):
        item = self.itemInventory[index]
        self.currentInstruction['type'] = y_helpers.TYPE_ITEM
        self.currentInstruction['item'] = item
        self.currentInstruction['itemIndex'] = y_helpers.find_index_by_id(
            item['id'], base.gameData.items)
        self.request('SelectTarget')

    def processInstructions(self, task):
        # this should be this.fight_round
        fight_round = FightRound(self.hero_party, self.enemy_party,
                                 base.gameData.items, base.magicData, self.instructionList)
        seq = Sequence()
        while True:
            roundOutcome = fight_round.round_fight()
            self.chooseAnimation(fight_round, seq, roundOutcome)
            if fight_round.is_last_turn_in_round or fight_round.is_battle_over:
                break
            fight_round.next_turn()
        seq.append(Func(self.animationWrapUp, fight_round))
        seq.start()
        return task.done

    def chooseAnimation(self, fight_round, seq, messages):
        hasAgent = self.animateAgent(fight_round, seq)
        if not hasAgent:
            return
        self.animateTarget(fight_round, seq, messages)

    def showTargetMessages(self, seq, messages, index):
        seq.append(Func(self.dialogBox.showMessage, messages[index]))
        seq.append(Wait(base.gameData.textDisplayTime))
        seq.append(Func(self.dialogBox.hide))

    def animateTarget(self, fight_round, seq, messages):
        turn = fight_round.current_turn
        if 'target' in turn:
            index = 0
            for target in turn['target']:
                modelTarget = y_helpers.find_by_name(self.animationModels,
                                                     target['name'])
                seq.append(Wait(base.gameData.textDisplayTime / 4))
                if 'collapsed' in messages[index]:
                    seq.append(Func(modelTarget.request, 'KOed'))
                elif modelTarget.state != 'Defending':
                    if not modelTarget.name in messages[index]:
                        modelTarget = self.getTargetFromMessage(
                            messages[index])
                    seq.append(Func(modelTarget.request, 'Attacked'))
                seq.append(Wait(base.gameData.textDisplayTime / 2))
                self.showTargetMessages(seq, messages, index)
                index += 1

    def getTargetFromMessage(self, message):
        mList = message.split(' ')
        return y_helpers.find_by_name(self.animationModels, mList[0])

    def animateAgent(self, fight_round, seq):
        turn = fight_round.current_turn
        modelAgent = y_helpers.find_by_name(self.animationModels,
                                            turn['agent']['name'])
        if modelAgent:
            if y_helpers.is_character_KOed(modelAgent.fightObj):
                return False
            seq.append(Func(modelAgent.request, turn['type']))
        return True

    def animationWrapUp(self, fight_round):
        if fight_round.is_battle_over:
            self.play_spoils(fight_round)
        else:
            for model in self.animationModels:
                model.initAnimation()
            self.request('SelectInput')

    def play_spoils(self, fight_round):
        seq = Sequence()
        for message in fight_round.battle_spoils_messages():
            seq.append(Func(self.dialogBox.showMessage, message))
            seq.append(Wait(base.gameData.textDisplayTime))
            seq.append(Func(self.dialogBox.hide))
        seq.append(Func(self.postOutcomeAction, fight_round.outcome))
        seq.start()

    def postOutcomeAction(self, outcome):
        if outcome == y_helpers.OUTCOME_VICTORY:
            base.fadeInOutSequence(base.messenger.send, 'Fight-Flee')
        else:
            # we need a proper game over state
            base.requestWithFade('StartMenu')
