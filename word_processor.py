import tkinter as tk
from tkinter import filedialog, messagebox, font
import os

class WordProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Word Processor")
        self.root.geometry("800x600")
        
        # Text widget
        self.text_area = tk.Text(self.root, undo=True)
        self.text_area.pack(expand=True, fill='both')
        
        # Menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        self.edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"))
        self.edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"))
        self.edit_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"))
        
        # Format menu
        self.format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)
        
        # Font family
        self.font_family = tk.StringVar()
        self.font_family.set("Arial")
        self.format_menu.add_command(label="Font", command=self.change_font)
        
        # Font size
        self.font_size = tk.StringVar()
        self.font_size.set("12")
        self.format_menu.add_command(label="Font Size", command=self.change_font_size)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Status Bar", anchor='w')
        self.status_bar.pack(side='bottom', fill='x')
        
        # Bind events
        self.text_area.bind('<KeyRelease>', self.update_status)
        
        # Initialize variables
        self.file_path = None

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.root.title("Untitled - Simple Word Processor")

    def open_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")]
        )
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, file.read())
                self.file_path = file_path
                self.root.title(f"{os.path.basename(file_path)} - Simple Word Processor")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {str(e)}")

    def save_file(self):
        if self.file_path:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(self.file_path, 'w') as file:
                    file.write(content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")]
        )
        if file_path:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(file_path, 'w') as file:
                    file.write(content)
                self.file_path = file_path
                self.root.title(f"{os.path.basename(file_path)} - Simple Word Processor")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def change_font(self):
        font_window = tk.Toplevel(self.root)
        font_window.title("Font")
        
        # Create font family dropdown
        font_families = list(font.families())
        font_family_combo = tk.ttk.Combobox(font_window, textvariable=self.font_family, values=font_families)
        font_family_combo.pack(pady=5)
        
        # Create font size dropdown
        font_sizes = [str(i) for i in range(8, 73, 2)]
        font_size_combo = tk.ttk.Combobox(font_window, textvariable=self.font_size, values=font_sizes)
        font_size_combo.pack(pady=5)
        
        def apply_font():
            current_font = font.Font(
                family=self.font_family.get(),
                size=int(self.font_size.get())
            )
            self.text_area.configure(font=current_font)
            font_window.destroy()
        
        apply_button = tk.Button(font_window, text="Apply", command=apply_font)
        apply_button.pack(pady=5)

    def change_font_size(self):
        size_window = tk.Toplevel(self.root)
        size_window.title("Font Size")
        
        font_sizes = [str(i) for i in range(8, 73, 2)]
        font_size_combo = tk.ttk.Combobox(size_window, textvariable=self.font_size, values=font_sizes)
        font_size_combo.pack(pady=5)
        
        def apply_size():
            current_font = font.Font(
                family=self.font_family.get(),
                size=int(self.font_size.get())
            )
            self.text_area.configure(font=current_font)
            size_window.destroy()
        
        apply_button = tk.Button(size_window, text="Apply", command=apply_size)
        apply_button.pack(pady=5)

    def update_status(self, event=None):
        content = self.text_area.get(1.0, tk.END)
        words = len(content.split())
        chars = len(content) - 1  # Subtract 1 for the extra newline
        self.status_bar.config(text=f"Words: {words} | Characters: {chars}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WordProcessor(root)
    root.mainloop()
