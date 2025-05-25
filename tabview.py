import customtkinter as ctk
from PIL import Image   
    
class TabView(ctk.CTkTabview):
    def __init__(self, master, tab_name_list, controller, **kwargs):
        super().__init__(master, corner_radius=10, border_width= 10, **kwargs)
        self.controller = controller
        # create tabs
        self.add(tab_name_list[0])
        self.add(tab_name_list[1])
        self.set(tab_name_list[0]) # Tab principale ouverte par défaut

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
        self.compare_button.grid(row=1, column = 0, columnspan=2, padx=16, pady=5, sticky="ew") 
        self.clear_button.grid(row=2, column=1, padx=4, pady=5, sticky="ew")
        self.correct_button.grid(row=2,column=0,padx=4, pady=5,sticky = "ew")

        # Définit la répartition globale de taille des frames pour les colonnes et lignes
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_propagate(False)

    def widget_dictionary_placement(self, master):
        '''
        Définis les différents widget à placer dans la fenêtre de la tab dictionnaire
        /!\\Penser à bien donner des noms différents aux widgets de la tab dictionnaire
        '''
        # Définitions des Widget
        self.menu_button_dictionary = ctk.CTkButton(master, text="Bon le menu là", anchor="center")
        self.desc_frame = ctk.CTkFrame(master, fg_color="dimgray")
        self.kanji_name_label = ctk.CTkLabel(self.desc_frame, text="", font=(ctk.CTkFont(family="comic sans ms", underline=True)))
        self.desc_label = ctk.CTkLabel(self.desc_frame, text="")
        self.kanji_frame_dictionary = ctk.CTkFrame(master, fg_color="white", width=400, height=400)
        self.kanji_display_dictionary = ctk.CTkLabel(self.kanji_frame_dictionary, text = "", text_color="black")

        # Position des frame et widgets dans la tab
        self.menu_button_dictionary.grid(row=2,column=0, sticky="sw")
        self.kanji_display_dictionary.grid(row=0, column=0, sticky="nw")
        self.desc_frame.grid(row=0, column=1, sticky="nsew", rowspan=2, padx=10, pady=10)
        self.kanji_frame_dictionary.grid(row=1, column=0, sticky="ns")

        # Position des widget dans la desc_frame
        self.kanji_name_label.grid(row=0, column = 0, columnspan=2, padx=15, pady=5, sticky="ew") 
        self.desc_label.grid(row=1, column = 0, columnspan=2, padx=15, pady=5, sticky="ew") 

        # Position des widget dans la kanji_frame_dictionary
        self.kanji_display_dictionary.grid(row=0, column=0, sticky="nsew")

        # Définit la répartition globale de taille des frames pour les colonnes et lignes
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_propagate(False)

        #DEBUG
        self.display_kanji_dictionary(':D')
    
    def display_kanji_dictionary(self, kanji):
        '''
        Permet d'afficher et d'ajouter les descriptions noms et apparence des kanjis selon le paramètre d'entrée
        EN DEVELOPPEMENT
        '''
        self.kanji_display_dictionary.configure(text=kanji)
        kanji_desc = "Yosh la description" # A terme : kanji.desc
        kanji_name = "Le nom de fou"
        self.desc_label.configure(text=kanji_desc)
        self.kanji_name_label.configure(text=kanji_name)