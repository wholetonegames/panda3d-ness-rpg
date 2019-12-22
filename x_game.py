from x_save_load import SaveLoadJSON
import os


class GameModel(SaveLoadJSON):
    def __init__(self, saveFolderPath):
        SaveLoadJSON.__init__(self, saveFolderPath)
        self.saveSlotNumbers = (1, 2, 3)
        self.protectedFields.append('saveSlotNumbers')
        self.selectedSaveSlot = 1
        self.protectedFields.append('selectedSaveSlot')
        self.hero_party = []
        self.itemInventory = []
        self.currentMap = ""
        self.heroPos = ""
        self.heroModel = "ness"
        self.previousSavedTime = 0
        # at the end, always
        self.resetGameModel()

    def runManualUpdates(self):
        self.filepath = os.path.dirname(self.filepath) + \
            "/slot{}.txt".format(self.selectedSaveSlot)
        self.totalTimePlayed += (base.elapsedSeconds - self.previousSavedTime)
        self.previousSavedTime = base.elapsedSeconds

    def registerActors(self):
        base.textEngine.registerActor('luc', self.hero_party[0])

        base.textEngine.registerActor('charaA', 'A')
        base.textEngine.registerActor('charaB', 'B')

    def resetGameModel(self):
        self.currentMap = "onett"
        self.currentCutsceneName = 'test'
        self.heroPos = base.mapData.maps[self.currentMap]["startPos"]
        self.totalTimePlayed = 0
        self.textDisplayTime = 2.0
        self.sfx_vol = 1
        self.bgm_vol = 1
        self.hero_party = [{'name': 'Ness',
                            'model': 'ness',
                            'hp': 100, 'max_hp': 100,
                            'level': 1, 'xp': 0,
                            'attack': {'base': 15, 'buffAdd': 0, 'buffMult': 1},
                            'defense': {'base': 5, 'buffAdd': 0, 'buffMult': 1},
                            'speed': {'base': 5, 'buffAdd': 0, 'buffMult': 1},
                            'statusEffect': {'KO': False, 'POISONED': False, 'STUNNED': False, 'CONFUSED': False},
                            'statusImmunity': [],
                            'magic': list(range(1, 21))  # [3],
                            },
                           ]
        self.registerActors()
        self.items = [
            {"id": 1, "amount": 100},
            {"id": 2, "amount": 100},
            {"id": 3, "amount": 100},
            {"id": 4, "amount": 100},
            {"id": 5, "amount": 100},
            {"id": 6, "amount": 100},
            {"id": 7, "amount": 100},
            {"id": 8, "amount": 100},
            {"id": 9, "amount": 100},
            {"id": 10, "amount": 100},
            {"id": 11, "amount": 100},
            {"id": 12, "amount": 100},
            {"id": 13, "amount": 100},
            {"id": 14, "amount": 100},
            {"id": 15, "amount": 100},
            {"id": 16, "amount": 100},
            {"id": 17, "amount": 100},
            {"id": 18, "amount": 100},
            {"id": 19, "amount": 100},
            {"id": 20, "amount": 100},
            {"id": 21, "amount": 100},
            {"id": 22, "amount": 100},
            {"id": 23, "amount": 100},
            {"id": 24, "amount": 100},
            {"id": 25, "amount": 100},
            {"id": 26, "amount": 100}
        ]

        self.flags = {
            "is_uriel_ready": True,
            "is_gabriel_ready": True,
            "is_raphael_ready": True,
            "is_michael_ready": True,
        }
