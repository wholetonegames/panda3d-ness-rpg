from setuptools import setup

setup(
    name="Earthbound_64",
    # install_requires=[
    #       'webbrowser', 'direct.fsm.FSM',
    #   ],
    options = {
        'build_apps': {
            'platforms': [
                'win_amd64',
                'win32',
             ],
            # 'include_modules': {
            #     'Earthbound_64': ['webbrowser'],
            # },
            'include_patterns': [
                # '**/*.mf',
                '**/*.ogg',
                '**/*.wav',
                '**/*.png',
                '**/*.jpg',
                '**/*.ttf',
                '**/*.egg'
            ],
            'exclude_patterns': [
            #     '**/*.ogg',
            #     '**/*.wav',
                '**/*.txt',
            #     '**/*.egg'
            ],
            'gui_apps': {
                'Earthbound_64': 'game_main.py',
            },
            'log_filename': 'output.log',
            'log_append': True,
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
        }
    }
)
