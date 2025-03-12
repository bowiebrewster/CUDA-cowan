import tkinter as tk
from tkinter import ttk

# Function to generate the control card
def generate_control_card():
    control_card = (
        f"{itpow_options[itpow.get()]} {iptvu_options[iptvu.get()]} {ipteb_options[ipteb.get()]} {norbpt_options[norbpt.get()]}  "
        f"{tolstb_options[tolstb.get()]} {tolend_options[tolend.get()]} {thresh_options[thresh.get()]} {kutd_options[kutd.get()]}  "
        f"{maxit_options[maxit.get()]} {npr_options[npr.get()]} {exf10_options[exf10.get()]} {exfm1_options[exfm1.get()]}  "
        f"{emx_options[emx.get()]} {corrf_options[corrf.get()]} {iw6_options[iw6.get()]}"
    )
    with open("control_card.txt", "w") as file:
        file.write(control_card)
    print("Control card generated and saved as 'control_card.txt'.")
    root.destroy()


# Create the main window
root = tk.Tk()
root.title("Control Card Generator")

# Add a frame for the dropdown menus
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky="W")

# Dictionary-style options for dropdown menus
itpow_options = {
    "Print SCF iteration information (NITER, DELT, ALFM)": "1",
    "Call POWER to print <r**m>": "2",
    "Print SCF iteration information and call POWER": "3",
    "Special option for debugging": "200+90",
}

iptvu_options = {
    "Do not print Fk and Gk": "0",
    "Print Fk and Gk": "1",
    "Print Fk, Gk, and Coulomb interaction energies": "2",
    "Print Fk, Gk, Coulomb energies, and wavefunction overlap integrals": "3",
    "Print Fk, Gk, Coulomb energies, overlap integrals, and HFS potentials": "4",
    "Print Fk, Gk, Coulomb energies, overlap integrals, HFS potentials, and HX/HF potentials": "5",
    "Print all above and relativistic contribution to potential": "6",
}

ipteb_options = {
    "Do not print eigenvalues": "0",
    "Print eigenvalues (EE, JJJ, R(JJJ), AZ)": "1",
    "Print eigenvalues and kinetic energy (Ekin)": "2",
}

norbpt_options = {
    "Do not print wavefunctions": "-9",
    "Print first two and last wavefunctions at every fifth mesh point": "01.",
    "Print first two and last two wavefunctions at every fifth mesh point": "02.",
    "Print first two and last three wavefunctions at every fifth mesh point": "03.",
    "Print first two and last four wavefunctions at every fifth mesh point": "04.",
    "Print first two and last five wavefunctions at every fifth mesh point": "05.",
    "Print all wavefunctions": "9",
}

tolstb_options = {
    "Stabilization tolerance = 0.2": "0.2",
    "Stabilization tolerance = 0.5": "0.5",
    "Stabilization tolerance = 1.0": "1.0",
}

tolend_options = {
    "Maximum change in potential = 5.E-08": "5.E-08",
    "Maximum change in potential = 1.E-06": "1.E-06",
    "Maximum change in potential = 1.E-04": "1.E-04",
}

thresh_options = {
    "Maximum fractional change in eigenvalue = 1.E-11": "1.E-11",
    "Maximum fractional change in eigenvalue = 1.E-09": "1.E-09",
    "Maximum fractional change in eigenvalue = 1.E-07": "1.E-07",
}

kutd_options = {
    "Hartree-Slater (HS) calculation": "-2",
    "Hartree-plus-statistical-exchange (HX) calculation": "-1",
    "Hartree-Fock-Slater (HFS) calculation with tail cutoff": "0",
    "Hartree-Fock-Slater (HFS) calculation without tail cutoff": "1",
}

maxit_options = {
    "Maximum SCF iterations = 90": "90",
    "Maximum SCF iterations = 100": "100",
    "Maximum SCF iterations = 150": "150",
    "Maximum SCF iterations = 190": "190",
}

npr_options = {
    "No diagnostic printing during SCF iteration": "0",
    "Print diagnostic potentials and wavefunctions": "1",
    "Print detailed diagnostic information": "2",
}

exf10_options = {
    "Slater's exchange coefficient = 1.0 (Kohn and Sham)": "1.0",
    "Slater's exchange coefficient = 1.5 (Slater's original value)": "1.5",
}

exfm1_options = {
    "Exchange coefficient = 0.65": "0.65",
    "Exchange coefficient = 0.7": "0.7",
    "Exchange coefficient = 0.8": "0.8",
}

emx_options = {
    "No continuum wavefunction calculations": "0.0",
    "Continuum wavefunction calculations with EMX = 0.1": "0.1",
    "Continuum wavefunction calculations with EMX = 0.5": "0.5",
}

corrf_options = {
    "No correlation potential (CORRF = 0.0)": "0.0",
    "Standard correlation potential (CORRF = 1.0)": "1.0",
    "Exaggerated correlation potential (CORRF = 1.5)": "1.5",
    "Highly exaggerated correlation potential (CORRF = 2.0)": "2.0",
}

iw6_options = {
    "No output to monitor screen": "-6",
    "Output to monitor screen": "0",
    "Detailed output to monitor screen": "6",
}

# Labels and dropdown menus
ttk.Label(frame, text="ITPOW (Controls printed output):").grid(row=0, column=0, sticky="W")
itpow = ttk.Combobox(frame, values=list(itpow_options.keys()))
itpow.grid(row=0, column=1, sticky="W")
itpow.set("Call POWER to print <r**m>")  # Default value

ttk.Label(frame, text="IPTVU (Controls printing of Fk and Gk integrals):").grid(row=1, column=0, sticky="W")
iptvu = ttk.Combobox(frame, values=list(iptvu_options.keys()))
iptvu.grid(row=1, column=1, sticky="W")
iptvu.set("Do not print Fk and Gk")  # Default value

ttk.Label(frame, text="IPTEB (Controls printing of eigenvalues):").grid(row=2, column=0, sticky="W")
ipteb = ttk.Combobox(frame, values=list(ipteb_options.keys()))
ipteb.grid(row=2, column=1, sticky="W")
ipteb.set("Do not print eigenvalues")  # Default value

ttk.Label(frame, text="NORBPT (Controls wavefunction printing):").grid(row=3, column=0, sticky="W")
norbpt = ttk.Combobox(frame, values=list(norbpt_options.keys()))
norbpt.grid(row=3, column=1, sticky="W")
norbpt.set("Do not print wavefunctions")  # Default value

ttk.Label(frame, text="TOLSTB (Stabilization tolerance for SCF iteration):").grid(row=4, column=0, sticky="W")
tolstb = ttk.Combobox(frame, values=list(tolstb_options.keys()))
tolstb.grid(row=4, column=1, sticky="W")
tolstb.set("Stabilization tolerance = 0.2")  # Default value

ttk.Label(frame, text="TOLEND (Maximum change in potential for SCF iteration):").grid(row=5, column=0, sticky="W")
tolend = ttk.Combobox(frame, values=list(tolend_options.keys()))
tolend.grid(row=5, column=1, sticky="W")
tolend.set("Maximum change in potential = 5.E-08")  # Default value

ttk.Label(frame, text="THRESH (Maximum fractional change in eigenvalue):").grid(row=6, column=0, sticky="W")
thresh = ttk.Combobox(frame, values=list(thresh_options.keys()))
thresh.grid(row=6, column=1, sticky="W")
thresh.set("Maximum fractional change in eigenvalue = 1.E-11")  # Default value

ttk.Label(frame, text="KUTD (Type of calculation, e.g., Hartree-Slater):").grid(row=7, column=0, sticky="W")
kutd = ttk.Combobox(frame, values=list(kutd_options.keys()))
kutd.grid(row=7, column=1, sticky="W")
kutd.set("Hartree-Slater (HS) calculation")  # Default value

ttk.Label(frame, text="MAXIT (Maximum number of SCF iterations):").grid(row=8, column=0, sticky="W")
maxit = ttk.Combobox(frame, values=list(maxit_options.keys()))
maxit.grid(row=8, column=1, sticky="W")
maxit.set("Maximum SCF iterations = 190")  # Default value

ttk.Label(frame, text="NPR (Diagnostic printing during SCF iteration):").grid(row=9, column=0, sticky="W")
npr = ttk.Combobox(frame, values=list(npr_options.keys()))
npr.grid(row=9, column=1, sticky="W")
npr.set("No diagnostic printing during SCF iteration")  # Default value

ttk.Label(frame, text="EXF10 (Coefficient for Slater's exchange term):").grid(row=10, column=0, sticky="W")
exf10 = ttk.Combobox(frame, values=list(exf10_options.keys()))
exf10.grid(row=10, column=1, sticky="W")
exf10.set("Slater's exchange coefficient = 1.0 (Kohn and Sham)")  # Default value

ttk.Label(frame, text="EXFM1 (Coefficient for exchange term):").grid(row=11, column=0, sticky="W")
exfm1 = ttk.Combobox(frame, values=list(exfm1_options.keys()))
exfm1.grid(row=11, column=1, sticky="W")
exfm1.set("Exchange coefficient = 0.65")  # Default value

ttk.Label(frame, text="EMX (Used for continuum wavefunction calculations):").grid(row=12, column=0, sticky="W")
emx = ttk.Combobox(frame, values=list(emx_options.keys()))
emx.grid(row=12, column=1, sticky="W")
emx.set("No continuum wavefunction calculations")  # Default value

ttk.Label(frame, text="CORRF (Multiplying factor for correlation potential):").grid(row=13, column=0, sticky="W")
corrf = ttk.Combobox(frame, values=list(corrf_options.keys()))
corrf.grid(row=13, column=1, sticky="W")
corrf.set("Standard correlation potential (CORRF = 1.0)")  # Default value

ttk.Label(frame, text="IW6 (Controls output to monitor screen):").grid(row=14, column=0, sticky="W")
iw6 = ttk.Combobox(frame, values=list(iw6_options.keys()))
iw6.grid(row=14, column=1, sticky="W")
iw6.set("No output to monitor screen")  # Default value




# Button to generate the control card
generate_button = ttk.Button(frame, text="Generate Control Card", command=generate_control_card)
generate_button.grid(row=15, column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()