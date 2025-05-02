import tkinter as tk
from tkinter import ttk
import math
from tkinter import messagebox


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Function Calculator")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        # Set the theme and style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('TEntry', font=('Arial', 12))
        self.style.configure('TNotebook', background='#f0f0f0')
        self.style.configure('TFrame', background='#f0f0f0')

        # Create notebook for different calculator types
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Create different tabs for calculator functions
        self.scientific_tab = ttk.Frame(self.notebook)
        self.conversion_tab = ttk.Frame(self.notebook)
        self.stoich_tab = ttk.Frame(self.notebook)
        self.physics_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.scientific_tab, text="Scientific")
        self.notebook.add(self.conversion_tab, text="Conversions")
        self.notebook.add(self.physics_tab, text="Physics")
        self.notebook.add(self.stoich_tab, text="Stoichiometry")
        self.quadratic_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.quadratic_tab, text="Quadratic")

        self.init_scientific_calculator()
        self.init_conversion_calculator()
        self.init_physics_calculator()
        self.init_stoichiometry_calculator()
        self.init_quadratic_calculator()


    def init_scientific_calculator(self):
        # Display frame
        display_frame = ttk.Frame(self.scientific_tab)
        display_frame.pack(fill='x', padx=10, pady=10)

        # Entry widget for display
        self.scientific_display = tk.Entry(display_frame, font=('Arial', 20), justify='right', bd=10)
        self.scientific_display.pack(fill='x')

        # Store the current scientific expression
        self.scientific_expression = ""

        # Button frames
        button_frame = ttk.Frame(self.scientific_tab)
        button_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Define scientific calculator buttons
        sci_buttons = [
            ('sin', 0, 0), ('cos', 0, 1), ('tan', 0, 2), ('√', 0, 3), ('^', 0, 4),
            ('log', 1, 0), ('ln', 1, 1), ('(', 1, 2), (')', 1, 3), ('π', 1, 4),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3), ('C', 2, 4),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3), ('CE', 3, 4),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3), ('e', 4, 4),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3), ('!', 5, 4)
        ]

        # Create and place buttons
        for (text, row, col) in sci_buttons:
            button = ttk.Button(button_frame, text=text, command=lambda t=text: self.scientific_button_click(t))
            button.grid(row=row, column=col, padx=3, pady=3, sticky='nsew')

        # Configure grid to expand
        for i in range(6):
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            button_frame.grid_columnconfigure(i, weight=1)

    def scientific_button_click(self, value):
        if value == '=':
            try:
                # Replace special functions and constants
                expression = self.scientific_expression
                expression = expression.replace('sin', 'math.sin')
                expression = expression.replace('cos', 'math.cos')
                expression = expression.replace('tan', 'math.tan')
                expression = expression.replace('log', 'math.log10')
                expression = expression.replace('ln', 'math.log')
                expression = expression.replace('π', 'math.pi')
                expression = expression.replace('e', 'math.e')
                expression = expression.replace('^', '**')
                expression = expression.replace('√', 'math.sqrt')

                # Handle factorial
                if '!' in expression:
                    # Simple factorial handling
                    for i in range(20, 0, -1):  # Check for factorial from 20! down to 1!
                        if str(i) + '!' in expression:
                            factorial_value = math.factorial(i)
                            expression = expression.replace(str(i) + '!', str(factorial_value))

                # Evaluate the expression and display the result
                result = eval(expression)
                self.scientific_display.delete(0, tk.END)
                self.scientific_display.insert(tk.END, str(result))
                self.scientific_expression = str(result)
            except Exception as e:
                self.scientific_display.delete(0, tk.END)
                self.scientific_display.insert(tk.END, "Error")
                self.scientific_expression = ""
        elif value == 'C':
            # Clear the display and expression
            self.scientific_expression = ""
            self.scientific_display.delete(0, tk.END)
        elif value == 'CE':
            # Clear the last entry
            self.scientific_expression = self.scientific_expression[:-1]
            self.scientific_display.delete(0, tk.END)
            self.scientific_display.insert(tk.END, self.scientific_expression)
        else:
            # Add the value to the expression and display
            self.scientific_expression += value
            self.scientific_display.delete(0, tk.END)
            self.scientific_display.insert(tk.END, self.scientific_expression)

    def init_conversion_calculator(self):
        # Main conversion frame
        main_frame = ttk.Frame(self.conversion_tab)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Create conversion type selection
        ttk.Label(main_frame, text="Select Conversion Type:").grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.conversion_types = ["Length", "Temperature", "Weight/Mass", "Area", "Volume", "Time"]
        self.conv_type_var = tk.StringVar()
        conv_type_combo = ttk.Combobox(main_frame, textvariable=self.conv_type_var, values=self.conversion_types,
                                       state='readonly')
        conv_type_combo.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        conv_type_combo.current(0)  # Default to Length
        conv_type_combo.bind('<<ComboboxSelected>>', self.update_conversion_units)

        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Convert From")
        input_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        ttk.Label(input_frame, text="Value:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.input_value = ttk.Entry(input_frame, width=20)
        self.input_value.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(input_frame, text="Unit:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.from_unit_var = tk.StringVar()
        self.from_unit_combo = ttk.Combobox(input_frame, textvariable=self.from_unit_var, state='readonly')
        self.from_unit_combo.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        # Output frame
        output_frame = ttk.LabelFrame(main_frame, text="Convert To")
        output_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        ttk.Label(output_frame, text="Result:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.output_value = ttk.Entry(output_frame, width=20, state='readonly')
        self.output_value.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(output_frame, text="Unit:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.to_unit_var = tk.StringVar()
        self.to_unit_combo = ttk.Combobox(output_frame, textvariable=self.to_unit_var, state='readonly')
        self.to_unit_combo.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        convert_button = ttk.Button(button_frame, text="Convert", command=self.perform_conversion)
        convert_button.pack(side=tk.LEFT, padx=5)

        clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_conversion)
        clear_button.pack(side=tk.LEFT, padx=5)

        # Initialize conversion units
        self.update_conversion_units()

    def update_conversion_units(self, event=None):
        # Define conversion units based on the selected type
        conversion_units = {
            "Length": ["Meter", "Kilometer", "Centimeter", "Millimeter", "Mile", "Yard", "Foot", "Inch"],
            "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
            "Weight/Mass": ["Kilogram", "Gram", "Milligram", "Pound", "Ounce", "Ton"],
            "Area": ["Square Meter", "Square Kilometer", "Square Centimeter", "Square Mile", "Square Yard",
                     "Square Foot", "Acre", "Hectare"],
            "Volume": ["Cubic Meter", "Cubic Centimeter", "Liter", "Milliliter", "Gallon", "Quart", "Pint", "Cup"],
            "Time": ["Second", "Minute", "Hour", "Day", "Week", "Month", "Year"]
        }

        conv_type = self.conv_type_var.get()
        units = conversion_units.get(conv_type, [])

        # Update from and to unit comboboxes
        self.from_unit_combo['values'] = units
        self.to_unit_combo['values'] = units

        if units:
            self.from_unit_combo.current(0)
            self.to_unit_combo.current(1)

        # Clear any existing values
        self.clear_conversion()

    def clear_conversion(self):
        self.input_value.delete(0, tk.END)
        self.output_value.config(state='normal')
        self.output_value.delete(0, tk.END)
        self.output_value.config(state='readonly')

    def perform_conversion(self):
        try:
            # Get input value and units
            value = float(self.input_value.get())
            from_unit = self.from_unit_var.get()
            to_unit = self.to_unit_var.get()
            conv_type = self.conv_type_var.get()

            # Convert to base unit
            base_value = self.convert_to_base(value, from_unit, conv_type)

            # Convert from base unit to target unit
            result = self.convert_from_base(base_value, to_unit, conv_type)

            # Display the result
            self.output_value.config(state='normal')
            self.output_value.delete(0, tk.END)
            self.output_value.insert(0, f"{result:.8g}")
            self.output_value.config(state='readonly')
        except ValueError:
            self.output_value.config(state='normal')
            self.output_value.delete(0, tk.END)
            self.output_value.insert(0, "Invalid input")
            self.output_value.config(state='readonly')
        except Exception as e:
            self.output_value.config(state='normal')
            self.output_value.delete(0, tk.END)
            self.output_value.insert(0, "Error")
            self.output_value.config(state='readonly')

    def convert_to_base(self, value, unit, conv_type):
        # Convert from given unit to base unit (for each conversion type)
        # Base units: meter, celsius, kilogram, square meter, cubic meter, second

        if conv_type == "Length":
            if unit == "Meter":
                return value
            elif unit == "Kilometer":
                return value * 1000
            elif unit == "Centimeter":
                return value * 0.01
            elif unit == "Millimeter":
                return value * 0.001
            elif unit == "Mile":
                return value * 1609.34
            elif unit == "Yard":
                return value * 0.9144
            elif unit == "Foot":
                return value * 0.3048
            elif unit == "Inch":
                return value * 0.0254

        elif conv_type == "Temperature":
            if unit == "Celsius":
                return value
            elif unit == "Fahrenheit":
                return (value - 32) * 5 / 9
            elif unit == "Kelvin":
                return value - 273.15

        elif conv_type == "Weight/Mass":
            if unit == "Kilogram":
                return value
            elif unit == "Gram":
                return value * 0.001
            elif unit == "Milligram":
                return value * 0.000001
            elif unit == "Pound":
                return value * 0.453592
            elif unit == "Ounce":
                return value * 0.0283495
            elif unit == "Ton":
                return value * 1000

        elif conv_type == "Area":
            if unit == "Square Meter":
                return value
            elif unit == "Square Kilometer":
                return value * 1000000
            elif unit == "Square Centimeter":
                return value * 0.0001
            elif unit == "Square Mile":
                return value * 2589988.11
            elif unit == "Square Yard":
                return value * 0.836127
            elif unit == "Square Foot":
                return value * 0.092903
            elif unit == "Acre":
                return value * 4046.86
            elif unit == "Hectare":
                return value * 10000

        elif conv_type == "Volume":
            if unit == "Cubic Meter":
                return value
            elif unit == "Cubic Centimeter":
                return value * 0.000001
            elif unit == "Liter":
                return value * 0.001
            elif unit == "Milliliter":
                return value * 0.000001
            elif unit == "Gallon":
                return value * 0.00378541
            elif unit == "Quart":
                return value * 0.000946353
            elif unit == "Pint":
                return value * 0.000473176
            elif unit == "Cup":
                return value * 0.000236588

        elif conv_type == "Time":
            if unit == "Second":
                return value
            elif unit == "Minute":
                return value * 60
            elif unit == "Hour":
                return value * 3600
            elif unit == "Day":
                return value * 86400
            elif unit == "Week":
                return value * 604800
            elif unit == "Month":
                return value * 2592000  # Assuming 30-day month
            elif unit == "Year":
                return value * 31536000  # Assuming 365-day year

        return value  # Default fallback

    def convert_from_base(self, base_value, unit, conv_type):
        # Convert from base unit to target unit

        if conv_type == "Length":
            if unit == "Meter":
                return base_value
            elif unit == "Kilometer":
                return base_value / 1000
            elif unit == "Centimeter":
                return base_value / 0.01
            elif unit == "Millimeter":
                return base_value / 0.001
            elif unit == "Mile":
                return base_value / 1609.34
            elif unit == "Yard":
                return base_value / 0.9144
            elif unit == "Foot":
                return base_value / 0.3048
            elif unit == "Inch":
                return base_value / 0.0254

        elif conv_type == "Temperature":
            if unit == "Celsius":
                return base_value
            elif unit == "Fahrenheit":
                return (base_value * 9 / 5) + 32
            elif unit == "Kelvin":
                return base_value + 273.15

        elif conv_type == "Weight/Mass":
            if unit == "Kilogram":
                return base_value
            elif unit == "Gram":
                return base_value / 0.001
            elif unit == "Milligram":
                return base_value / 0.000001
            elif unit == "Pound":
                return base_value / 0.453592
            elif unit == "Ounce":
                return base_value / 0.0283495
            elif unit == "Ton":
                return base_value / 1000

        elif conv_type == "Area":
            if unit == "Square Meter":
                return base_value
            elif unit == "Square Kilometer":
                return base_value / 1000000
            elif unit == "Square Centimeter":
                return base_value / 0.0001
            elif unit == "Square Mile":
                return base_value / 2589988.11
            elif unit == "Square Yard":
                return base_value / 0.836127
            elif unit == "Square Foot":
                return base_value / 0.092903
            elif unit == "Acre":
                return base_value / 4046.86
            elif unit == "Hectare":
                return base_value / 10000

        elif conv_type == "Volume":
            if unit == "Cubic Meter":
                return base_value
            elif unit == "Cubic Centimeter":
                return base_value / 0.000001
            elif unit == "Liter":
                return base_value / 0.001
            elif unit == "Milliliter":
                return base_value / 0.000001
            elif unit == "Gallon":
                return base_value / 0.00378541
            elif unit == "Quart":
                return base_value / 0.000946353
            elif unit == "Pint":
                return base_value / 0.000473176
            elif unit == "Cup":
                return base_value / 0.000236588

        elif conv_type == "Time":
            if unit == "Second":
                return base_value
            elif unit == "Minute":
                return base_value / 60
            elif unit == "Hour":
                return base_value / 3600
            elif unit == "Day":
                return base_value / 86400
            elif unit == "Week":
                return base_value / 604800
            elif unit == "Month":
                return base_value / 2592000  # Assuming 30-day month
            elif unit == "Year":
                return base_value / 31536000  # Assuming 365-day year

        return base_value  # Default fallback

    def init_physics_calculator(self):
        # Main physics frame
        main_frame = ttk.Frame(self.physics_tab)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Create physics calculation type selection
        ttk.Label(main_frame, text="Select Physics Formula:").grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.physics_formulas = [
            "Velocity (v = d/t)",
            "Acceleration (a = Δv/t)",
            "Force (F = m×a)",
            "Weight (W = m×g)",
            "Kinetic Energy (KE = ½m×v²)",
            "Potential Energy (PE = m×g×h)",
            "Work (W = F×d×cosθ)",
            "Power (P = W/t)",
            "Momentum (p = m×v)",
            "Density (ρ = m/V)",
            "Pressure (P = F/A)",
            "Ohm's Law (V = I×R)"
        ]

        self.physics_var = tk.StringVar()
        phys_formula_combo = ttk.Combobox(main_frame, textvariable=self.physics_var,
                                          values=self.physics_formulas, state='readonly', width=25)
        phys_formula_combo.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        phys_formula_combo.current(0)  # Default to velocity
        phys_formula_combo.bind('<<ComboboxSelected>>', self.update_physics_inputs)

        # Input frame for physics parameters
        self.physics_input_frame = ttk.LabelFrame(main_frame, text="Input Parameters")
        self.physics_input_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        # Result frame
        result_frame = ttk.LabelFrame(main_frame, text="Result")
        result_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        ttk.Label(result_frame, text="Result:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.physics_result = ttk.Entry(result_frame, width=30, state='readonly')
        self.physics_result.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        calculate_button = ttk.Button(button_frame, text="Calculate", command=self.calculate_physics)
        calculate_button.pack(side=tk.LEFT, padx=5)

        clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_physics)
        clear_button.pack(side=tk.LEFT, padx=5)

        # Help button for physics formulas
        help_button = ttk.Button(button_frame, text="Formula Help", command=self.show_physics_help)
        help_button.pack(side=tk.LEFT, padx=5)

        # Dictionary to store our input fields
        self.physics_inputs = {}

        # Initialize physics inputs for the default formula (velocity)
        self.update_physics_inputs()

    def update_physics_inputs(self, event=None):
        # Clear existing input fields
        for widget in self.physics_input_frame.winfo_children():
            widget.destroy()

        # Clear the dictionary of input fields
        self.physics_inputs.clear()

        # Set up input fields based on selected formula
        formula = self.physics_var.get()

        if formula == "Velocity (v = d/t)":
            self.create_physics_input("Distance (d)", "meters", 0)
            self.create_physics_input("Time (t)", "seconds", 1)

        elif formula == "Acceleration (a = Δv/t)":
            self.create_physics_input("Initial Velocity (v₀)", "m/s", 0)
            self.create_physics_input("Final Velocity (v)", "m/s", 1)
            self.create_physics_input("Time (t)", "seconds", 2)

        elif formula == "Force (F = m×a)":
            self.create_physics_input("Mass (m)", "kg", 0)
            self.create_physics_input("Acceleration (a)", "m/s²", 1)

        elif formula == "Weight (W = m×g)":
            self.create_physics_input("Mass (m)", "kg", 0)
            self.create_physics_input("Gravity (g)", "m/s²", 1, default_value="9.8")

        elif formula == "Kinetic Energy (KE = ½m×v²)":
            self.create_physics_input("Mass (m)", "kg", 0)
            self.create_physics_input("Velocity (v)", "m/s", 1)

        elif formula == "Potential Energy (PE = m×g×h)":
            self.create_physics_input("Mass (m)", "kg", 0)
            self.create_physics_input("Gravity (g)", "m/s²", 1, default_value="9.8")
            self.create_physics_input("Height (h)", "m", 2)

        elif formula == "Work (W = F×d×cosθ)":
            self.create_physics_input("Force (F)", "N", 0)
            self.create_physics_input("Distance (d)", "m", 1)
            self.create_physics_input("Angle (θ)", "degrees", 2, default_value="0")

        elif formula == "Power (P = W/t)":
            self.create_physics_input("Work (W)", "J", 0)
            self.create_physics_input("Time (t)", "s", 1)

        elif formula == "Momentum (p = m×v)":
            self.create_physics_input("Mass (m)", "kg", 0)
            self.create_physics_input("Velocity (v)", "m/s", 1)

        elif formula == "Density (ρ = m/V)":
            self.create_physics_input("Mass (m)", "kg", 0)
            self.create_physics_input("Volume (V)", "m³", 1)

        elif formula == "Pressure (P = F/A)":
            self.create_physics_input("Force (F)", "N", 0)
            self.create_physics_input("Area (A)", "m²", 1)

        elif formula == "Ohm's Law (V = I×R)":
            self.create_physics_input("Current (I)", "A", 0)
            self.create_physics_input("Resistance (R)", "Ω", 1)

        # Clear the result
        self.clear_physics_result()

    def create_physics_input(self, label_text, unit_text, row, default_value=""):
        # Create label
        ttk.Label(self.physics_input_frame, text=label_text + ":").grid(
            row=row, column=0, padx=5, pady=5, sticky='w')

        # Create entry field
        entry = ttk.Entry(self.physics_input_frame, width=15)
        entry.grid(row=row, column=1, padx=5, pady=5, sticky='ew')

        # Insert default value if provided
        if default_value:
            entry.insert(0, default_value)

        # Create unit label
        ttk.Label(self.physics_input_frame, text=unit_text).grid(
            row=row, column=2, padx=5, pady=5, sticky='w')

        # Store the entry widget in our dictionary
        key = label_text.split('(')[0].strip() if '(' in label_text else label_text
        self.physics_inputs[key] = entry

    def clear_physics(self):
        # Clear all input fields
        for entry in self.physics_inputs.values():
            entry.delete(0, tk.END)

        # Clear the result
        self.clear_physics_result()

    def clear_physics_result(self):
        # Clear the result field
        self.physics_result.config(state='normal')
        self.physics_result.delete(0, tk.END)
        self.physics_result.config(state='readonly')

    def calculate_physics(self):
        try:
            formula = self.physics_var.get()
            result = 0
            unit = ""

            # Calculate based on the selected formula
            if formula == "Velocity (v = d/t)":
                distance = float(self.physics_inputs["Distance"].get())
                time = float(self.physics_inputs["Time"].get())
                result = distance / time
                unit = "m/s"

            elif formula == "Acceleration (a = Δv/t)":
                v0 = float(self.physics_inputs["Initial Velocity"].get())
                v = float(self.physics_inputs["Final Velocity"].get())
                time = float(self.physics_inputs["Time"].get())
                result = (v - v0) / time
                unit = "m/s²"

            elif formula == "Force (F = m×a)":
                mass = float(self.physics_inputs["Mass"].get())
                acceleration = float(self.physics_inputs["Acceleration"].get())
                result = mass * acceleration
                unit = "N"

            elif formula == "Weight (W = m×g)":
                mass = float(self.physics_inputs["Mass"].get())
                gravity = float(self.physics_inputs["Gravity"].get())
                result = mass * gravity
                unit = "N"

            elif formula == "Kinetic Energy (KE = ½m×v²)":
                mass = float(self.physics_inputs["Mass"].get())
                velocity = float(self.physics_inputs["Velocity"].get())
                result = 0.5 * mass * velocity ** 2
                unit = "J"

            elif formula == "Potential Energy (PE = m×g×h)":
                mass = float(self.physics_inputs["Mass"].get())
                gravity = float(self.physics_inputs["Gravity"].get())
                height = float(self.physics_inputs["Height"].get())
                result = mass * gravity * height
                unit = "J"

            elif formula == "Work (W = F×d×cosθ)":
                force = float(self.physics_inputs["Force"].get())
                distance = float(self.physics_inputs["Distance"].get())
                angle_deg = float(self.physics_inputs["Angle"].get())
                angle_rad = math.radians(angle_deg)
                result = force * distance * math.cos(angle_rad)
                unit = "J"

            elif formula == "Power (P = W/t)":
                work = float(self.physics_inputs["Work"].get())
                time = float(self.physics_inputs["Time"].get())
                result = work / time
                unit = "W"

            elif formula == "Momentum (p = m×v)":
                mass = float(self.physics_inputs["Mass"].get())
                velocity = float(self.physics_inputs["Velocity"].get())
                result = mass * velocity
                unit = "kg·m/s"

            elif formula == "Density (ρ = m/V)":
                mass = float(self.physics_inputs["Mass"].get())
                volume = float(self.physics_inputs["Volume"].get())
                result = mass / volume
                unit = "kg/m³"

            elif formula == "Pressure (P = F/A)":
                force = float(self.physics_inputs["Force"].get())
                area = float(self.physics_inputs["Area"].get())
                result = force / area
                unit = "Pa"

            elif formula == "Ohm's Law (V = I×R)":
                current = float(self.physics_inputs["Current"].get())
                resistance = float(self.physics_inputs["Resistance"].get())
                result = current * resistance
                unit = "V"

            # Display the result
            self.physics_result.config(state='normal')
            self.physics_result.delete(0, tk.END)
            self.physics_result.insert(0, f"{result:.6g} {unit}")
            self.physics_result.config(state='readonly')

        except ValueError:
            self.physics_result.config(state='normal')
            self.physics_result.delete(0, tk.END)
            self.physics_result.insert(0, "Invalid input")
            self.physics_result.config(state='readonly')
        except ZeroDivisionError:
            self.physics_result.config(state='normal')
            self.physics_result.delete(0, tk.END)
            self.physics_result.insert(0, "Cannot divide by zero")
            self.physics_result.config(state='readonly')
        except Exception as e:
            self.physics_result.config(state='normal')
            self.physics_result.delete(0, tk.END)
            self.physics_result.insert(0, f"Error: {str(e)}")
            self.physics_result.config(state='readonly')

    def show_physics_help(self):
        # Show help information for the selected formula with examples
        formula = self.physics_var.get()

        help_text = {
            "Velocity (v = d/t)":
                "Velocity (v) = Distance (d) / Time (t)\n\n"
                "This calculates the speed of an object moving in a straight line.\n\n"
                "Example: If a car travels 120 kilometers in 2 hours, its velocity is:\n"
                "v = 120 km ÷ 2 h = 60 km/h",

            "Acceleration (a = Δv/t)":
                "Acceleration (a) = Change in Velocity (Δv) / Time (t)\n\n"
                "This calculates how quickly velocity changes over time.\n\n"
                "Example: If a car accelerates from 0 m/s to 20 m/s in 5 seconds, its acceleration is:\n"
                "a = (20 m/s - 0 m/s) ÷ 5 s = 4 m/s²",

            "Force (F = m×a)":
                "Force (F) = Mass (m) × Acceleration (a)\n\n"
                "Newton's Second Law: The force needed to accelerate an object.\n\n"
                "Example: To accelerate a 1500 kg car at 2 m/s², the force required is:\n"
                "F = 1500 kg × 2 m/s² = 3000 N (Newtons)",

            "Weight (W = m×g)":
                "Weight (W) = Mass (m) × Gravitational acceleration (g)\n\n"
                "The force exerted on an object due to gravity.\n\n"
                "Example: A person with a mass of 70 kg has a weight on Earth of:\n"
                "W = 70 kg × 9.8 m/s² = 686 N (Newtons)",

            "Kinetic Energy (KE = ½m×v²)":
                "Kinetic Energy (KE) = ½ × Mass (m) × Velocity² (v²)\n\n"
                "The energy possessed by an object due to its motion.\n\n"
                "Example: A 1000 kg car moving at 15 m/s has kinetic energy of:\n"
                "KE = ½ × 1000 kg × (15 m/s)² = ½ × 1000 kg × 225 m²/s² = 112,500 J (Joules)",

            "Potential Energy (PE = m×g×h)":
                "Potential Energy (PE) = Mass (m) × Gravity (g) × Height (h)\n\n"
                "The energy possessed by an object due to its position in a gravitational field.\n\n"
                "Example: A 5 kg object raised to a height of 10 meters has potential energy of:\n"
                "PE = 5 kg × 9.8 m/s² × 10 m = 490 J (Joules)",

            "Work (W = F×d×cosθ)":
                "Work (W) = Force (F) × Distance (d) × cos(θ)\n\n"
                "The energy transferred when a force moves an object. θ is the angle between force and displacement.\n\n"
                "Example 1: Pushing a 200 N box for 5 meters (force in same direction as movement):\n"
                "W = 200 N × 5 m × cos(0°) = 200 N × 5 m × 1 = 1000 J\n\n"
                "Example 2: Pulling a 100 N sled at a 30° angle for 10 meters:\n"
                "W = 100 N × 10 m × cos(30°) = 100 N × 10 m × 0.866 = 866 J",

            "Power (P = W/t)":
                "Power (P) = Work (W) / Time (t)\n\n"
                "The rate at which work is done or energy is transferred.\n\n"
                "Example: If a motor does 5000 J of work in 10 seconds, its power output is:\n"
                "P = 5000 J ÷ 10 s = 500 W (Watts)",

            "Momentum (p = m×v)":
                "Momentum (p) = Mass (m) × Velocity (v)\n\n"
                "The quantity of motion of an object.\n\n"
                "Example: A 0.5 kg ball moving at 20 m/s has momentum of:\n"
                "p = 0.5 kg × 20 m/s = 10 kg·m/s",

            "Density (ρ = m/V)":
                "Density (ρ) = Mass (m) / Volume (V)\n\n"
                "The mass per unit volume of a substance.\n\n"
                "Example: If a 200 g (0.2 kg) metal cube has a volume of 25 cm³ (0.000025 m³), its density is:\n"
                "ρ = 0.2 kg ÷ 0.000025 m³ = 8000 kg/m³\n"
                "For comparison: Water has a density of 1000 kg/m³",

            "Pressure (P = F/A)":
                "Pressure (P) = Force (F) / Area (A)\n\n"
                "The force applied perpendicular to the surface of an object per unit area.\n\n"
                "Example: A 75 kg person standing on one foot exerts a force of:\n"
                "F = 75 kg × 9.8 m/s² = 735 N\n"
                "If the footprint area is 0.015 m², the pressure is:\n"
                "P = 735 N ÷ 0.015 m² = 49,000 Pa (Pascals)",

            "Ohm's Law (V = I×R)":
                "Voltage (V) = Current (I) × Resistance (R)\n\n"
                "The relationship between voltage, current, and resistance in an electrical circuit.\n\n"
                "Example: If a circuit has a current of 2 amperes and a resistance of 6 ohms, the voltage is:\n"
                "V = 2 A × 6 Ω = 12 V (Volts)"
        }

        messagebox.showinfo("Physics Formula Help", help_text.get(formula, "Formula information not available."))
    def init_stoichiometry_calculator(self):
        main_frame = ttk.Frame(self.stoich_tab)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Input for mass of A
        ttk.Label(main_frame, text="Known Mass (A):").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.mass_a_entry = ttk.Entry(main_frame, width=15)
        self.mass_a_entry.grid(row=0, column=1, padx=5, pady=5)

        # Input for coefficient of A
        ttk.Label(main_frame, text="Coefficient of A:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.coeff_a_entry = ttk.Entry(main_frame, width=15)
        self.coeff_a_entry.grid(row=2, column=1, padx=5, pady=5)

        # Input for molar mass of A
        ttk.Label(main_frame, text="Molar Mass of A (g/mol):").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.molmass_a_entry = ttk.Entry(main_frame, width=15)
        self.molmass_a_entry.grid(row=3, column=1, padx=5, pady=5)

        # Input for coefficient of B
        ttk.Label(main_frame, text="Coefficient of B:").grid(row=5, column=0, sticky='w', padx=5, pady=5)
        self.coeff_b_entry = ttk.Entry(main_frame, width=15)
        self.coeff_b_entry.grid(row=5, column=1, padx=5, pady=5)

        # Input for molar mass of B
        ttk.Label(main_frame, text="Molar Mass of B (g/mol):").grid(row=6, column=0, sticky='w', padx=5, pady=5)
        self.molmass_b_entry = ttk.Entry(main_frame, width=15)
        self.molmass_b_entry.grid(row=6, column=1, padx=5, pady=5)

        # Result display
        ttk.Label(main_frame, text="Calculated Mass (B):").grid(row=7, column=0, sticky='w', padx=5, pady=10)
        self.mass_b_result = ttk.Entry(main_frame, width=20, state='readonly')
        self.mass_b_result.grid(row=7, column=1, padx=5, pady=10)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=10)
        calc_button = ttk.Button(button_frame, text="Calculate", command=self.perform_stoich_calculation)
        calc_button.pack(side=tk.LEFT, padx=5)
        clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_stoich_inputs)
        clear_button.pack(side=tk.LEFT, padx=5)

    def perform_stoich_calculation(self):
        try:
            mass_a = float(self.mass_a_entry.get())
            coeff_a = float(self.coeff_a_entry.get())
            molar_mass_a = float(self.molmass_a_entry.get())
            coeff_b = float(self.coeff_b_entry.get())
            molar_mass_b = float(self.molmass_b_entry.get())

            # Step 1: mass A -> moles A
            moles_a = mass_a / molar_mass_a
            # Step 2: moles A -> moles B
            moles_b = moles_a * (coeff_b / coeff_a)
            # Step 3: moles B -> mass B
            mass_b = moles_b * molar_mass_b

            self.mass_b_result.config(state='normal')
            self.mass_b_result.delete(0, tk.END)
            self.mass_b_result.insert(0, f"{mass_b:.4g}")
            self.mass_b_result.config(state='readonly')
        except Exception:
            self.mass_b_result.config(state='normal')
            self.mass_b_result.delete(0, tk.END)
            self.mass_b_result.insert(0, "Error")
            self.mass_b_result.config(state='readonly')

    def clear_stoich_inputs(self):
        for entry in [
            self.mass_a_entry, self.formula_a_entry, self.coeff_a_entry, self.molmass_a_entry,
            self.formula_b_entry, self.coeff_b_entry, self.molmass_b_entry
        ]:
            entry.delete(0, tk.END)
        self.mass_b_result.config(state='normal')
        self.mass_b_result.delete(0, tk.END)
        self.mass_b_result.config(state='readonly')


    def init_quadratic_calculator(self):
        main_frame = ttk.Frame(self.quadratic_tab)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Title and explanation
        ttk.Label(main_frame, text="Quadratic Equation Solver", font=('Arial', 12, 'bold')).grid(row=0, column=0,
                                                                                                 columnspan=2, pady=10)
        ttk.Label(main_frame, text="For equation: ax² + bx + c = 0").grid(row=1, column=0, columnspan=2, pady=5)

        # Coefficient inputs
        ttk.Label(main_frame, text="a:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.quad_a = ttk.Entry(main_frame, width=15)
        self.quad_a.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(main_frame, text="b:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.quad_b = ttk.Entry(main_frame, width=15)
        self.quad_b.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(main_frame, text="c:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.quad_c = ttk.Entry(main_frame, width=15)
        self.quad_c.grid(row=4, column=1, padx=5, pady=5, sticky='w')

        # Results section
        result_frame = ttk.LabelFrame(main_frame, text="Results")
        result_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=10, sticky='ew')

        ttk.Label(result_frame, text="Discriminant:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.quad_discriminant = ttk.Entry(result_frame, width=25, state='readonly')
        self.quad_discriminant.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(result_frame, text="x₁:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.quad_x1 = ttk.Entry(result_frame, width=25, state='readonly')
        self.quad_x1.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(result_frame, text="x₂:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.quad_x2 = ttk.Entry(result_frame, width=25, state='readonly')
        self.quad_x2.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)

        solve_button = ttk.Button(button_frame, text="Solve", command=self.solve_quadratic)
        solve_button.pack(side=tk.LEFT, padx=5)

        clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_quadratic)
        clear_button.pack(side=tk.LEFT, padx=5)


    def solve_quadratic(self):
        try:
            a = float(self.quad_a.get())
            b = float(self.quad_b.get())
            c = float(self.quad_c.get())

            # Calculate discriminant
            discriminant = b ** 2 - 4 * a * c

            # Update discriminant display
            self.quad_discriminant.config(state='normal')
            self.quad_discriminant.delete(0, tk.END)
            self.quad_discriminant.insert(0, f"{discriminant:.4g}")
            self.quad_discriminant.config(state='readonly')

            # Calculate roots
            if a == 0:
                if b == 0:
                    # Not a valid equation
                    self.quad_x1.config(state='normal')
                    self.quad_x1.delete(0, tk.END)
                    self.quad_x1.insert(0, "Not a quadratic equation")
                    self.quad_x1.config(state='readonly')

                    self.quad_x2.config(state='normal')
                    self.quad_x2.delete(0, tk.END)
                    self.quad_x2.insert(0, "a cannot be zero")
                    self.quad_x2.config(state='readonly')
                else:
                    # Linear equation
                    x = -c / b
                    self.quad_x1.config(state='normal')
                    self.quad_x1.delete(0, tk.END)
                    self.quad_x1.insert(0, f"{x:.4g}")
                    self.quad_x1.config(state='readonly')

                    self.quad_x2.config(state='normal')
                    self.quad_x2.delete(0, tk.END)
                    self.quad_x2.insert(0, "Linear equation (bx + c = 0)")
                    self.quad_x2.config(state='readonly')
            else:
                if discriminant > 0:
                    # Two real roots
                    x1 = (-b + math.sqrt(discriminant)) / (2 * a)
                    x2 = (-b - math.sqrt(discriminant)) / (2 * a)

                    self.quad_x1.config(state='normal')
                    self.quad_x1.delete(0, tk.END)
                    self.quad_x1.insert(0, f"{x1:.4g}")
                    self.quad_x1.config(state='readonly')

                    self.quad_x2.config(state='normal')
                    self.quad_x2.delete(0, tk.END)
                    self.quad_x2.insert(0, f"{x2:.4g}")
                    self.quad_x2.config(state='readonly')
                elif discriminant == 0:
                    # One real root (repeated)
                    x = -b / (2 * a)

                    self.quad_x1.config(state='normal')
                    self.quad_x1.delete(0, tk.END)
                    self.quad_x1.insert(0, f"{x:.4g}")
                    self.quad_x1.config(state='readonly')

                    self.quad_x2.config(state='normal')
                    self.quad_x2.delete(0, tk.END)
                    self.quad_x2.insert(0, f"{x:.4g} (repeated root)")
                    self.quad_x2.config(state='readonly')
                else:
                    # Complex roots
                    real_part = -b / (2 * a)
                    imag_part = math.sqrt(abs(discriminant)) / (2 * a)

                    self.quad_x1.config(state='normal')
                    self.quad_x1.delete(0, tk.END)
                    self.quad_x1.insert(0, f"{real_part:.4g} + {imag_part:.4g}i")
                    self.quad_x1.config(state='readonly')

                    self.quad_x2.config(state='normal')
                    self.quad_x2.delete(0, tk.END)
                    self.quad_x2.insert(0, f"{real_part:.4g} - {imag_part:.4g}i")
                    self.quad_x2.config(state='readonly')
        except Exception:
            # Handle errors
            self.quad_discriminant.config(state='normal')
            self.quad_discriminant.delete(0, tk.END)
            self.quad_discriminant.insert(0, "Error")
            self.quad_discriminant.config(state='readonly')

            self.quad_x1.config(state='normal')
            self.quad_x1.delete(0, tk.END)
            self.quad_x1.insert(0, "Error")
            self.quad_x1.config(state='readonly')

            self.quad_x2.config(state='normal')
            self.quad_x2.delete(0, tk.END)
            self.quad_x2.insert(0, "Error")
            self.quad_x2.config(state='readonly')


    def clear_quadratic(self):
        self.quad_a.delete(0, tk.END)
        self.quad_b.delete(0, tk.END)
        self.quad_c.delete(0, tk.END)

        self.quad_discriminant.config(state='normal')
        self.quad_discriminant.delete(0, tk.END)
        self.quad_discriminant.config(state='readonly')

        self.quad_x1.config(state='normal')
        self.quad_x1.delete(0, tk.END)
        self.quad_x1.config(state='readonly')

        self.quad_x2.config(state='normal')
        self.quad_x2.delete(0, tk.END)
        self.quad_x2.config(state='readonly')

def main():
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()



if __name__ == "__main__":
    main()