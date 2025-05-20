import customtkinter as ctk
from PIL import Image   
    
class TabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("tab 1")
        self.add("tab 2")

        # add widgets on tabs
        self.widgets = self.widget_placement(master = self.tab("tab 1"))
        self.label.grid(row=0, column=0, padx=20, pady=10)
    
    def widget_placement(self, master):
        '''
        Définis les différents widget à placer dans la fenêtre
        '''
        # Définitions des variables
        self.appearance = ctk.StringVar(value="dark")

        # Définitions des Widget
        self.canvas_frame = ctk.CTkFrame(master) # Stocke le canvas
        self.kanji_found_frame = ctk.CTkScrollableFrame(master, width= 200, height= 200) # Stocke les kanji et kana proposés par l'app
        self.main_canvas = ctk.CTkCanvas(self.canvas_frame, bg="white", borderwidth=3, cursor="tcross") 
        logo = ctk.CTkImage(light_image=Image.open("assets/logo.png"), size=(50, 50))
        # ctk.CTkImage(light_image=Image.open("<path to light mode image>"), dark_image=Image.open("<path to dark mode image>"), size=(30, 30))
        self.logo_label = ctk.CTkLabel(master, image=logo, text="App Logo")  # display image with a CTkLabel
        self.compare_button = ctk.CTkButton(self.canvas_frame, border_width=3, corner_radius=5, anchor="center", text="Comparer le caractère")
        self.clear_button = ctk.CTkButton(self.canvas_frame, border_width=3, corner_radius=5, anchor="center", text="Effacer")
        self.correct_button = ctk.CTkButton(self.canvas_frame, border_width=3, corner_radius=5, anchor="center", text="Corriger")
        self.exit_button = ctk.CTkButton(master, border_width=3, corner_radius=5, anchor="center", text="Quitter")
        #self.appearance_switch = ctk.CTkSwitch(master, textvariable=self.appearance, offvalue="light", onvalue="dark", text="theme", command=self.switch_appearance)
        self.appearance_switch = ctk.CTkSwitch(master, textvariable=self.appearance, offvalue="light", onvalue="dark", text="theme")

        # Définition de l'état des widgets par défaut
        self.appearance_switch.select()

        # Position des widgets dans l'app
        self.logo_label.grid(row=0,column=0)
        self.tab.grid(row = 0, column = 1)
        self.canvas_frame.grid(row=1,column=1, sticky="nsew")
        self.kanji_found_frame.grid(row=1,column=3, sticky="nsew")
        self.exit_button.grid(row=3,column=0, sticky="s")
        self.appearance_switch.grid(row=2, column=0, sticky="s")

        # Position des widget dans la canvas_frame
        self.main_canvas.grid(row=0,column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.compare_button.grid(row=1, column = 0, columnspan=2, padx=15, pady=5, sticky="ew") 
        self.clear_button.grid(row=2, column=1, padx=5, pady=5, sticky="e")
        self.correct_button.grid(row=2,column=0,padx=5, pady=5,sticky = "w")

        # Définit la répartition globale de taille de l'application pour les colonnes et lignes
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
