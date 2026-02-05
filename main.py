"""
Hungarian Firm Registry LLM Data Cleaner
Main GUI Application

This application provides a graphical interface for cleaning historical Hungarian
firm registry data using OpenAI's language models.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import threading
from src.data_handler import DataHandler
from src.llm_processor import LLMProcessor
from src.config import AVAILABLE_MODELS, DEFAULT_MODEL, EVENT_TYPES


class FirmRegistryCleanerGUI:
    """Main GUI application"""
    
    def __init__(self, root):
        """Initialize the GUI"""
        self.root = root
        self.root.title("Hungarian Firm Registry LLM Data Cleaner")
        self.root.geometry("1400x900")
        
        # Data components
        self.data_handler = DataHandler()
        self.llm_processor = None
        
        # Processing state
        self.is_processing = False
        self.stop_requested = False
        self.current_row_index = 0
        
        # Setup GUI
        self._setup_menu()
        self._setup_gui()
        
        # Try to initialize LLM processor
        self._initialize_llm()
    
    def _setup_menu(self):
        """Setup menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Excel...", command=self.open_file)
        file_menu.add_command(label="Save Excel", command=self.save_excel)
        file_menu.add_command(label="Save JSON", command=self.save_json)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def _setup_gui(self):
        """Setup main GUI components"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=3)  # Excel viewer
        main_frame.rowconfigure(3, weight=1)  # JSON output
        
        # === Control Panel ===
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="5")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Model selection
        ttk.Label(control_frame, text="OpenAI Model:").grid(row=0, column=0, padx=5)
        self.model_var = tk.StringVar(value=DEFAULT_MODEL)
        self.model_dropdown = ttk.Combobox(
            control_frame,
            textvariable=self.model_var,
            values=AVAILABLE_MODELS,
            state="readonly",
            width=20
        )
        self.model_dropdown.grid(row=0, column=1, padx=5)
        self.model_dropdown.bind("<<ComboboxSelected>>", self.on_model_change)
        
        # Buttons
        ttk.Button(
            control_frame,
            text="📂 Open File",
            command=self.open_file
        ).grid(row=0, column=2, padx=5)
        
        self.lookup_button = ttk.Button(
            control_frame,
            text="🔍 Lookup",
            command=self.lookup_selected_row
        )
        self.lookup_button.grid(row=0, column=3, padx=5)
        
        self.play_button = ttk.Button(
            control_frame,
            text="▶ Play",
            command=self.start_auto_processing
        )
        self.play_button.grid(row=0, column=4, padx=5)
        
        self.stop_button = ttk.Button(
            control_frame,
            text="⏹ Stop",
            command=self.stop_auto_processing,
            state="disabled"
        )
        self.stop_button.grid(row=0, column=5, padx=5)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready. Please open an Excel file.")
        ttk.Label(
            control_frame,
            textvariable=self.status_var,
            foreground="blue"
        ).grid(row=0, column=6, padx=20)
        
        # === Excel Viewer ===
        excel_frame = ttk.LabelFrame(main_frame, text="Excel Data", padding="5")
        excel_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        excel_frame.columnconfigure(0, weight=1)
        excel_frame.rowconfigure(0, weight=1)
        
        # Treeview for Excel data
        self.tree = ttk.Treeview(excel_frame, show="tree headings", selectmode="browse")
        
        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(excel_frame, orient="vertical", command=self.tree.yview)
        tree_scroll_x = ttk.Scrollbar(excel_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_scroll_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        tree_scroll_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)
        
        # === Separator ===
        ttk.Separator(main_frame, orient="horizontal").grid(
            row=2, column=0, sticky=(tk.W, tk.E), pady=10
        )
        
        # === JSON Output ===
        json_frame = ttk.LabelFrame(main_frame, text="LLM Output (JSON)", padding="5")
        json_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        json_frame.columnconfigure(0, weight=1)
        json_frame.rowconfigure(0, weight=1)
        
        self.json_output = scrolledtext.ScrolledText(
            json_frame,
            wrap=tk.WORD,
            width=80,
            height=15,
            font=("Courier", 10)
        )
        self.json_output.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def _initialize_llm(self):
        """Initialize LLM processor with error handling"""
        try:
            self.llm_processor = LLMProcessor(model=self.model_var.get())
            self.status_var.set("Ready. Please open an Excel file.")
        except Exception as e:
            self.status_var.set(f"⚠ LLM Error: {str(e)}")
            messagebox.showerror(
                "API Key Error",
                f"Failed to initialize OpenAI API:\n{str(e)}\n\n"
                "Please ensure your .env file contains a valid OPENAI_API_KEY."
            )
    
    def on_model_change(self, event=None):
        """Handle model selection change"""
        if self.llm_processor:
            self.llm_processor.set_model(self.model_var.get())
            self.status_var.set(f"Model changed to: {self.model_var.get()}")
    
    def open_file(self):
        """Open and load Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("All files", "*.*")
            ],
            initialdir="example_data"
        )
        
        if not file_path:
            return
        
        try:
            self.status_var.set("Loading Excel file...")
            self.root.update()
            
            # Load data
            df = self.data_handler.load_excel(file_path)
            
            # Update treeview
            self._populate_treeview(df)
            
            self.status_var.set(f"Loaded {len(df)} rows from {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
            self.status_var.set("Error loading file")
    
    def _populate_treeview(self, df):
        """Populate treeview with dataframe data"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Setup columns
        columns = list(df.columns)
        self.tree["columns"] = columns
        
        # Format columns
        self.tree.column("#0", width=50, minwidth=50, stretch=False)
        for col in columns:
            self.tree.column(col, width=150, minwidth=100, stretch=True)
            self.tree.heading(col, text=col, anchor=tk.W)
        
        # Add data
        for idx, row in df.iterrows():
            values = [str(val) if val is not None else "" for val in row]
            self.tree.insert("", "end", text=str(idx), values=values)
    
    def on_row_select(self, event=None):
        """Handle row selection in treeview"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            row_text = self.tree.item(item, "text")
            self.current_row_index = int(row_text)
    
    def lookup_selected_row(self):
        """Process the selected row"""
        if not self._validate_ready():
            return
        
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a row to process.")
            return
        
        # Get row index
        item = selection[0]
        row_index = int(self.tree.item(item, "text"))
        
        # Process row in thread to keep GUI responsive
        thread = threading.Thread(target=self._process_single_row, args=(row_index,))
        thread.daemon = True
        thread.start()
    
    def _process_single_row(self, row_index):
        """Process a single row (runs in thread)"""
        try:
            self._update_status(f"Processing row {row_index}...")
            self._disable_buttons()
            
            # Get row data
            row_data = self.data_handler.get_row(row_index)
            
            # Process with LLM
            cleaned_data = self.llm_processor.process_row(row_data)
            
            # Update dataframe
            self.data_handler.update_row(row_index, cleaned_data)
            
            # Update GUI
            self._update_treeview_row(row_index)
            self._display_json(cleaned_data)
            
            self._update_status(f"✓ Processed row {row_index}")
            
        except Exception as e:
            error_msg = f"Error processing row {row_index}: {str(e)}"
            self._update_status(f"✗ {error_msg}")
            self._display_json({"error": str(e)})
            messagebox.showerror("Processing Error", error_msg)
        
        finally:
            self._enable_buttons()
    
    def start_auto_processing(self):
        """Start automatic processing from selected row"""
        if not self._validate_ready():
            return
        
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select starting row.")
            return
        
        # Get starting row
        item = selection[0]
        start_index = int(self.tree.item(item, "text"))
        
        # Confirm
        total_rows = self.data_handler.get_row_count()
        rows_to_process = total_rows - start_index
        
        if not messagebox.askyesno(
            "Confirm Auto-Processing",
            f"Process {rows_to_process} rows starting from row {start_index}?\n\n"
            f"This will use the OpenAI API and may incur costs."
        ):
            return
        
        # Start processing in thread
        self.is_processing = True
        self.stop_requested = False
        thread = threading.Thread(
            target=self._auto_process_rows,
            args=(start_index,)
        )
        thread.daemon = True
        thread.start()
    
    def _auto_process_rows(self, start_index):
        """Auto-process rows from start_index onwards (runs in thread)"""
        try:
            self._update_status("Auto-processing started...")
            self._set_processing_mode(True)
            
            total_rows = self.data_handler.get_row_count()
            
            for row_index in range(start_index, total_rows):
                if self.stop_requested:
                    self._update_status("⏹ Processing stopped by user")
                    break
                
                try:
                    # Update progress
                    progress = f"Processing row {row_index + 1}/{total_rows}"
                    self._update_status(progress)
                    
                    # Select row in GUI
                    self._select_treeview_row(row_index)
                    
                    # Get row data
                    row_data = self.data_handler.get_row(row_index)
                    
                    # Process with LLM
                    cleaned_data = self.llm_processor.process_row(row_data)
                    
                    # Update dataframe
                    self.data_handler.update_row(row_index, cleaned_data)
                    
                    # Update GUI
                    self._update_treeview_row(row_index)
                    self._display_json(cleaned_data)
                    
                except Exception as e:
                    error_msg = f"Error at row {row_index}: {str(e)}"
                    self._update_status(error_msg)
                    self._display_json({"error": str(e)})
                    
                    # Ask user if they want to continue
                    if not messagebox.askyesno(
                        "Error",
                        f"{error_msg}\n\nContinue processing?"
                    ):
                        break
            
            if not self.stop_requested:
                self._update_status("✓ Auto-processing completed")
                messagebox.showinfo("Complete", "All rows processed successfully!")
            
        finally:
            self.is_processing = False
            self.stop_requested = False
            self._set_processing_mode(False)
    
    def stop_auto_processing(self):
        """Request stop of auto-processing"""
        self.stop_requested = True
        self._update_status("Stopping after current row...")
    
    def _validate_ready(self):
        """Check if system is ready to process"""
        if self.llm_processor is None:
            messagebox.showerror(
                "Not Ready",
                "LLM processor not initialized. Check your API key."
            )
            return False
        
        if self.data_handler.get_row_count() == 0:
            messagebox.showwarning(
                "No Data",
                "Please load an Excel file first."
            )
            return False
        
        return True
    
    def _update_treeview_row(self, row_index):
        """Update a specific row in the treeview"""
        df = self.data_handler.get_dataframe()
        row = df.iloc[row_index]
        
        # Find item in treeview
        for item in self.tree.get_children():
            if self.tree.item(item, "text") == str(row_index):
                values = [str(val) if val is not None else "" for val in row]
                self.tree.item(item, values=values)
                break
    
    def _select_treeview_row(self, row_index):
        """Select a specific row in treeview (thread-safe)"""
        def select():
            for item in self.tree.get_children():
                if self.tree.item(item, "text") == str(row_index):
                    self.tree.selection_set(item)
                    self.tree.see(item)
                    break
        
        self.root.after(0, select)
    
    def _display_json(self, data):
        """Display JSON data in output textbox (thread-safe)"""
        def display():
            self.json_output.delete(1.0, tk.END)
            json_str = json.dumps(data, ensure_ascii=False, indent=2)
            self.json_output.insert(1.0, json_str)
        
        self.root.after(0, display)
    
    def _update_status(self, message):
        """Update status label (thread-safe)"""
        self.root.after(0, lambda: self.status_var.set(message))
    
    def _disable_buttons(self):
        """Disable processing buttons (thread-safe)"""
        def disable():
            self.lookup_button.config(state="disabled")
            self.play_button.config(state="disabled")
        
        self.root.after(0, disable)
    
    def _enable_buttons(self):
        """Enable processing buttons (thread-safe)"""
        def enable():
            if not self.is_processing:
                self.lookup_button.config(state="normal")
                self.play_button.config(state="normal")
        
        self.root.after(0, enable)
    
    def _set_processing_mode(self, processing):
        """Set GUI to processing mode (thread-safe)"""
        def set_mode():
            if processing:
                self.lookup_button.config(state="disabled")
                self.play_button.config(state="disabled")
                self.stop_button.config(state="normal")
                self.model_dropdown.config(state="disabled")
            else:
                self.lookup_button.config(state="normal")
                self.play_button.config(state="normal")
                self.stop_button.config(state="disabled")
                self.model_dropdown.config(state="readonly")
        
        self.root.after(0, set_mode)
    
    def save_excel(self):
        """Save processed data to Excel"""
        if self.data_handler.get_row_count() == 0:
            messagebox.showwarning("No Data", "No data to save.")
            return
        
        try:
            output_path = self.data_handler.save_excel()
            messagebox.showinfo("Saved", f"Excel file saved to:\n{output_path}")
            self.status_var.set(f"✓ Saved to {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save Excel:\n{str(e)}")
    
    def save_json(self):
        """Save processed data to JSON"""
        if self.data_handler.get_row_count() == 0:
            messagebox.showwarning("No Data", "No data to save.")
            return
        
        try:
            output_path = self.data_handler.save_json()
            messagebox.showinfo("Saved", f"JSON file saved to:\n{output_path}")
            self.status_var.set(f"✓ Saved to {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save JSON:\n{str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Hungarian Firm Registry LLM Data Cleaner
Version 1.0

A tool for cleaning historical Hungarian firm registry data
from "Központi Értesítő" using OpenAI's language models.

Event Classification:
1 - Firm birth
2 - Firm death  
3 - Ownership change
4 - Management change
5 - Legal status change
6 - Other

© 2026"""
        
        messagebox.showinfo("About", about_text)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = FirmRegistryCleanerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
