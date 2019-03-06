from imports import *
from kivy.garden.filebrowser import FileBrowser
from activity import *
from log import *
from controllers import *
from os.path import join


class FilePopup(Popup):
    def __init__(self, map, grid, log, sm, type, content = "", **kwargs):
        super().__init__(**kwargs)
        self.auto_dismiss = False
        if type == "oload":
            self.title = "Load File"
            fbrowser = OdoSelect(self, map, grid, log, sm, dpath = "data", sel_str="Select")
        elif type == "isave":
            self.title = "Save File"
            fbrowser = ImgSave(self, map, grid, log, sm, dpath = "plots", sel_str="Save")
        elif type == "asave":
            self.title = "Save Activity"
            fbrowser = ActSave(self, map, grid, log, sm, dpath = "saved", sel_str="Save",
                               content = content)
        else:
            self.title = "Load Activity"
            fbrowser = ActSelect(self, map, grid, log, sm, dpath="saved", sel_str="Select")
        self.add_widget(fbrowser)


class Dialog(FileBrowser):
    """
    filebrowser
    """
    def __init__(self, pop, map, grid, log, sm, dpath, sel_str, **kwargs):
        if sys.platform == 'win':
            self.user_path = dirname(expanduser(os.getcwd())) + sep + dpath
        else:
            self.user_path = expanduser(os.getcwd()) + sep + dpath
        # print(self.user_path)

        super().__init__(select_string=sel_str, path = self.user_path,
                              favorites=[(self.user_path, dpath)], **kwargs)
        self.bind(on_success=self._fbrowser_success,
                    on_canceled=self._fbrowser_canceled)
        self.pop = pop
        self.grid = grid
        self.map = map
        self.sm = sm
        self.log = log


    def _fbrowser_canceled(self, instance):
        # print ('cancelled, Close self.')
        self.pop.dismiss()

    def _fbrowser_success(self, instance):
        # print(instance.selection)
        self.pop.dismiss()


class OdoSelect(Dialog):
    """
    filebrowser
    """
    def __init__(self, pop, map, grid, log, sm, dpath, sel_str, **kwargs):
        super().__init__(pop, map, grid, log, sm, dpath, sel_str, **kwargs)
        self.filters = ["*.odo"]

    def _fbrowser_success(self, instance):
        # print(instance.selection)
        if(len(instance.selection) == 0):
            # print('no selection')
            return
        fpath = str(instance.selection[0])
        fname = basename(fpath)
        # print (fname)
        # return fname
        self.add_odor(fname)
        self.pop.dismiss()

    def add_odor(self, o):
        odor = Odor(o)
        self.grid.addOdor(odor)
        # self.grid.addOdor(self.o2)
        # print("add")
        # displayActivations(self.grid)
        # self.map.plot_canv.draw()
        self.map.update()
        self.sm.add_om(o)
        # self.log.


class ImgSave(Dialog):
    """
    filebrowser
    """

    def __init__(self, pop, map, grid, log, sm, dpath, sel_str, **kwargs):
        super().__init__(pop, map, grid, log, sm, dpath, sel_str, **kwargs)
        self.filters = ["*.png"]

    def _fbrowser_success(self, instance):
        #TODO display default filename
        if self.filename == "":
            self.filename = "my_plot.png"
        # print(self.filename)
        self.map.plot_canv.print_png(join(self.user_path, self.filename))  #"my_plot.png"
        self.pop.dismiss()


class ActSelect(Dialog):
    """
    Dialog to select activity file to load
    """
    def __init__(self, pop, map, grid, log, sm, dpath, sel_str, **kwargs):
        super().__init__(pop, map, grid, log, sm, dpath, sel_str, **kwargs)
        self.filters = ["*.act"]

    def _fbrowser_success(self, instance):
        # print(instance.selection)
        if(len(instance.selection) == 0):
            # print('no selection')
            return
        fpath = str(instance.selection[0])
        # print(fpath)
        # fname = basename(fpath)
        # print (fname)
        # return fname
        self.grid.clear()
        self.sm.clear()
        self.log.clear()
        with open(fpath) as f:
            for line in f:
                # print(line)
                l = line[:-1].split("\t")
                # print(l)
                fname = l[0]
                conc = float(l[1])
                self.add_odor(fname, conc)
        self.pop.dismiss()

    def add_odor(self, o, c):
        odor = Odor(o)
        self.grid.addOdor(odor)
        self.grid.adjustConcs(odor, c)
        # self.grid.addOdor(self.o2)
        # print("add")
        # displayActivations(self.grid)
        # self.map.plot_canv.draw()
        self.map.update()
        self.sm.add_om(o)


class ActSave(Dialog):
    """
    Dialog to save new activity file
    """
    def __init__(self, pop, map, grid, log, sm, dpath, sel_str, content, **kwargs):
        super().__init__(pop, map, grid, log, sm, dpath, sel_str, **kwargs)
        self.filters = ["*.act"]
        self.content = content

    def _fbrowser_success(self, instance):
        if self.filename == "":
            self.filename = "my_activity.act"
        # print(self.filename)
        with open(join(self.user_path,self.filename), "w") as f:
            f.write(self.content)
        f.close()
        self.pop.dismiss()



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
        self.add_widget(self.fbrowser)
        self.save_btn =  Button(on_press=self.export_activity, text="Export Activity")
        self.add_widget(self.save_btn)
        self.load_btn =  Button(on_press=self.load_activity, text="Load Activity")
        self.add_widget(self.load_btn)
        self.img_btn =  Button(on_press=self.save_img, text="Save Image")
        self.add_widget(self.img_btn)
        self.clear_btn =  Button(text="Clear All", on_press = self.clear)
        self.add_widget(self.clear_btn)


    def open_browser(self, b):
        p = FilePopup(self.map, self.grid, self.log, self.sm, type="oload", size_hint=(0.7,0.7))
        p.open()


    def export_activity(self, b):
        r = self.grid.receptors[0]
        # r.odors.keys()
        f = ""
        for i in r.concs.items():
            f += str(i[0]) + '\t' + str(i[1]) + '\n'
        p = FilePopup(self.map, self.grid, self.log, self.sm, type="asave", content=f, size_hint=(0.7, 0.7))
        p.open()

    def load_activity(self, b):
        p = FilePopup(self.map, self.grid, self.log, self.sm, type="aload", size_hint=(0.7, 0.7))
        p.open()

    def save_img(self, b):
        p = FilePopup(self.map, self.grid, self.log, self.sm, type="isave", size_hint=(0.7, 0.7))
        p.open()
        # self.map.plot_canv.print_png("my_plot.png")

    def clear(self, b):
        self.map.clear()
        self.sm.clear()
        self.log.clear()
        # for plot in self.log.plots:
        #     self.my_graph.remove_plot(plot)
