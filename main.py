from kivy.app import App 
from kivy.lang import Builder 
from kivy.uix.screenmanager import Screen 
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.clock import Clock 
from kivy.core.audio import SoundLoader

class FirstScreen(Screen):
    pass

class ImageButton(ButtonBehavior, Image):
    pass

class SecondScreen(Screen):
    pomodoro_time = 1500
    def on_enter(self):
        print("screen 2")
        Clock.schedule_interval(self.update_pomodoro_timer,1)
        
    
    def update_pomodoro_timer(self,*args):
        self.pomodoro_time -= 1
        self.p_minutes = self.pomodoro_time // 60 
        self.p_seconds = self.pomodoro_time % 60 
        self.ids.timer1.text =("{} : {} ".format(self.p_minutes,self.p_seconds))
        if self.pomodoro_time == 0 :
            sound = SoundLoader.load('timer.ogg')
            if sound:
                sound.play()
            self.ids.timer1.text = "25:00"
            self.pomodoro_time = 1500
            Clock.unschedule(self.update_pomodoro_timer)
            self.manager.current = 'third_screen'


class ThirdScreen(Screen):
    break_time = 300
    def on_enter(self):
        print("screen 3 ")
        Clock.schedule_interval(self.update_break_timer,1)

    def update_break_timer(self,*args):
        self.break_time -= 1
        self.b_minutes = self.break_time // 60 
        self.b_seconds = self.break_time % 60 
        self.ids.timer2.text =("{} : {} ".format(self.b_minutes,self.b_seconds))

        if self.break_time == 0:
             self.ids.timer2.text ="5:00"
             self.break_time = 300
             Clock.unschedule(self.update_break_timer)
             self.manager.current = 'second_screen'
        if self.break_time == 6:
            sound = SoundLoader.load('timer.ogg')
            if sound:
                sound.play()

GUI = Builder.load_file("main.kv")

class MainApp(App):
    def build(self):
        return GUI

    def change_screen(self, screen_name):
        #Get the screen manager from the kv file 
        screen_manager =self.root.ids['screen_manager']
        screen_manager.current = screen_name

MainApp().run()

