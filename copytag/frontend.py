import backend
import service
from diagnostics import install_diagnostics_logging
import logging
from logging_config import setup_logging
import tkinter as tk
from tkinter import ttk, filedialog

setup_logging()


class TagCopierApp:
	def __init__(self, root):
		self.root = root
		self.root.title("Tag Copier")
		self.root.geometry("1000x600")
		
		# Criar frame principal
		main_frame = ttk.Frame(root, padding="10")
		main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
		
		# Source Directory
		ttk.Label(main_frame, text="Source Directory:").grid(row=0, column=0, sticky=tk.W)
		self.source_var = tk.StringVar()
		ttk.Entry(main_frame, textvariable=self.source_var, width=50).grid(row=0, column=1, padx=5)
		ttk.Button(main_frame, text="Browse", command=self.browse_source).grid(row=0, column=2)
		
		# Destination Directory
		ttk.Label(main_frame, text="Destination Directory:").grid(row=1, column=0, sticky=tk.W)
		self.dest_var = tk.StringVar()
		ttk.Entry(main_frame, textvariable=self.dest_var, width=50).grid(row=1, column=1, padx=5)
		ttk.Button(main_frame, text="Browse", command=self.browse_dest).grid(row=1, column=2)
		
		# Buttons
		button_frame = ttk.Frame(main_frame)
		button_frame.grid(row=2, column=0, columnspan=3, pady=10)
		ttk.Button(button_frame, text="Generate CSV", command=self.generate_csv).pack(side=tk.LEFT, padx=5)
		ttk.Button(button_frame, text="Copy Tags", command=self.copy_tags).pack(side=tk.LEFT, padx=5)
		
		# Treeview para mostrar dados
		self.tree = ttk.Treeview(main_frame, columns=("Origin", "Origin File", "Tag", "Dest File", "Destination"))
		self.tree.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
		
		# Configurar colunas
		for col in ("Origin", "Origin File", "Tag", "Dest File", "Destination"):
			self.tree.heading(col, text=col)
			
		# Scrollbar
		scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
		scrollbar.grid(row=3, column=3, sticky=(tk.N, tk.S))
		self.tree.configure(yscrollcommand=scrollbar.set)

	def browse_source(self):
		directory = filedialog.askdirectory()
		self.source_var.set(directory)

	def browse_dest(self):
		directory = filedialog.askdirectory()
		self.dest_var.set(directory)

	def generate_csv(self):
		# Implementar lógica do CSV
		pass

	def copy_tags(self):
		# Implementar lógica de cópia
		pass


def main():
    try:
        install_diagnostics_logging()
    except Exception:
        # Continue even if diagnostics cannot be installed
        pass
    logging.info("Starting Tkinter frontend main window")
    root = tk.Tk()
    app = TagCopierApp(root)
    root.mainloop()

if __name__ == '__main__':
	main()
