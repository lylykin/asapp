import customtkinter as ctk
from PIL import Image   
    
class TabView(ctk.CTkTabview):
    def __init__(self, master, tab_name_list, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add(tab_name_list[0])
        self.add(tab_name_list[1])

        # add widgets on tabs
        self.widget_compare_canvas_placement(master = self.tab(tab_name_list[0]))
        self.widget_dictionary_placement(master = self.tab(tab_name_list[1]))
    
    def widget_compare_canvas_placement(self, master):
        '''
        Définis les différents widget à placer dans la fenêtre de la tab canvas
        '''
        # Définitions des Widget
        self.canvas_frame = ctk.CTkFrame(master) # Stocke le canvas
        self.kanji_found_frame = ctk.CTkScrollableFrame(master, width= 200, height= 200) # Stocke les kanji et kana proposés par l'app
        self.main_canvas = ctk.CTkCanvas(self.canvas_frame, bg="white", borderwidth=3, cursor="tcross") 
        self.compare_button = ctk.CTkButton(self.canvas_frame, border_width=3, corner_radius=5, anchor="center", text="Comparer le caractère")
        self.clear_button = ctk.CTkButton(self.canvas_frame, border_width=3, corner_radius=5, anchor="center", text="Effacer")
        self.correct_button = ctk.CTkButton(self.canvas_frame, border_width=3, corner_radius=5, anchor="center", text="Corriger")

        # Position des frame dans la tab
        self.canvas_frame.grid(row=0,column=0, sticky="nsew")
        self.kanji_found_frame.grid(row=0,column=1, sticky="nsew")

        # Position des widget dans la canvas_frame
        self.main_canvas.grid(row=0,column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.compare_button.grid(row=1, column = 0, columnspan=2, padx=15, pady=5, sticky="ew") 
        self.clear_button.grid(row=2, column=1, padx=5, pady=5, sticky="e")
        self.correct_button.grid(row=2,column=0,padx=5, pady=5,sticky = "w")

        # Définit la répartition globale de taille des frames pour les colonnes et lignes
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)

    def widget_dictionary_placement(self, master):
        '''
        Définis les différents widget à placer dans la fenêtre de la tab dictionnaire
        '''
        # Définitions des Widget
        self.canvas_frame = ctk.CTkFrame(master) # Stocke le canvas
        self.kanji_found_frame = ctk.CTkScrollableFrame(master, width= 200, height= 200) # Stocke les kanji et kana proposés par l'app
        self.main_canvas = ctk.CTkCanvas(self.canvas_frame, bg="white", borderwidth=3, cursor="tcross") 
        self.compare_button = ctk.CTkButton(self.canvas_frame, border_width=3, corner_radius=5, anchor="center", text="YAY LA TAB 2 GENRE")
        self.clear_button = ctk.CTkButton(self.canvas_frame, border_width=3, corner_radius=5, anchor="center", text="Effacer")
        self.correct_button = ctk.CTkButton(self.canvas_frame, border_width=3, corner_radius=5, anchor="center", text="Corriger")

        # Position des frame dans la tab
        self.canvas_frame.grid(row=0,column=0, sticky="nsew")
        self.kanji_found_frame.grid(row=0,column=1, sticky="nsew")

        # Position des widget dans la canvas_frame
        self.main_canvas.grid(row=0,column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.compare_button.grid(row=1, column = 0, columnspan=2, padx=15, pady=5, sticky="ew") 
        self.clear_button.grid(row=2, column=1, padx=5, pady=5, sticky="e")
        self.correct_button.grid(row=2,column=0,padx=5, pady=5,sticky = "w")

        # Définit la répartition globale de taille des frames pour les colonnes et lignes
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)