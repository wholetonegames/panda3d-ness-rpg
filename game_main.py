from u_fsm import ConfigFSM
from t_engine import TextEngine
from direct.task import Task
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, PandaSystem
from x_game import GameModel
from x_maps import MapsModel
from direct.gui.OnscreenText import OnscreenText, TextNode
from direct.gui.DirectGui import DirectFrame

appName = "This is not Earthbound 64"
loadPrcFileData("",
                """
    window-title {}
    #load-display pandagl
    #win-size 1366 768
    win-size 1280 720
    fullscreen 0
    cursor-hidden 0
    show-frame-rate-meter 0
    model-path $MAIN_DIR/egg/
    framebuffer-multisample 1
    #multisamples 8
    #texture-anisotropic-degree 2
    #textures-auto-power-2 1
    #notify-level-device debug
    #notify-level-device spam
    #want-pstats 1
""".format(appName))


class Main(ShowBase,  ConfigFSM):
    def __init__(self):
        self.loadingText = None
        self.saveFolderPath = './saves/'
        self.appName = appName
        ShowBase.__init__(self)
        self.textEngine = TextEngine(base.messenger.send)
        self.mapData = MapsModel()
        self.gameData = GameModel(self.saveFolderPath)
        ConfigFSM.__init__(self)
        self.disableMouse()
        self.callLoadingScreen()

        self.request("StartMenu")
        # self.request("RPGField")
        # self.request("Cutscene")

    def callLoadingScreen(self):
        self.loadingText = DirectFrame(
            frameSize=(base.a2dLeft, base.a2dRight,
                       base.a2dBottom, base.a2dTop),
            frameColor=(0, 0, 0, 1.0))

        txt = OnscreenText("Loading...", 1, fg=(1, 1, 1, 1), pos=(
            0, 0), align=TextNode.ACenter, scale=.07, mayChange=1)
        txt.reparentTo(self.loadingText)
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()

    def removeLoadingScreen(self):
        if self.loadingText:
            self.loadingText.removeNode()
        self.loadingText = None


game = Main()
game.run()
