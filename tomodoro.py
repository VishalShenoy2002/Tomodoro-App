from kivymd.app import MDApp

from kivymd.uix.bottomnavigation import MDBottomNavigation,MDBottomNavigationItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton,MDRectangleFlatIconButton,MDFloatingActionButtonSpeedDial,MDRaisedButton,MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.list import MDList,OneLineListItem,IconRightWidget
from kivymd.uix.dialog import MDDialog

from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

import os




class SocialMediaApp(MDApp):
    
    def build(self):
        self.icon="icon.ico"
        self.title="Tomodoro"

        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette="Red"
        self.seconds=900
        self.dialog=None
        self.tasklist=[]
        
        with open('tasks.txt','w') as f:
            f.write('')
            f.close()
        
        self.timer_clock=Clock
        
        self.manager=MDBottomNavigation()

        self.todo_tab=MDBottomNavigationItem(name="TodoScreen",text="To-Do List",icon='format-list-bulleted')
        self.manager.add_widget(self.todo_tab)

        self.timer_tab=MDBottomNavigationItem(name="TimerScreen",text="Pomodoro",icon='timer')
        self.manager.add_widget(self.timer_tab)


        # === Creating Top Cards === #
        self.create_top_card=MDCard(elevation=20,size_hint=(0.8,0.1),radius=20,pos_hint={"top":1,"center_x":0.5})
        self.timer_tab.add_widget(self.create_top_card)

        # === ToDo Screen === #
        self.main_todo_box_layout=MDBoxLayout(orientation="vertical")
        self.todo_tab.add_widget(self.main_todo_box_layout)

        self.scrollview=ScrollView(do_scroll_x=False,pos_hint={"right":1})
        self.main_todo_box_layout.add_widget(self.scrollview)

        self.task_list=MDList()
        self.scrollview.add_widget(self.task_list)

        self.data={"Create Task":'pencil',"Delete Task":'trash-can-outline'}

        self.create_button=MDFloatingActionButtonSpeedDial(data=self.data,pos_hint={"center_x":0.9},callback=self.check_button_press)
        self.todo_tab.add_widget(self.create_button)


        
    # === Pomodoro Screen === #
        self.pomodoro_card=MDCard(elevation=20,size_hint=(0.8,0.8),radius=20,pos_hint={"top":0.85,"center_x":0.5})
        self.timer_tab.add_widget(self.pomodoro_card)

        self.create_label=MDLabel(text="Pomodoro",bold=True,halign='center',pos_hint={"center_x":0.5})
        self.create_top_card.add_widget(self.create_label)

        self.pomodoro_box_layout=MDBoxLayout(orientation="vertical",spacing=20)
        self.pomodoro_card.add_widget(self.pomodoro_box_layout)

        self.timer_length_boxlayout=MDBoxLayout()
        self.pomodoro_box_layout.add_widget(self.timer_length_boxlayout)

        self.short_timer=MDCheckbox(group="timer_length",active=True)
        self.timer_length_boxlayout.add_widget(self.short_timer)

        self.short_timer_label=MDLabel(text="Short Session",bold=True)
        self.timer_length_boxlayout.add_widget(self.short_timer_label)

        self.long_timer=MDCheckbox(group="timer_length")
        self.timer_length_boxlayout.add_widget(self.long_timer)

        self.long_timer_label=MDLabel(text="Long Session",bold=True)
        self.timer_length_boxlayout.add_widget(self.long_timer_label)

        self.timer_label=MDLabel(text="00:15:00",font_style='H2',halign='center',pos_hint={"center_x":0.5})
        self.pomodoro_box_layout.add_widget(self.timer_label)

        self.timer_button_box_layout=MDBoxLayout()
        self.pomodoro_box_layout.add_widget(self.timer_button_box_layout)

        self.set_button=MDRaisedButton(text="Set",font_size=20,pos_hint={"center_x":0.5},on_release=self.set_timer)
        self.pomodoro_box_layout.add_widget(self.set_button)

        self.start_stop_button=MDRaisedButton(text="Start",font_size=20,pos_hint={"center_x":0.5},on_release=self.start_timer)
        self.pomodoro_box_layout.add_widget(self.start_stop_button)

        self.reset_button=MDFlatButton(text="Reset",font_size=20,size_hint=(None,None),pos_hint={"center_x":0.5},on_release=self.reset_timer)
        self.pomodoro_box_layout.add_widget(self.reset_button)

        self.load_task()

        return self.manager


# === Functions === #  

    def set_timer(self,*args):
        self.seconds=0
        if self.short_timer.state=="down":
            self.seconds=900
            self.format_to_label(self.seconds)
        
        else:
            self.seconds=2700
            self.format_to_label(self.seconds)

    def reset_timer(self,*args):
        self.seconds=0
        if self.short_timer.state=="down":
            self.seconds=900
            self.format_to_label(self.seconds)
        
        else:
            self.seconds=2700
            self.format_to_label(self.seconds)


    def format_to_label(self,seconds):
        m,s=divmod(abs(int(seconds)),60)
        h,m=divmod(m,60)
        timer=str(h).zfill(2)+':'+str(m).zfill(2)+':'+str(s).zfill(2)
        self.timer_label.text=timer
        self.seconds-=1

    def timer_(self,*args):
        if self.start_stop_button.text=="Stop":
            if self.seconds >=0:
                when_to_stop=abs(int(self.seconds))
                self.format_to_label(when_to_stop)


        
    def start_timer(self,*args):
        if self.start_stop_button.text=="Start":
            self.timer_clock.schedule_interval(self.timer_,1)
            self.start_stop_button.text="Stop"
        else:
            self.start_stop_button.text="Start"
            self.timer_clock.unschedule(self.timer_)

    
    def update_list(self,task):
            self.task=OneLineListItem(text=task)
            self.task_list.add_widget(self.task)

    def create_task(self,*args):
        self.tasklist.append(self.create_task_field.text)
        with open("tasks.txt",'a') as f:
            f.write("{}\n".format(self.create_task_field.text))

        self.task=OneLineListItem(text=self.create_task_field.text)
        self.task_list.add_widget(self.task)
        self.create_task_dialog.dismiss()


    def open_task_dialog(self):
        self.create_task_field=MDTextField(hint_text="Task Name",size_hint=(0.8,1),pos_hint={"center_x":0.5})
        self.create_task_button=MDRectangleFlatIconButton(icon='plus',text="Create Task",on_release=self.create_task)
        self.create_task_dialog=MDDialog(title="Create Task",type='custom',content_cls=self.create_task_field,buttons=[self.create_task_button])


        if self.dialog==None:
            self.create_task_dialog.open()
            self.dialog=True
        else:
            self.dialog=None

    def load_task(self):
        with open('tasks.txt') as f:
            self.tasklist=f.readlines()
            f.close()

        for task in self.tasklist:
            self.update_list(task)

    def delete_task(self):
        print(len(self.tasklist))
        if len(self.tasklist) !=0:
            self.tasklist.pop(0)
            with open('tasks.txt','w') as f:
                f.writelines(self.tasklist)
                f.close()
            self.task_list.clear_widgets()
            self.load_task()


    def check_button_press(self,instance):
        if instance.icon=="pencil":
            self.open_task_dialog()
        else:
            self.delete_task()


        
        
        

if __name__=="__main__":
    app=SocialMediaApp()
    app.run()