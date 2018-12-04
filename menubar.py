from imports import *
from kivy.garden.filebrowser import FileBrowser
from activity import *
from log import *


class FilePopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auto_dismiss = True
        fbrowser = FileSelect()
        self.add_widget(fbrowser)


class FileSelect(FileBrowser):
    """
    filebrowser
    """
    def __init__(self,**kwargs):
        if sys.platform == 'win':
            self.user_path = dirname(expanduser(os.getcwd())) + sep + 'data'
        else:
            self.user_path = expanduser(os.getcwd()) + sep + 'data'
        print(self.user_path)

        super().__init__(select_string='Select',
                              favorites=[(self.user_path, 'data')], **kwargs)
        self.bind(on_success=self._fbrowser_success,
                    on_canceled=self._fbrowser_canceled)


    def _fbrowser_canceled(self, instance):
        print ('cancelled, Close self.')
        # self.dismiss()
        #TODO: close

    def _fbrowser_success(self, instance):
        print(instance.selection)
        if(len(instance.selection) == 0):
            print('no selection')
            return
        fpath = str(instance.selection[0])
        fname = basename(fpath)
        print (fname)
        return fname
        #TODO add odor


class MenuBar(BoxLayout):
    """
    Menu Bar at top
    """
    def __init__(self, grid, map, **kwargs):
        super().__init__(**kwargs)
        self.grid = grid
        self.map = map

        self.fbrowser = Button(on_press=self.open_browser, text="New Odor")
                                # size_hint=(0.1,1))
        self.add_widget(self.fbrowser)
        self.save_btn =  Button(text="Save Activity")
        self.add_widget(self.save_btn)
        self.clear_btn =  Button(text="Clear All")
        self.add_widget(self.clear_btn)

        #TODO: for demonstration
        self.o1 = Odor('odorlog_5-4-100a.odo')
        self.o2 = Odor('odorlog_5-4-100b.odo')
        self.add_btn =  Button(text="Add Odor", on_press=self.add_odor)
        self.add_widget(self.add_btn)
        self.remove_btn =  Button(text="Remove Odor", on_press=self.remove_odor)
        self.add_widget(self.remove_btn)
        self.conc_btn =  Button(text="Change Conc", on_press=self.adjust_conc)
        self.add_widget(self.conc_btn)

    def open_browser(self, b):
        p = FilePopup(size_hint=(0.7,0.7))
        p.open()

    def add_odor(self, b):
        self.grid.addOdor(self.o1)
        # self.grid.addOdor(self.o2)
        print("add")
        # displayActivations(self.grid)
        # self.map.plot_canv.draw()
        self.map.update("Occupancy")

    def remove_odor(self, b):
        self.grid.removeOdor(self.o1)
        print("remove")
        self.map.update("Occupancy")

    def adjust_conc(self, b):
        self.grid.adjustConcs(self.o2, 10e-4)
        print("adj")
        self.map.update("Occupancy")
