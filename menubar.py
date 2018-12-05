from imports import *
from kivy.garden.filebrowser import FileBrowser
from activity import *
from log import *
from controllers import *


class FilePopup(Popup):
    def __init__(self,map, grid, sm, **kwargs):
        super().__init__(**kwargs)
        self.auto_dismiss = False
        self.title = "Load File"
        fbrowser = FileSelect(self, map, grid, sm)
        self.add_widget(fbrowser)


class FileSelect(FileBrowser):
    """
    filebrowser
    """
    def __init__(self, pop, map, grid, sm, **kwargs):
        if sys.platform == 'win':
            self.user_path = dirname(expanduser(os.getcwd())) + sep + 'data'
        else:
            self.user_path = expanduser(os.getcwd()) + sep + 'data'
        print(self.user_path)

        super().__init__(select_string='Select',
                              favorites=[(self.user_path, 'data')], **kwargs)
        self.bind(on_success=self._fbrowser_success,
                    on_canceled=self._fbrowser_canceled)
        self.pop = pop
        self.grid = grid
        self.map = map
        self.sm = sm


    def _fbrowser_canceled(self, instance):
        print ('cancelled, Close self.')
        self.pop.dismiss()
        #TODO: close

    def _fbrowser_success(self, instance):
        print(instance.selection)
        if(len(instance.selection) == 0):
            print('no selection')
            return
        fpath = str(instance.selection[0])
        fname = basename(fpath)
        print (fname)
        # return fname
        self.add_odor(fname)
        self.pop.dismiss()

    def add_odor(self, o):
        odor = Odor(o)
        self.grid.addOdor(odor)
        # self.grid.addOdor(self.o2)
        print("add")
        # displayActivations(self.grid)
        # self.map.plot_canv.draw()
        self.map.update()
        self.sm.add_om(o)

    def remove_odor(self, o):
        # TODO: move this
        self.grid.removeOdor(self.o1)
        print("remove")
        self.map.update()
        self.sm.remove_om(o)



class MenuBar(BoxLayout):
    """
    Menu Bar at top
    """
    def __init__(self, grid, map, log, sm, **kwargs):
        super().__init__(**kwargs)
        self.grid = grid
        self.map = map
        self.log = log
        self.sm = sm

        self.fbrowser = Button(on_press=self.open_browser, text="New Odor")
                                # size_hint=(0.1,1))
        self.add_widget(self.fbrowser)
        self.save_btn =  Button(text="Export Activity")
        self.add_widget(self.save_btn)
        self.load_btn =  Button(text="Load Activity")
        self.add_widget(self.load_btn)
        self.img_btn =  Button(text="Save Image")
        self.add_widget(self.img_btn)
        self.clear_btn =  Button(text="Clear All", on_press = self.clear)
        self.add_widget(self.clear_btn)


    def open_browser(self, b):
        p = FilePopup(self.map, self.grid, self.sm, size_hint=(0.7,0.7))
        p.open()


    def export_activity(self, b):
        pass

    def load_activity(self, b):
        pass

    def save_img(self, b):
        pass
        # self.map.plot_canv.print_png("my_plot.png")

    def clear(self, b):
        self.map.clear()
        self.sm.clear()
        self.log.clear()
        # for plot in self.log.plots:
        #     self.my_graph.remove_plot(plot)
