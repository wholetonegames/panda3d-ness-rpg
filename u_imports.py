from w_rpg_field import RPGField
from x_enemy import EnemyModel
from x_magic import MagicModel
from x_item import ItemModel
from u_sound import ConfigSound
from w_cutscenes_manager import CutsceneManager
from u_render import ConfigRender
from panda3d.ai import AIWorld
from panda3d.core import (
    PandaSystem,
    CollisionTraverser,
    CollisionHandlerQueue,
    CollisionHandlerPusher,
    loadPrcFileData,
    VirtualFileSystem)
import y_md5_check
from panda3d.core import Filename


class ConfigImports(ConfigRender):
    def __init__(self):
        # self.load_assets()
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()
        base.groundHandler = CollisionHandlerQueue()
        self.AIworld = AIWorld(render)
        ConfigRender.__init__(self)

        self.elapsedSeconds = 0
        self.sound = ConfigSound()
        self.rpgField = RPGField()
        self.enemyData = EnemyModel()
        self.itemData = ItemModel()
        self.magicData = MagicModel()
        self.cutsceneManager = CutsceneManager()
        # print(PandaSystem.getVersionString())
        self.load_fonts()

        # this needs to be called only when game starts
        taskMgr.add(self.updateTime, 'updateTime')
        # before starting a new game
        # taskMgr.remove('updateTime')

    def userExit(self):
        quit()

    def updateTime(self, task):
        self.elapsedSeconds = int(globalClock.getFrameTime())
        return task.cont

    def load_assets(self):
        filename = "assets.mf"
        correct_md5 = '9f733c91cc681a1d1c8108d238a0a50b'
        read_md5 = y_md5_check.md5_sum(filename)
        assert read_md5 == correct_md5
        vfs = VirtualFileSystem.getGlobalPtr()
        if vfs.mount(filename, ".", VirtualFileSystem.MFReadOnly):
            print('mounted')

    def load_fonts(self):
        self.font_title = base.loader.loadFont('EarthBound.ttf')
        self.font_title.setPixelsPerUnit(80)
