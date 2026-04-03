import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tkinter import Tk, Label, Button, filedialog, StringVar, OptionMenu, messagebox, Frame, Entry, Toplevel, Text, Scrollbar
from tkinter import font as tkFont

class DataVisualizationApp:
    def __init__(self, master):
        self.master = master
        master.title("Data Visualization App")
        master.geometry("700x650")
        master.configure(bg="#eaeaea")

        # Custom font
        self.custom_font = tkFont.Font(family="Helvetica", size=12)

        # Frame for layout
        self.frame = Frame(master, bg="#ffffff", bd=2, relief="groove")
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label = Label(self.frame, text="Choose a CSV or Excel file to visualize:", bg="#ffffff", font=self.custom_font)
        self.label.pack(pady=10)

        self.file_path = StringVar()
        self.file_label = Label(self.frame, textvariable=self.file_path, bg="#ffffff", font=self.custom_font)
        self.file_label.pack(pady=5)

        self.upload_button = Button(self.frame, text="Upload CSV/Excel", command=self.upload_file, bg="#4CAF50", fg="white", font=self.custom_font)
        self.upload_button.pack(pady=10)

        self.plot_type = StringVar(master)
        self.plot_type.set("Select Plot Type")  # default value
        self.plot_menu = OptionMenu(self.frame, self.plot_type, "Histogram", "Boxplot", "Scatter Plot", "Line Plot", "Heatmap", "Pair Plot", command=self.on_plot_type_change)
        self.plot_menu.config(bg="#f0f0f0", font=self.custom_font)
        self.plot_menu.pack(pady=10)

        # Attribute selectors for plotting
        self.attr_frame = Frame(self.frame, bg="#ffffff")
        self.attr_frame.pack(pady=5)

        # For single attribute plots
        self.single_attr_label = Label(self.attr_frame, text="Select Attribute:", bg="#ffffff", font=self.custom_font)
        self.single_attr_var = StringVar(master)
        self.single_attr_menu = OptionMenu(self.attr_frame, self.single_attr_var, "")

        # For two attribute plots (x and y)
        self.x_attr_label = Label(self.attr_frame, text="X Attribute:", bg="#ffffff", font=self.custom_font)
        self.x_attr_var = StringVar(master)
        self.x_attr_menu = OptionMenu(self.attr_frame, self.x_attr_var, "")

        self.y_attr_label = Label(self.attr_frame, text="Y Attribute:", bg="#ffffff", font=self.custom_font)
        self.y_attr_var = StringVar(master)
        self.y_attr_menu = OptionMenu(self.attr_frame, self.y_attr_var, "")

        # Initially hide attribute selectors
        self.hide_attribute_selectors()

        self.plot_button = Button(self.frame, text="Generate Plot", command=lambda: self.plot_data(self.plot_type.get()), bg="#2196F3", fg="white", font=self.custom_font)
        self.plot_button.pack(pady=10)

        # Filter Section
        self.filter_label = Label(self.frame, text="Filter by Column Value:", bg="#ffffff", font=self.custom_font)
        self.filter_label.pack(pady=10)

        self.filter_column = StringVar(master)
        self.filter_column.set("Select Column")  # default value
        self.column_menu = OptionMenu(self.frame, self.filter_column, "Select Column")  # Initialize with a default option
        self.column_menu.config(bg="#f0f0f0", font=self.custom_font)
        self.column_menu.pack(pady=5)

        self.filter_value = StringVar()
        self.filter_entry = Entry(self.frame, textvariable=self.filter_value, bg="#ffffff", font=self.custom_font)
        self.filter_entry.pack(pady=5)

        self.filter_button = Button(self.frame, text="Apply Filter", command=self.apply_filter, bg="#FF9800", fg="white", font=self.custom_font)
        self.filter_button.pack(pady=10)

        # Data Summary Button
        self.summary_button = Button(self.frame, text="Summarize Data", command=self.summarize_data, bg="#9C27B0", fg="white", font=self.custom_font)
        self.summary_button.pack(pady=10)

    def hide_attribute_selectors(self):
        # Hide all attribute selectors initially
        for widget in self.attr_frame.winfo_children():
            widget.pack_forget()

    def show_single_attribute_selector(self):
        self.hide_attribute_selectors()
        self.single_attr_label.pack(side="left", padx=5, pady=2)
        self.single_attr_menu.pack(side="left", padx=5, pady=2)

    def show_two_attribute_selectors(self):
        self.hide_attribute_selectors()
        self.x_attr_label.pack(side="left", padx=5, pady=2)
        self.x_attr_menu.pack(side="left", padx=5, pady=2)
        self.y_attr_label.pack(side="left", padx=10, pady=2)
        self.y_attr_menu.pack(side="left", padx=5, pady=2)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx;*.xls")])
        if file_path:
            self.file_path.set(file_path)
            try:
                ext = os.path.splitext(file_path)[1].lower()
                if ext == ".csv":
                    self.data = pd.read_csv(file_path)
                elif ext in [".xlsx", ".xls"]:
                    self.data = pd.read_excel(file_path)
                else:
                    messagebox.showerror("Error", "Unsupported file type selected.")
                    return
                messagebox.showinfo("Success", "File uploaded successfully!")
                # Update column names for filtering
                self.update_column_names()
                # Update attribute selectors for plotting
                self.update_attribute_menus()
                # Clear any previous filters when new file is loaded
                if hasattr(self, 'filtered_data'):
                    del self.filtered_data
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def update_column_names(self):
        """Update the column names in the filter dropdown."""
        menu = self.column_menu["menu"]
        menu.delete(0, "end")
        for column in self.data.columns:
            menu.add_command(label=column, command=lambda value=column: self.filter_column.set(value))
        # Set the default value to the first column name if available
        if self.data.columns.any():
            self.filter_column.set(self.data.columns[0])

    def update_attribute_menus(self):
        # Update all attribute option menus based on data columns
        columns = list(self.data.columns)
        if not columns:
            return

        # Single attribute
        menu = self.single_attr_menu["menu"]
        menu.delete(0, "end")
        for col in columns:
            menu.add_command(label=col, command=lambda value=col: self.single_attr_var.set(value))
        self.single_attr_var.set(columns[0])

        # X attribute
        menu = self.x_attr_menu["menu"]
        menu.delete(0, "end")
        for col in columns:
            menu.add_command(label=col, command=lambda value=col: self.x_attr_var.set(value))
        self.x_attr_var.set(columns[0])

        # Y attribute
        menu = self.y_attr_menu["menu"]
        menu.delete(0, "end")
        for col in columns:
            menu.add_command(label=col, command=lambda value=col: self.y_attr_var.set(value))
        self.y_attr_var.set(columns[1] if len(columns) > 1 else columns[0])

    def on_plot_type_change(self, selected_plot_type):
        # Show/hide attribute selectors depending on plot type
        if selected_plot_type in ["Histogram", "Boxplot", "Heatmap", "Pair Plot"]:
            self.show_single_attribute_selector()
        elif selected_plot_type in ["Scatter Plot", "Line Plot"]:
            self.show_two_attribute_selectors()
        else:
            self.hide_attribute_selectors()

    def apply_filter(self):
        """Apply the filter based on user input."""
        if not hasattr(self, 'data'):
            messagebox.showwarning("Warning", "No data loaded. Please upload a CSV or Excel file.")
            return

        column = self.filter_column.get()
        value = self.filter_value.get().strip()

        if column and value and column != "Select Column":
            try:
                # Filter the DataFrame, converting both sides to strings for comparison
                self.filtered_data = self.data[self.data[column].astype(str) == value]
                self.file_path.set(f"Filtered Data: {len(self.filtered_data)} rows")
                messagebox.showinfo("Success", f"Filter applied: {len(self.filtered_data)} rows found.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply filter: {e}")
        else:
            messagebox.showwarning("Warning", "Please select a column and enter a value.")

    def plot_data(self, plot_type):
        if not hasattr(self, 'data'):
            messagebox.showwarning("Warning", "No data loaded. Please upload a CSV or Excel file.")
            return

        data_to_plot = getattr(self, 'filtered_data', self.data)

        if plot_type == "Histogram":
            col = self.single_attr_var.get()
            if col not in data_to_plot.columns:
                messagebox.showwarning("Warning", "Selected attribute not in data.")
                return
            self.plot_histogram(data_to_plot, col)
        elif plot_type == "Boxplot":
            col = self.single_attr_var.get()
            if col not in data_to_plot.columns:
                messagebox.showwarning("Warning", "Selected attribute not in data.")
                return
            self.plot_boxplot(data_to_plot, col)
        elif plot_type == "Scatter Plot":
            x_col = self.x_attr_var.get()
            y_col = self.y_attr_var.get()
            if x_col not in data_to_plot.columns or y_col not in data_to_plot.columns:
                messagebox.showwarning("Warning", "Selected attributes not in data.")
                return
            self.plot_scatter(data_to_plot, x_col, y_col)
        elif plot_type == "Line Plot":
            x_col = self.x_attr_var.get()
            y_col = self.y_attr_var.get()
            if x_col not in data_to_plot.columns or y_col not in data_to_plot.columns:
                messagebox.showwarning("Warning", "Selected attributes not in data.")
                return
            self.plot_line(data_to_plot, x_col, y_col)
        elif plot_type == "Heatmap":
            col = self.single_attr_var.get()
            # Heatmap uses correlation matrix, no specific attribute used, but we keep compatibility
            self.plot_heatmap(data_to_plot)
        elif plot_type == "Pair Plot":
            # Pair plot uses all numeric columns, no single attribute needed
            self.plot_pairplot(data_to_plot)
        else:
            messagebox.showwarning("Warning", "Please select a valid plot type.")

    def plot_histogram(self, data, column):
        plt.figure(figsize=(10, 6))
        sns.histplot(data[column], bins=20, kde=True)
        plt.title(f'Histogram of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.show()

    def plot_boxplot(self, data, column):
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=data[column])
        plt.title(f'Boxplot of {column}')
        plt.xlabel(column)
        plt.show()

    def plot_scatter(self, data, x_column, y_column):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=data[x_column], y=data[y_column])
        plt.title(f'Scatter Plot of {x_column} vs {y_column}')
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.show()

    def plot_line(self, data, x_column, y_column):
        plt.figure(figsize=(10, 6))
        sns.lineplot(x=data[x_column], y=data[y_column])
        plt.title(f'Line Plot of {x_column} vs {y_column}')
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.show()

    def plot_heatmap(self, data):
        plt.figure(figsize=(10, 6))
        correlation = data.select_dtypes(include=[np.number]).corr()
        sns.heatmap(correlation, annot=True, cmap='coolwarm')
        plt.title('Heatmap of Correlation Matrix')
        plt.show()

    def plot_pairplot(self, data):
        sns.pairplot(data.select_dtypes(include=[np.number]))
        plt.suptitle('Pair Plot of Data', y=1.02)
        plt.show()

    def summarize_data(self):
        """Display a summary of the data in a new window."""
        if not hasattr(self, 'data'):
            messagebox.showwarning("Warning", "No data loaded. Please upload a CSV or Excel file.")
            return

        data_to_summarize = getattr(self, 'filtered_data', self.data)

        summary_window = Toplevel(self.master)
        summary_window.title("Data Summary")
        summary_window.geometry("800x600")

        text_area = Text(summary_window, wrap="word", font=self.custom_font)
        text_area.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        scrollbar = Scrollbar(summary_window, command=text_area.yview)
        scrollbar.pack(side="right", fill="y")
        text_area['yscrollcommand'] = scrollbar.set

        class StdoutRedirector:
            def __init__(self, text_widget):
                self.text_widget = text_widget

            def write(self, string):
                self.text_widget.insert("end", string)
                self.text_widget.see("end")

            def flush(self):
                pass

        import sys
        sys.stdout = StdoutRedirector(text_area)

        print("Data Summary:\n")
        print(data_to_summarize.describe())
        print("\nData Info:\n")
        data_to_summarize.info()
        print("\nMissing Values:\n")
        print(data_to_summarize.isnull().sum())

        sys.stdout = sys.__stdout__

        text_area.insert("1.0", "Data Summary:\n")
        text_area.insert("end", data_to_summarize.describe().to_string())
        text_area.insert("end", "\n\nData Info:\n")
        import io
        buffer = io.StringIO()
        data_to_summarize.info(buf=buffer)
        s = buffer.getvalue()
        text_area.insert("end", s)

        text_area.insert("end", "\n\nMissing Values:\n")
        text_area.insert("end", data_to_summarize.isnull().sum().to_string())

        text_area.config(state="disabled")


if __name__ == "__main__":
    import sys
    root = Tk()
    app = DataVisualizationApp(root)
    root.mainloop()
