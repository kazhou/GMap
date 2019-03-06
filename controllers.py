from imports import *
import math

class MyScrollView(ScrollView):
    pass

Builder.load_string('''
<MyScrollView>:
    canvas:
        Color:
            rgb: 0.75, 0.75, 0.75
        Rectangle:
            pos: self.pos
            size: self.size
''')


class OManager(BoxLayout):
    """
    Controls for single odor:
    Check box, slider, replace/remove
    """
    slider_val = NumericProperty(-5)
    def __init__(self, menu, odor, grid, map, log, **kwargs):
        super().__init__(**kwargs)
        self.menu = menu
        self.odor = odor
        self.grid = grid
        self.map = map
        self.log = log
        self.conc = round(1/math.log(10, self.grid.getConc(odor)),1) #-5

        self.checkbox = CheckBox(color = [0,0,1,1], size_hint=(0.1,1), group = 'show')
        self.checkbox.bind(active = self.show_plot)

        self.big_box1 = BoxLayout(orientation="vertical",size_hint=(0.20,1))
        self.name = Label(text=('[size=16][color=000000]'+str(odor)),
                    markup = True, size_hint=(1,0.15))
        self.big_box1.add_widget(self.name)

        self.box = BoxLayout(orientation="vertical",size_hint=(0.20,1))
        # self.show_btn = ToggleButton(text="Show",size_hint=(1,0.5))
        self.reset_btn = Button(text="Reset",size_hint=(1,0.5),
                        on_press = self.reset)
        self.remove_btn = Button(text="Remove",
                        size_hint=(1,0.5), on_press=self.remove)
        self.box.add_widget(self.reset_btn)
        self.box.add_widget(self.remove_btn)
        self.padding = [5,10,5,10]
        self.slider = Slider(min=-10, max=0, step=0.5, value=self.conc,
                        size_hint=(0.5,1))
        self.slider.fbind('value', self.on_slider_val)
        self.label = Label(text=('[size=18][color=000000]10e'+str(self.conc)),
                    markup = True, size_hint=(0.2,1))
        self.big_box2 = BoxLayout(orientation="horizontal", size_hint=(1,0.85))

        self.big_box2.add_widget(self.box)
        self.big_box2.add_widget(self.slider)
        self.big_box2.add_widget(self.label)
        self.big_box2.add_widget(self.checkbox)

        self.big_box1.add_widget(self.big_box2)
        self.add_widget(self.big_box1)

    def on_slider_val(self, instance, val):
        self.label.text = ('[size=18][color=000000]10e'+str(val))
        self.conc = val
        if self.log.odor == self.odor:
            self.log.conc = val
            self.log.updateConcLine()
        #TODO: adjust COnc by val
        #udpate map
        self.adjust_conc(pow(10,val))


    def reset(self, instance):
        self.slider.value = -5
        if self.log.odor == self.odor:
            self.log.conc = -5
            self.conc = -5
            self.log.updateConcLine()
        self.adjust_conc(1e-5)

    def adjust_conc(self, conc):
        odor = self.grid.odors[self.odor]
        self.grid.adjustConcs(odor, conc)
        # print("adj")
        self.map.update()

    def remove(self, instance):
        # print(self.menu.om_list)
        # print("remove")
        self.menu.remove_om(self.odor)
        # print(self.name)
        print(self.menu.om_list)

    def show_plot(self, instance, active):
        # print('in choose odor')
        if not active:
            self.log.graph.remove_plot(self.log.plot)
            self.log.odor = None
            return

        self.log.odor = self.odor
        self.log.conc = self.conc
        # print(self.conc, self.log.conc)
        self.log.graph.remove_plot(self.log.plot)
        self.log.plot = MeshLinePlot(color=[1, 0, 0, 1])
        data = self.log.getData(self.log.receptor, self.log.odor)
        self.log.plot.points = data
        self.log.graph.add_plot(self.log.plot)

        self.log.updateConcLine()

    def hide(self):
        pass

    def show(self):
        pass

class SlideMenu(BoxLayout):
    """
    Menu of sliders to adjust concentrations
    """
    def __init__(self, grid, map, log, **kwargs):
        super().__init__(**kwargs)
        self.grid = grid
        self.map = map
        self.log = log

        self.orientation="vertical"
        self.background_color = (1, .5, 0, 1)
        size = len(grid.odors)
        self.om_list = {}
        odors = list(grid.odors.keys())
        for i in range(size):
            self.om_list[odors[i]] = OManager(self, odors[i],
                        self.grid, self.map, self.log,
                        size=(self.width, 75),
                         size_hint=(None, None))
            self.add_widget(self.om_list[odors[i]])

    def add_om(self, odor):
        if odor in self.om_list:
            return
        om = OManager(self, odor, self.grid, self.map,  self.log,
                    size=(self.width, 75),
                     size_hint=(None, None))
        self.om_list[odor] = om
        self.add_widget(om)

    def remove_om(self, odor):
        if odor not in self.om_list:
            return
        self.remove_widget(self.om_list[odor])
        self.grid.removeOdor(odor)
        self.map.update()
        self.log.graph.remove_plot(self.log.plot)
        del self.om_list[odor]

    def clear(self):
        self.om_list = {}
        self.clear_widgets()

class MapOptions(BoxLayout):
    """
    """
    def getState(self):
        return self.opt_btn.text

    def __init__(self, map, **kwargs):
        super().__init__(**kwargs)
        self.map = map
        self.orientation = "horizontal"
        self.opt_btn = ToggleButton(text='Occupancy', state='down',
                size_hint=(0.5,1), on_press=self.update)
        # self.opt_btn.bind(self.update)
        # self.act_btn = ToggleButton(text='Activation', group='opt',
        #         size_hint=(0.5,1))
        self.add_widget(self.opt_btn)

    def update(self,event):
        #TODO: switch map display
        if self.opt_btn.state == 'normal':
            self.opt_btn.text = "Activation"
        else:
            self.opt_btn.text = "Occupancy"
        self.map.state = self.opt_btn.text
        self.map.update()


class LogOptions(BoxLayout):
    """
    """
    def getState(self):
        return self.opt_btn.text

    def __init__(self, log, grid, **kwargs):
        super().__init__(**kwargs)
        self.log = log
        self.grid = grid
        self.orientation = "horizontal"
        self.opt_btn = ToggleButton(text='Occupancy', state='down',
                size_hint=(0.4,1), on_press=self.update)
        self.add_widget(self.opt_btn)

        # self.padding = [0,50,0,50]
        row1 = BoxLayout(orientation="horizontal", size_hint=(0.6,1))
        self.rec_label = Label(text=('[size=16][color=000000]Receptor'),
                    markup = True, size_hint=(0.7, 1))
        self.rec_select = TextInput(text = "0", multiline=False, input_type='number',
            on_text_validate=self.choose_rec, size_hint=(0.3, 1))
        # row1.padding = [5,20,5,20]
        row1.add_widget(self.rec_label)
        row1.add_widget(self.rec_select)

        # row2 = BoxLayout(orientation="horizontal", size_hint=(1,0.4))
        # self.odor_label = Label(text=('[size=16][color=000000]Odor'),
        #             markup = True, size_hint=(0.5, 1))
        # self.odor_select = TextInput(multiline=False, input_type='text',
        #     on_text_validate=self.choose_odor, size_hint=(0.5, 1))
        # row2.padding = [5,20,5,20]
        # row2.add_widget(self.odor_label)
        # row2.add_widget(self.odor_select)

        self.add_widget(row1)
        # self.add_widget(row2)

        # self.odor_select

    def choose_rec(self,instance):
        # Ensure within bounds
        # print('in choose rec')
        value = int(self.rec_select.text)
        if value >= self.grid.num_receptors or value < 0:
            return
        self.log.receptor = value
        self.log.graph.remove_plot(self.log.plot)
        self.log.plot = MeshLinePlot(color=[1, 0, 0, 1])
        data = self.log.getData(self.log.receptor, self.log.odor)
        self.log.plot.points = data
        self.log.graph.add_plot(self.log.plot)

        self.log.updateConcLine()



    def update(self, event):
        #TODO: switch map display
        # print("update")
        if self.opt_btn.state == 'normal':
            self.opt_btn.text = "Activation"
            self.log.state =  "Activation"
        else:
            self.opt_btn.text = "Occupancy"
            self.log.state =  "Occupancy"
        # print(self.state)
        self.log.graph.remove_plot(self.log.plot)
        self.log.plot = MeshLinePlot(color=[1, 0, 0, 1])
        data = self.log.getData(self.log.receptor, self.log.odor)
        self.log.plot.points = data
        self.log.graph.add_plot(self.log.plot)

        self.log.updateConcLine()
