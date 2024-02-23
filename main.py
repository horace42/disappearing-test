from tkinter import *
from tkinter import ttk
from tkinter.font import Font


class MainWindow:
    """
    Tk interface definition
    """
    def __init__(self, r: Tk):
        self.root = r
        self.root.minsize(width=1024, height=768)

        # integer variable for the user selected timeout
        self.timeout_int = 5
        # identifier to cancel scheduling
        self.after_id = None

        mainframe = ttk.Frame(self.root, width=1024, height=768)
        mainframe.configure(borderwidth=10, relief="raised")
        mainframe.grid_propagate(False)
        mainframe.grid(column=0, row=0)

        instruction_label = ttk.Label(mainframe, width=30, text="Choose timeout and start typing")
        instruction_label.grid(column=0, row=0)

        # radio buttons for choosing timeout value
        self.timeout_var = StringVar(value="5")
        five_radio = ttk.Radiobutton(mainframe, text="5 seconds", width=20,
                                     variable=self.timeout_var, value="5",
                                     command=self.timeout_select)
        five_radio.grid(column=0, row=1)
        ten_radio = ttk.Radiobutton(mainframe, text="10 seconds", width=20,
                                    variable=self.timeout_var, value="10",
                                    command=self.timeout_select)
        ten_radio.grid(column=0, row=2)

        # display number of typed words
        words_frame = ttk.Frame(mainframe, width=100, height=20)
        words_frame.grid(column=3, row=1)
        words_frame.grid_propagate(False)
        self.words_count_var = StringVar(value="0")
        words_count_label = ttk.Label(words_frame, textvariable=self.words_count_var, width=3, anchor="e")
        words_count_label.grid(column=0, row=0)
        words_label = ttk.Label(words_frame, text="words")
        words_label.grid(column=1, row=0)

        # display countdown to text deletion
        self.timer_var = StringVar(value="5")
        font = Font(font=("Segoe UI", 40, NORMAL))
        style = ttk.Style()
        style.configure("Countdown.TLabel", foreground="green", font=font)
        timer_label = ttk.Label(mainframe, textvariable=self.timer_var, width=2, anchor="e", style="Countdown.TLabel")
        timer_label.grid(column=4, row=1, rowspan=2)

        # text widget for user input
        self.input_text = Text(mainframe, name="input_text", width=60, height=20, wrap=WORD,
                               background="white", padx=10, pady=10)
        self.input_text.grid(column=0, row=3, columnspan=5)
        self.input_text.bind("<space>", self.count_words)
        self.input_text.bind("<Return>", self.count_words)
        self.input_text.bind("<Key>", self.timing_out)

        self.input_text.focus()

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=10)

    def timeout_select(self):
        """
        Update timeout based on user selecting radio button
        :return:
        """
        self.timeout_int = int(self.timeout_var.get())
        self.timer_var.set(str(self.timeout_int))
        self.input_text.focus()

    def count_words(self, event):
        """
        Count number of typed words, bind to Return and space
        :param event: Event
        :return: None
        """
        txt = self.input_text.get("1.0", "end -1 chars")
        txt_array = txt.split()
        self.words_count_var.set(str(len(txt_array)))

    def timing_out(self, event):
        """
        End current countdown and start another, bind to any key
        :param event: Event
        :return: None
        """
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.timer_var.set(str(self.timeout_int))
        self.after_id = self.root.after(1000, self.delete_text, self.timeout_int)

    def delete_text(self, timer):
        """
        Count down every second and updated displayed timer. Delete text when counter reaches zero.
        :param timer: Remaining time in seconds.
        :return: None
        """
        if timer == 0:
            self.input_text.delete("1.0", END)
            self.words_count_var.set("0")
        else:
            self.timer_var.set(str(timer - 1))
            self.after_id = self.root.after(1000, self.delete_text, timer - 1)


def main():
    root = Tk()
    root.title("Disappearing Text Writing App")
    MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
