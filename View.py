# This file is the GUI python file
# Run View can get GUI interface
from tkinter import *
from functools import partial
import webbrowser
import information_retrieval


class HyperlinkManager:

    def __init__(self, text):

        self.text = text

        self.text.tag_config("hyper", foreground="blue", underline=1)

        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return

class View:
    def __init__(self):
        self.window = Tk()
        self.window.geometry('1000x700')
        self.window.title('Information Retrieval')
        self.name = 'Zhiqi (Victoria) Rong & Sue Ji \n zhiqir & chenqinj'
        self.name_label = Label(self.window, text=self.name, font=('Helvetica', 15), width=30, height=4, background='alice blue')
        self.query = Label(self.window, text='Enter your query:', font=('Helvetica', 17, 'bold'), width=30, height=1)

        self.name_label.place(x=250, y=5)
        self.query.place(x=25, y=121)
        self.query_input = Entry(self.window, bd=7)
        self.query_input.place(x=255, y=115)

        def boolean_search():
            scroll = Scrollbar()
            text = Text(self.window, font=('Helvetica', 16), background='mint cream')
            scroll.place(x=110, y=210)
            text.place(x=110, y=160)
            scroll.config(command=text.yview)
            text.config(yscrollcommand=scroll.set)

            if self.query_input.get() != '':
                final_string, time, url_list_string_list, final_url_list = information_retrieval.show_result(self.query_input.get())
                hyperlink = HyperlinkManager(text)
                text.insert('insert', final_string)

                for i in range(len(final_url_list)):
                    text.insert('insert', url_list_string_list[i],hyperlink.add(partial(webbrowser.open, final_url_list[i])))
                    text.insert('insert', '\n\n')

                self.time_show = Label(self.window, text=time, font=('Helvetica', 17), width=50, height=2,
                                       background='alice blue')
                self.time_show.place(x=120, y=640)
        #     if self.query_input.get() != '':
        #         final_string, time = boolean_retrieval.show_result(self.query_input.get())
        #         self.query_show = Label(self.window, text=final_string, font=('Helvetica', 17), width=100, height=10, background='mint cream')
        #         self.time_show = Label(self.window, text=time, font=('Helvetica', 17), width=50, height=2, fg='cornflower blue')
        #         self.query_show.place(x=5, y=165)
        #         self.time_show.place(x=50, y=400)
        #     else:
        #         try:
        #             self.query_show.destroy()
        #             self.time_show.destroy()
        #         except:
        #             pass

        button1 = Button(self.window, text='Search', width=15, height=2, command=boolean_search)
        button1.place(x=470, y=115)

    def mainloop(self):
        self.window.mainloop()


if __name__ == '__main__':
    x = View()
    x.mainloop()
