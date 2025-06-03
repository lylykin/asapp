import customtkinter as ctk
from PIL import Image   
    
class TabView(ctk.CTkTabview):
    def __init__(self, master, tab_name_list, controller, **kwargs):
        super().__init__(master, corner_radius=10, border_width= 10, height=400, width=700, **kwargs) # 
        self.controller = controller
        # create tabs
        self.add(tab_name_list[0])
        self.add(tab_name_list[1])
        self.set(tab_name_list[0]) # Tab principale ouverte par défaut

        # Définit la répartition globale de taille des frames pour les colonnes et lignes
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_propagate(True)

        # add widgets on tabs
        self.widget_compare_canvas_placement(master = self.tab(tab_name_list[0]))
        self.widget_dictionary_placement(master = self.tab(tab_name_list[1]))
    
    def widget_compare_canvas_placement(self, master):
        '''
        Définis les différents widget à placer dans la fenêtre de la tab canvas
        '''
        # Définition et position de la frame centrale contenant la tab
        #self.center_frame_compare_canvas = ctk.CTkFrame(master)
        #self.center_frame_compare_canvas.grid(row=0,column=0, padx=10, pady=10, sticky="nsew")
        #self.center_frame_compare_canvas.grid_rowconfigure(0, weight=1)
        #self.center_frame_compare_canvas.grid_propagate(True)

        # Définitions des Widget
        self.canvas_frame = ctk.CTkFrame(master) # Stocke le canvas
        self.kanji_found_frame = ctk.CTkScrollableFrame(master, fg_color="dimgray", width= 215, height= 375) # Stocke les kanji et kana proposés par l'app
        self.main_canvas = ctk.CTkCanvas(self.canvas_frame, bg="white", borderwidth=3, cursor="tcross", width=310, height=270) 
        self.compare_button = ctk.CTkButton(self.canvas_frame, border_width=3, corner_radius=5, anchor="center", text="Comparer le caractère")
        self.clear_button = ctk.CTkButton(self.canvas_frame, border_width=3, corner_radius=5, anchor="center", text="Effacer")
        self.correct_button = ctk.CTkButton(self.canvas_frame, border_width=3, corner_radius=5, anchor="center", text="Corriger")
        self.n_found_label = ctk.CTkLabel(self.kanji_found_frame, text="")
        self.teacher_frame = ctk.CTkFrame(master)
        self.teacher_button = ctk.CTkButton(self.teacher_frame, border_width=3, corner_radius=5, anchor="center", text="Apprendre à écrire le kanji", width=125, height=20)
        self.teacher_entry = ctk.CTkEntry(self.teacher_frame)

        # Position des frame dans la tab
        self.canvas_frame.grid(row=0,column=0, sticky="nsew")
        self.teacher_frame.grid(row=1, column=0, sticky="esw")
        self.kanji_found_frame.grid(row=0,column=1, rowspan=2, sticky="nsew")

        # Position des widget dans la teacher_frame
        self.teacher_button.grid(row = 0, column = 0, sticky = "s")
        self.teacher_entry.grid(row = 0, column = 1, sticky = "s")

        # Position des widget dans la canvas_frame
        self.main_canvas.grid(row=0,column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.compare_button.grid(row=1, column = 0, columnspan=2, padx=16, pady=5, sticky="ew") 
        self.clear_button.grid(row=2, column=1, padx=4, pady=5, sticky="ew")
        self.correct_button.grid(row=2,column=0,padx=4, pady=5,sticky = "ew")

        # Position des widget dans la canvas_frame
        self.n_found_label.grid(row=0,column=0, sticky='nsew')

        # Définit la répartition globale de taille des frames pour les colonnes et lignes
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_propagate(True)

    def widget_dictionary_placement(self, master):
        '''
        Définis les différents widget à placer dans la fenêtre de la tab dictionnaire
        /!\\Penser à bien donner des noms différents aux widgets de la tab dictionnaire
        '''
        self.last_search = "" # Dernière recherche effectuée dans le dictionnaire

        # Définitions des Widget
        self.text_frame = ctk.CTkFrame(master) # Stocke la zone de texte
        self.text_kanji_found_frame = ctk.CTkScrollableFrame(master, fg_color="dimgray", width= 215, height= 210) # Stocke les kanji et kana proposés par l'app
        self.text_box = ctk.CTkTextbox(self.text_frame, width=300, height=150, wrap='word') # Textbox est la version améliorée d'un simple Entry
        self.search_text_button = ctk.CTkButton(self.text_frame, border_width=3, corner_radius=5, anchor="center", text="Chercher les caractères")
        self.desc_frame = ctk.CTkFrame(master, fg_color="dimgray", width= 540, height= 165) # Changer à une couleur dynamique réactive au thème
        self.kanji_name_label = ctk.CTkLabel(self.desc_frame, text="", font=(ctk.CTkFont(family="comic sans ms", weight="bold")))
        self.desc_label = ctk.CTkLabel(self.desc_frame, text="")
        self.entry_result_label = ctk.CTkLabel(self.text_kanji_found_frame, text="")
        
        # Position des frame dans la tab
        self.text_frame.grid(row=0,column=0, sticky="nsew")
        self.text_kanji_found_frame.grid(row=0,column=1, sticky="nsew")
        self.desc_frame.grid(row=1, column = 0, columnspan=2, sticky="ew")

        # Position des widget dans la text_frame
        self.text_box.grid(row=0,column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.search_text_button.grid(row=1, column = 0, columnspan=2, padx=16, pady=5, sticky="ew")

        # Position des widget dans la desc_frame
        self.kanji_name_label.grid(row=0, column = 0, padx=15, pady=5, sticky="ew") 
        self.desc_label.grid(row=1, column = 0, padx=15, pady=5, sticky="ew") 

        # Position des widget dans la text_kanji_found_frame
        self.entry_result_label.grid(row=0,column=0, sticky='nsew')

        # Définit la répartition globale de taille des frames pour les colonnes et lignes
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_propagate(True)

        #DEBUG
        self.display_kanji_dictionary(':D')
    
    def display_kanji_dictionary(self, kanji):
        '''
        Permet d'afficher et d'ajouter les descriptions noms et apparence des kanjis selon le paramètre d'entrée
        EN DEVELOPPEMENT
        '''
        #self.kanji_display_dictionary.configure(text=kanji)
        kanji_desc = ""
        kanji_name = ""
        self.desc_label.configure(text=kanji_desc)
        self.kanji_name_label.configure(text=kanji_name)