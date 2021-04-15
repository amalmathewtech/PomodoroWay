from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.tab import MDTabsBase


from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.audio import SoundLoader


KV = '''
BoxLayout:
    orientation: "vertical"
    MDToolbar:
        id: toolbar
        title: "PomodoroWay"
        md_bg_color:(0.858,0.32,0.30,1)
        bold: True
    
    MDTabs:
        id: tabs
        background_color:(0.898,0.37,0.34,1)
         
        BoxLayout:
            
            orientation: 'vertical'
            col:(0.898,0.37,0.34,1)
            id : clr
            canvas:
                Color:
                    rgb:self.col
                Rectangle:
                    pos:self.pos
                    size:self.size
            
            FloatLayout:

                MDLabel:
                    id : time
                    text: '[color=#ffffff][b]25[/b]:[b]00[/b][/color]'
                    markup: True
                    halign: 'center'
                    valign: 'middle'
                    font_name: 'Roboto'
                    font_size: 160
            
                MDRectangleFlatButton:
                    id: start_btn
                    text: "[color=#fc382d][b]START[/b][/color]"
                    bold:True
                    md_bg_color:1,1,1,1
                    markup:True
                    pos_hint: {'center_x':0.5, 'center_y':0.3}
                    size_hint: (0.40,0.10)
                    on_press: app.start_timer()

                MDLabel:
                    id : info
                    text: ''
                    color: 1,1,1,1
                    bold:True
                    halign: 'center'
                    pos_hint: {'center_x':0.5, 'center_y':0.2}
                
                MDLabel:
                    id: mode
                    text: 'Pomodoro'
                    markup:True
                    color: 1,1,1,1
                    bold:True
                    halign: 'center'
                    pos_hint: {'center_x':0.5, 'center_y':0.8}
                  
'''

class PomodoroWayApp(MDApp):
    pomodoro_time = 1500
    mode = 1
    cycles = 0

    def update_time(self,sec):
        self.pomodoro_time -= 1
        p_minutes, p_seconds = self.pomodoro_time // 60, self.pomodoro_time % 60
    
        self.root.ids.time.text = ('[color=#ffffff][b]%02d[/b]:[b]%02d[/b][/color]' % (p_minutes, p_seconds))

        if self.mode == 1 and self.pomodoro_time == 0:
            self.mode = 2
            self.root.ids.time.text = '[color=#ffffff][b]05[/b]:[b]00[/b][/color]'
            self.pomodoro_time = 300
            sound = SoundLoader.load('timer.ogg')
            if sound:
                sound.play()

        if self.mode == 2 and self.pomodoro_time == 0:
            self.cycles = self.cycles+1
            if self.cycles == 4:
                self.mode = 3
                self.root.ids.time.text = '[color=#ffffff][b]20[/b]:[b]00[/b][/color]'
                self.pomodoro_time = 1200
                sound = SoundLoader.load('timer.ogg')
                if sound:
                    sound.play()
            else:
                self.mode = 1
                self.root.ids.time.text = '[color=#ffffff][b]25[/b]:[b]00[/b][/color]'
                self.pomodoro_time = 1500
                sound = SoundLoader.load('timer.ogg')
                if sound:
                    sound.play()
        
        if self.mode == 3 and self.pomodoro_time == 0:
            self.restart()
            sound = SoundLoader.load('timer.ogg')
            if sound:
                sound.play()

        if self.mode == 1:
            self.root.ids.info.text = 'Time to work!'
            self.root.ids.mode.text = 'Pomodoro'
            self.root.ids.tabs.background_color = (0.898,0.37,0.34,1)
            self.root.ids.toolbar.md_bg_color = (0.858,0.32,0.30,1)
            self.root.ids.clr.col =(0.898,0.37,0.34,1)

        if self.mode == 2:
            self.root.ids.info.text = 'Time for a break'
            self.root.ids.mode.text = 'Short Break'
            self.root.ids.tabs.background_color = (0.274, 0.55, 0.568, 1)
            self.root.ids.toolbar.md_bg_color = (0.304, 0.58, 0.598, 1)
            self.root.ids.clr.col = (0.274, 0.55, 0.568, 1)
            self.root.ids.start_btn.disabled = True
            self.root.ids.start_btn.opacity = 0

        if self.mode == 3:
            self.root.ids.info.text = 'Time for a break'
            self.root.ids.mode.text = 'Long Break'
            self.root.ids.tabs.background_color = (0.2627, 0.494, 0.65, 1)
            self.root.ids.toolbar.md_bg_color = (0.2927, 0.524, 0.68, 1)
            self.root.ids.clr.col = (0.2627, 0.494, 0.65, 1)
            self.root.ids.start_btn.disabled = True
            self.root.ids.start_btn.opacity = 0

    def restart(self):
        Clock.unschedule(self.update_time)
        self.root.ids.start_btn.opacity = 1
        self.root.ids.start_btn.disabled = False
        self.cycles = 0
        self.mode = 1
        self.root.ids.time.text = '[color=#ffffff][b]25[/b]:[b]00[/b][/color]'
        self.pomodoro_time = 1500


    def start_timer(self):
        self.root.ids.start_btn.opacity = 0
        self.root.ids.start_btn.disabled = True
        Clock.schedule_interval(self.update_time, 1)

    def build(self):
        return Builder.load_string(KV)

PomodoroWayApp().run()
