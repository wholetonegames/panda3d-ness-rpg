from w_menu_start import StartMenu
from w_menu_load import LoadMenu
from w_menu_option import OptionMenu
from w_menu_config import ConfigMenu
from w_menu_items import ItemMenu
from w_menu_magic import MagicMenu
from w_menu_save import SaveMenu
from w_rpg_fight import RPGFight
from u_imports import ConfigImports
from u_controls import ConfigControls
from direct.fsm.FSM import FSM


class ConfigFSM(FSM, ConfigImports, ConfigControls):
    def __init__(self):
        FSM.__init__(self, "FSM-Game")
        ConfigImports.__init__(self)
        ConfigControls.__init__(self)
        self.defaultTransitions = {
            'StartMenu': ['RPGField', 'LoadMenu', 'Cutscene'],
            'RPGField': ['OptionMenu', 'RPGFight', 'Cutscene'],
            'OptionMenu': ['RPGField', 'ConfigMenu', 'ItemMenu',
                           'StartMenu', 'MagicMenu', 'SaveMenu',
                           'LoadMenu', ],
            'RPGFight': ['RPGField', 'Cutscene', 'StartMenu'],
            'Cutscene': ['RPGField', 'RPGFight'],
            'LoadMenu': ['OptionMenu', 'StartMenu', 'RPGField'],
            'ConfigMenu': ['OptionMenu'],
            'ItemMenu': ['OptionMenu'],
            'MagicMenu': ['OptionMenu'],
            'SaveMenu': ['OptionMenu'],
        }
        self.accept("Back-Field", self.request, ["RPGField"])
        self.accept("Back-Option", self.request, ["OptionMenu"])
        self.accept('Cutscene', self.callScene)
        self.accept('MapReload', self.rpgField.resetMap)

    # FSM ##################################################################

    def enterStartMenu(self):
        self.initController()
        self.startMenu = StartMenu()

        self.accept("Menu-Start", self.startNewGame)
        self.accept("Menu-Load", self.request, ["LoadMenu"])
        self.accept("Menu-Website", self.startMenu.websiteTask)
        self.accept("Menu-Quit", self.userExit)

        taskMgr.add(self.startMenu.readKeys, "readKeysTask")
        base.removeLoadingScreen()

    def exitStartMenu(self):
        self.resetButtons()
        self.ignore("Menu-Start")
        self.ignore("Menu-Load")
        self.ignore("Menu-Website")
        self.ignore("Menu-Quit")

        taskMgr.remove("readKeysTask")
        self.startMenu.quit()
        del self.startMenu

    def enterRPGField(self):
        self.accept("Field-Fight", self.request, ["RPGFight"])
        self.accept("Field-Menu", self.request, ["OptionMenu"])
        taskMgr.add(self.rpgField.moveHero, "moveTask")
        taskMgr.add(self.rpgField.AIUpdate, "AIUpdate")
        self.rpgField.start()
        self.initController()
        base.removeLoadingScreen()

    def exitRPGField(self):
        base.callLoadingScreen()
        self.resetButtons()
        self.ignore("Field-Fight")
        self.ignore("Field-Menu")
        taskMgr.remove("moveTask")
        taskMgr.remove("AIUpdate")
        self.rpgField.stop()

    def enterRPGFight(self):
        self.rpgField.deleteEnemyByIndex()
        # fix enemy data later
        self.rpgFight = RPGFight(
            base.gameData.hero_party, self.enemyData, self.enemy_label)
        self.accept("Fight-Input", self.rpgFight.request, ["SelectInput"])
        self.accept("Fight-Flee", self.request, ["RPGField"])
        self.rpgFight.start()
        self.initController()
        base.removeLoadingScreen()

    def exitRPGFight(self):
        self.disableController()
        base.callLoadingScreen()
        self.resetButtons()
        self.ignore("Fight-Flee")
        taskMgr.remove("readKeysTask")
        self.rpgFight.quit()

    def enterCutscene(self):
        self.disableController()
        self.cutsceneManager.callScene(base.gameData.currentCutsceneName)
        base.removeLoadingScreen()

    def exitCutscene(self):
        base.callLoadingScreen()
        self.resetButtons()
        self.cutsceneManager.quitScene()
        self.initController()

    def enterOptionMenu(self):
        self.optionMenu = OptionMenu()

        self.accept("Option-Items", self.request, ["ItemMenu"])
        self.accept("Option-Magic", self.request, ["MagicMenu"])
        self.accept("Option-Save", self.request, ["SaveMenu"])
        self.accept("Option-Config", self.request, ["ConfigMenu"])
        self.accept("Option-Quit", self.request, ["StartMenu"])
        self.accept("Chara-Add", self.optionMenu.displayCharacterSheet, [1])
        self.accept("Chara-Sub", self.optionMenu.displayCharacterSheet, [-1])

        taskMgr.add(self.optionMenu.readKeys, "readKeysTask")
        base.removeLoadingScreen()

    def exitOptionMenu(self):
        self.resetButtons()

        self.ignore("Option-Items")
        self.ignore("Option-Magic")
        self.ignore("Option-Save")
        self.ignore("Option-Load")
        self.ignore("Option-Config")
        self.ignore("Option-Quit")
        self.ignore("Chara-Add")
        self.ignore("Chara-Sub")

        taskMgr.remove("readKeysTask")
        self.optionMenu.quit()

    def enterLoadMenu(self):
        self.loadMenu = LoadMenu()
        self.accept("Back-Load", self.request, ["StartMenu"])
        taskMgr.add(self.loadMenu.readKeys, "readKeysTask")

    def exitLoadMenu(self):
        self.resetButtons()
        self.ignore("Back-Load")
        taskMgr.remove("readKeysTask")
        self.loadMenu.quit()

    def enterSaveMenu(self):
        self.saveMenu = SaveMenu()
        taskMgr.add(self.saveMenu.readKeys, "readKeysTask")

    def exitSaveMenu(self):
        self.resetButtons()
        taskMgr.remove("readKeysTask")
        self.saveMenu.quit()

    def enterItemMenu(self):
        self.itemMenu = ItemMenu()
        taskMgr.add(self.itemMenu.readKeys, "readKeysTask")

    def exitItemMenu(self):
        self.resetButtons()
        taskMgr.remove("readKeysTask")
        self.itemMenu.quit()

    def enterMagicMenu(self):
        self.magicMenu = MagicMenu()
        self.accept("Chara-Add", self.magicMenu.displayCharacterSheet, [1])
        self.accept("Chara-Sub", self.magicMenu.displayCharacterSheet, [-1])
        taskMgr.add(self.magicMenu.readKeys, "readKeysTask")

    def exitMagicMenu(self):
        self.resetButtons()
        self.ignore("Chara-Add")
        self.ignore("Chara-Sub")
        taskMgr.remove("readKeysTask")
        self.magicMenu.quit()

    def enterConfigMenu(self):
        self.configMenu = ConfigMenu()
        self.accept("Chara-Add", self.configMenu.change_config, [1])
        self.accept("Chara-Sub", self.configMenu.change_config, [-1])
        taskMgr.add(self.configMenu.readKeys, "readKeysTask")

    def exitConfigMenu(self):
        self.resetButtons()
        self.ignore("Chara-Add")
        self.ignore("Chara-Sub")
        taskMgr.remove("readKeysTask")
        self.configMenu.quit()

    # FSM ##################################################################

    def callScene(self, cutsceneName):
        base.gameData.currentCutsceneName = cutsceneName
        self.requestWithFade('Cutscene')

    def requestWithFade(self, stateName):
        self.fadeInOutSequence(self.request, stateName)

    def startNewGame(self):
        base.gameData.resetGameModel()
        # maybe request an opening cutscene etc
        base.messenger.send("MapReload")
        self.request("RPGField")

        # this is needed for cutscenes
        # self.rpgField.stop()
        # self.request("Cutscene")
