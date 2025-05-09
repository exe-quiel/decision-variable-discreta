import tkinter as tk

class DoubleEntryTable(tk.Frame):

    def __init__(self, parent, values, column_headers, row_headers, on_header_click=None, disable_values=False, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.values = values
        self.disable_values = disable_values
        self.row_headers = []
        self.column_headers = []
        self.entries = []

        for col_index in range(len(column_headers)):
            #col_label = tk.Label(self, text=column_headers[col_index], width=10, padx=0, borderwidth=1, relief=tk.GROOVE, bg='black', fg='white')
            col_label = tk.Label(self, text=column_headers[col_index], width=10, padx=0)
            col_label.grid(column=col_index + 1, row=0, padx=0, pady=0, sticky=tk.NSEW)
            col_label.bind('<Button-1>', on_header_click)
            self.column_headers.append(col_label)
        for row_index in range(len(row_headers)):
            #row_label = tk.Label(self, text=row_headers[row_index], width=10, padx=0, borderwidth=1, relief=tk.GROOVE, bg='black', fg='white')
            row_label = tk.Label(self, text=row_headers[row_index], width=10, padx=0)
            row_label.grid(column=0, row=1 + row_index, padx=0, pady=0, sticky=tk.NSEW)
            row_label.bind('<Button-1>', on_header_click)
            self.row_headers.append(row_label)
        for value_row_index in range(len(values)):
            for value_col_index in range(len(values[value_row_index])):
                value_entry = tk.Entry(self, width=10, relief=tk.RIDGE, borderwidth=1, name=f'{value_col_index}-{value_row_index}', justify=tk.RIGHT)
                value_entry.delete(0, tk.END)
                value_entry.insert(0, values[value_row_index][value_col_index])
                #t = tk.Label(f, width=5, background='#ffffff', border=1, borderwidth=1)
                if self.disable_values:
                    value_entry.config(state=tk.DISABLED)
                value_entry.grid(column=value_col_index + 1, row=value_row_index + 1, pady=0, padx=0, sticky=tk.NSEW)
                self.entries.append(value_entry)

        #self.pack()

    def get_values_as_list(self):
        #self.values = []
        for entry in self.entries:
            value_pos = str(entry).split('.')[-1].split('-')
            x, y = int(value_pos[0]), int(value_pos[1])
            self.values[y][x] = float(entry.get())
        return self.values

    def get_row_headers(self):
        return [label.cget('text') for label in self.row_headers]

    def get_column_headers(self):
        return [label.cget('text') for label in self.column_headers]


if __name__ == '__main__':
    import tkinter.simpledialog
    
    def read_str_and_replace_header(event):
        new_text = tk.simpledialog.askstring('New header text', 'Type new text')
        event.widget['text'] = new_text

    root = tk.Tk()
    
    DoubleEntryTable(root,
                     [[1, 2, 3, 4, 5, 6], [5, 6, 7, 8, 1, 1], [9, 10, 11, 12, 2, 2]],
                     ['Col 1', 'Col 2', 'Col 3', 'Col 4', 'Col 5', 'Col 6'],
                     ['Row 1', 'Row 2', 'Row 3'],
                     on_header_click=read_str_and_replace_header).pack()

    root.mainloop()


        