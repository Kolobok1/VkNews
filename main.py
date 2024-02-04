from threading import Thread
from post_news import Post_news
import os
from os import environ

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

from tkinter import Tk
from tkinter.filedialog import askopenfilename

Window.size = (400, 600)
Window.clearcolor = (111/255, 212/255, 255/255, 1)
environ['KIVY_CLIPBOARD']  ='sdl2'

class MyApp(App):
    
    photo = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def work_vk(self):
        self.root.children[0].text = Post_news.main(self.post.text, self.photo)
        self.root.children[1].text = ''
            
    def thread_fun(self,post):
        self.root.children[0].text = ''
        t1 = Thread(target=self.work_vk)
        t1.start()
        
    def load_photo(self, arg):

        Tk().withdraw()
        self.photo = askopenfilename()
        if self.photo == '':
            self.root.children[1].text = 'Фото не выбрано'
        else:
            self.root.children[1].text = 'Фото добавлено'
        
    def app_groop(self, arg):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "info", "Group links.txt")
        with open(file_path, 'w', encoding='utf-8') as f:
           f.write(self.post.text)
        self.root.children[0].text = 'Группы обновлены'

    def add_token(self, arg):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "info", "Token.txt")
        with open(file_path, 'w', encoding='utf-8') as f:
           f.write(self.post.text)
        self.root.children[0].text = 'Токен добавлен'
        
    def build(self):
        
        fl = FloatLayout()
        
        btn = Button(size_hint =(.5, .15), 
                    pos_hint = {'center_x':.75, 'y':.0},
                    text ="Запуск",
                    on_press = self.thread_fun)
        
        label = Label(
            pos_hint = {'center_x':.5, 'center_y':.4},
            color = (1/255,1/255,1/255,1))   
        
        label1 = Label(text='Текст поста',
                    pos_hint = {'center_x':.21, 'center_y':.92},
                    color = (1/255,1/255,1/255,1)
                    )
        
        self.post = TextInput(size_hint =(.8, .4), 
                    pos_hint = {'x':.1, 'top':.9},
                    )
        
        btn_photo = Button(size_hint =(.5, .15), 
            pos_hint = {'center_x':.75, 'y':.15},
            text ="Загрузить фото",
            on_press = self.load_photo)
        
        btn_token = Button(size_hint =(.5, .15), 
            pos_hint = {'center_x':.25, 'y':.0},
            text ="Токен",
            on_press = self.add_token)
        
        btn_groops = Button(size_hint =(.5, .15), 
            pos_hint = {'center_x':.25, 'y':.15},
            text ="Группы",
            on_press = self.app_groop)
        
        label2 = Label(
                pos_hint = {'center_x':.5, 'center_y':.45},
                color = (1/255,1/255,1/255,1)
                )
        
        fl.add_widget(label1)
        fl.add_widget(self.post)
        fl.add_widget(btn)
        fl.add_widget(btn_photo)
        fl.add_widget(btn_token)
        fl.add_widget(btn_groops)
        fl.add_widget(label2)
        fl.add_widget(label)
        
        return fl
    
if __name__ == '__main__':
    MyApp().run()