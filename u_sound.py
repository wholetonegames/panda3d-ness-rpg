class ConfigSound:
    def __init__(self):
        self.sfxClick = base.loader.loadSfx("sfx/click.wav")
        self.sfxCancel = base.loader.loadSfx("sfx/item.wav")

        self.bgmFight = base.loader.loadMusic("bgm/final.ogg")
        self.bgmMap = base.loader.loadMusic("bgm/intro.ogg")

        self.musicList = [self.bgmFight,
                          self.bgmMap]

        # base.accept("playConfirm", play_sound, [self.sfxClick])
        # base.accept("playCancel", play_sound, [self.sfxCancel])

        # base.accept("playMap", self.playMusic, [1])
        # base.accept("playFight", self.playMusic, [0])

    def playMusic(self, index):
        music = self.musicList[index]
        music.setVolume(base.gameData.bgm_vol)
        music.setLoop(True)
        music.play()

    def play_sound(self, sound):
        sound.setVolume(base.gameData.sfx_vol)
        sound.play()
