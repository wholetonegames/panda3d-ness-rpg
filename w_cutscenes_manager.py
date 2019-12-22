from w_cutscenes_test import CutsceneTest

class CutsceneManager:
    def __init__(self):
        self.currentCutscene = None
        self.sceneTest = CutsceneTest()
        self.sceneDict = {'test': self.sceneTest}

    def callScene(self, key):
        if key in self.sceneDict:
            self.currentCutscene = self.sceneDict[key]
            self.currentCutscene.setup()

    def quitScene(self):
        self.currentCutscene.quit()