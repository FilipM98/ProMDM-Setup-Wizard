import wx
import math


class Wizard(wx.Panel):
    page_index = 0
    num_of_pages = 0
    inputs_per_page = 6
    conf_lines = []

    with open("temp.txt") as file_in:
        for line in file_in:
            if not "#" in line and "ENV" in line:
                conf_lines.append(line[0: line.find("=")].replace(" ", ""))
    num_of_pages = int(math.ceil(len(conf_lines) / inputs_per_page))
    texts = [""] * len(conf_lines)
    texts[0] = "localhost"
    texts[1] = "8080"

    def __init__(self, parent, index):
        self.page_index = index
        wx.Panel.__init__(self, parent)
        tekst = 'ProMDM Wizard ' + str(self.page_index + 1) + " / " + str(self.num_of_pages)
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        wx.StaticText(self, -1, tekst, (330, 20)).SetFont(font)

        for i in range(index * self.inputs_per_page, (index + 1) * self.inputs_per_page):
            if not i >= len(self.conf_lines):
                bonus_space = i % self.inputs_per_page * 40
                wx.StaticText(self, -1, self.conf_lines[i], (150, 80 + bonus_space))
                self.texts[i] = wx.TextCtrl(self, -1, self.texts[i], (450, 75 + bonus_space), (150, 30))

        self.btnBack = wx.Button(self, -1, "Back", (325, 525))
        self.btnCancel = wx.Button(self, -1, "Cancel", (495, 525))
        if self.page_index == 0:
            self.btnBack.Enable(False)
        if self.page_index == self.num_of_pages - 1:
            self.btnNext = wx.Button(self, -1, "Finish", (410, 525))
        else:
            self.btnNext = wx.Button(self, -1, "Next", (410, 525))


class Program(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, 'ProMDM', wx.DefaultPosition, (800, 600),
                          style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        self.texts = []
        self.panels = []

        self.panels.append(Wizard(self, 0))
        sizer.Add(self.panels[0], 1, wx.EXPAND)
        self.panels[0].btnNext.Bind(wx.EVT_BUTTON, self.show_next_panel)
        self.panels[0].btnCancel.Bind(wx.EVT_BUTTON, self.cancel)
        self.current_panel = self.panels[0]

        for i in range(1, self.panels[0].num_of_pages):
            self.panels.append(Wizard(self, i))
            sizer.Add(self.panels[i], 1, wx.EXPAND)
            if (i == self.panels[0].num_of_pages - 1):
                self.panels[i].btnNext.Bind(wx.EVT_BUTTON, self.write)
            else:
                self.panels[i].btnNext.Bind(wx.EVT_BUTTON, self.show_next_panel)
            self.panels[i].btnCancel.Bind(wx.EVT_BUTTON, self.cancel)
            self.panels[i].btnBack.Bind(wx.EVT_BUTTON, self.show_prev_panel)

    def show_prev_panel(self, event):
        current_page = self.current_panel.page_index
        self.panels[current_page].Hide()
        self.panels[current_page - 1].Show()
        self.current_panel = self.panels[current_page - 1]
        self.Layout()

    def show_next_panel(self, event):
        current_page = self.current_panel.page_index
        self.panels[current_page].Hide()
        self.panels[current_page + 1].Show()
        self.current_panel = self.panels[current_page + 1]
        self.Layout()

    def cancel(self, event):
        self.Destroy()

    def write(self, event):
        result_file = open("example.txt", "w")
        for index, text in enumerate(self.current_panel.texts):
            if text.GetValue() == "":
                "#"+self.current_panel.conf_lines[index]
            else:
                result_file.write(self.current_panel.conf_lines[index] + " = \"" + text.GetValue() + "\"\n")
        result_file.close()
        self.Destroy()


if __name__ == "__main__":
    app = wx.App(False)
    frame = Program()
    frame.Show()
    app.MainLoop()