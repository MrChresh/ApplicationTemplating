import sys
import threading
import zipfile
from docx2pdf import convert
from pypdf import PdfWriter
import json
from tkinter import Button, Entry, Label, Tk, END

#uv pip install docx2pdf pypdf

CONFIG_FILE = 'config.json'
TEMPLATE_PART = 'word/document.xml'


def loadConfig(path=CONFIG_FILE):
    with open(path, encoding='utf-8') as json_file:
        return json.load(json_file)


def updateZip(zipname, dstzipname, filename, replace):
    with zipfile.ZipFile(zipname) as inzip, zipfile.ZipFile(dstzipname, "w") as outzip:
        # Iterate the input files
        for inzipinfo in inzip.infolist():
            # Read input file
            with inzip.open(inzipinfo) as infile:
                if inzipinfo.filename == filename:
                    content = infile.read()
                    content = str(content.decode(encoding='utf8'))
                    # Modify the content of the file by replacing a string
                    for key, value in replace.items():
                        content = content.replace(key, value)
                    # Write content
                    outzip.writestr(inzipinfo.filename, content)
                else:
                    content = infile.read()
                    content = str(content.decode(encoding='utf8'))
                    outzip.writestr(inzipinfo.filename, content)


def generate(config_data, replace):
    updateZip(config_data['read'], 'temp/tempfile.docx', TEMPLATE_PART, replace)

    convert('temp/tempfile.docx', 'temp/tempfile1.pdf')

    # Create a writer object
    writer = PdfWriter()

    writer.append('temp/tempfile1.pdf')

    for value in config_data['append']:
        writer.append(value)

    # Write the combined file to disk
    with open(config_data['out'], 'wb') as output_file:
        writer.write(output_file)

    # Close the writer
    writer.close()


class PlaceholderEntry(Entry):
    """Entry showing the configured value as placeholder while it is empty."""

    def __init__(self, master=None, placeholder='', **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.empty = True
        self.insert(0, placeholder)
        self.configure(fg='grey')
        self.bind('<FocusIn>', self._showInput)
        self.bind('<Button-1>', self._showInput)
        self.bind('<Key>', self._showInput)
        self.bind('<FocusOut>', self._showPlaceholder)

    def _showInput(self, _event=None):
        if self.empty:
            self.delete(0, END)
            self.configure(fg='black')
            self.empty = False

    def _showPlaceholder(self, _event=None):
        if not self.get():
            self.empty = True
            self.configure(fg='grey')
            self.insert(0, self.placeholder)

    def get_value(self):
        return self.placeholder if self.empty else self.get()


class App(Tk):
    def __init__(self, config_data):
        super().__init__()
        self.title('Application templating')
        self.resizable(False, False)
        self.config_data = config_data
        self.entries = {}

        Label(self, text='Template:').grid(row=0, column=0, sticky='w', padx=8, pady=(8, 0))
        Label(self, text=config_data['read'], fg='grey').grid(row=0, column=1, sticky='w', padx=8, pady=(8, 0))
        Label(self, text='Output:').grid(row=1, column=0, sticky='w', padx=8, pady=(0, 8))
        Label(self, text=config_data['out'], fg='grey').grid(row=1, column=1, sticky='w', padx=8, pady=(0, 8))

        row = 2
        for key, value in config_data['replace'].items():
            Label(self, text=key).grid(row=row, column=0, sticky='w', padx=8, pady=2)
            entry = PlaceholderEntry(self, placeholder=value, width=40)
            entry.grid(row=row, column=1, sticky='ew', padx=8, pady=2)
            self.entries[key] = entry
            row += 1

        self.generateButton = Button(self, text='Generate', command=self.startGeneration)
        self.generateButton.grid(row=row, column=0, columnspan=2, sticky='ew', padx=8, pady=(10, 4))
        self.status = Label(self, text='', fg='grey', wraplength=380, justify='left')
        self.status.grid(row=row + 1, column=0, columnspan=2, sticky='ew', padx=8, pady=(0, 8))
        self.bind('<Return>', lambda _event: self.startGeneration())
        self.bind('<KP_Enter>', lambda _event: self.startGeneration())

    def startGeneration(self):
        replace = {key: entry.get_value() for key, entry in self.entries.items()}
        self.generateButton.configure(state='disabled')
        self.status.configure(text='Generating...', fg='grey')
        self.update_idletasks()
        threading.Thread(target=self._generate, args=(replace,), daemon=True).start()

    def _generate(self, replace):
        try:
            generate(self.config_data, replace)
        except Exception as error:
            message, color = f'Failed: {error}', 'firebrick'
        else:
            message, color = f'Done: {self.config_data["out"]}', 'seagreen'
        self.after(0, lambda: self._done(message, color))

    def _done(self, message, color):
        self.status.configure(text=message, fg=color)
        self.generateButton.configure(state='normal')


def main():
    config_data = loadConfig()
    if len(sys.argv) > 1 and sys.argv[1] == '--manual':
        for key, value in config_data['replace'].items():
            print(key + ': ')
            config_data['replace'][key] = input()
            print('\n')
        generate(config_data, config_data['replace'])
    else:
        App(config_data).mainloop()


if __name__ == '__main__':
    main()
