import customtkinter as ctk
from tabview import TabView
from PIL import Image
from controller import Controller
from kanji_teach import writeTeacher
from dictionary import Dictionary
from kanji import KanjiDB

class App(ctk.CTk):
    
    def __init__(self):
        ctk.set_default_color_theme("assets/asapp_theme.json") # Mets un thème custom pour les widget par défaut
        super().__init__()
        self.title("Asapp")
        self.geometry("750x500")
        self.resizable(False,True)

        self.controller = Controller()
        self.dictionary = Dictionary()
        
        self.tab_name_list = ["Identifier un caractère", "Dictionnaire","Apprendre l'écriture"] # Noms des onglets que l'on donne, impérativement Strings
        self.tab = TabView(self, self.tab_name_list, self.controller)
        for tab_name in self.tab_name_list:
            self.tab._tab_dict[tab_name].grid_configure(ipady=10)
        self.tab._segmented_button.configure(font=ctk.CTkFont(family="Arial", size=12, weight="bold"))

        self.strokes = [] # Liste stockant les traits tracés sous forme de liste de paires de points
        self.n_kanjis_displayed = {} # Nombre de caractères affichés sur la droite de chaque tab, contient 1 entier associé à chaque tab
        self.kanjis_displayed_dico = {} # Caractères affichés sur la droite de chaque tab (numéro de frame : widget associé)

        self.widget_window_placement()
        self.widget_interact()

    def widget_window_placement(self):
        '''
        Définis les différents widget à placer dans la fenêtre générale
        '''
        # Définitions des variables
        self.appearance = ctk.StringVar(value="dark")

        # Définitions des Widget
        logo = ctk.CTkImage(light_image=Image.open("assets/logo.png"), size=(50, 50))
        # ctk.CTkImage(light_image=Image.open("<path to light mode image>"), dark_image=Image.open("<path to dark mode image>"), size=(30, 30))
        self.logo_label = ctk.CTkLabel(self, image=logo, text="")  # display image with a CTkLabel
        self.exit_button = ctk.CTkButton(self, border_width=3, corner_radius=5, anchor="center", text="Quitter", width=125, height=20)
        #self.appearance_switch = ctk.CTkSwitch(master, textvariable=self.appearance, offvalue="light", onvalue="dark", text="theme", command=self.switch_appearance)
        self.appearance_switch = ctk.CTkSwitch(self, textvariable=self.appearance, variable=self.appearance, offvalue="light", onvalue="dark", text="theme")

        # Définition de l'état des widgets par défaut
        self.appearance_switch.select()

        # Position des widgets dans l'app
        self.logo_label.grid(row=0,column=0)
        self.tab.grid(row = 0, column = 1, rowspan=3, sticky = "nsew", padx=20, pady=20)
        self.exit_button.grid(row=3,column=0, sticky="s")
        self.appearance_switch.grid(row=2, column=0, sticky="s")

        # Définit la répartition globale de taille de l'application pour les colonnes et lignes
        self.grid_rowconfigure(1, weight=20)
        self.grid_columnconfigure(1, weight=20)
        self.grid_rowconfigure((0,2,3), weight=1)
        self.grid_columnconfigure(0, weight=1)

    def widget_interact(self):
        '''
        Définis les liaisons entre les widget et les interactions de l'utilisateur
        '''
        self.tab.main_canvas.bind("<B1-Motion>", self.canvas_draw_stroke) # Détection de mouvement avec clic gauche de la souris sur le canvas
        self.tab.main_canvas.bind("<ButtonPress-1>", self.canvas_new_stroke)
        self.tab.main_canvas.bind("<ButtonRelease-1>", self.canvas_end_stroke) # debug pour l'instant
        self.exit_button.bind("<ButtonPress-1>", self.end_app)
        self.tab.clear_button.bind("<ButtonPress-1>", self.clear_canvas)
        self.tab.correct_button.bind("<ButtonPress-1>", self.clear_last_stroke)
        self.tab.compare_button.bind("<Button-1>", lambda event : self.display_boxes("canvas"))
        self.tab.search_text_button.bind("<Button-1>", lambda event : self.display_boxes("text"))
        self.appearance_switch.bind("<ButtonPress-1>", self.switch_appearance)
        self.appearance_switch.bind("<ButtonPress-1>", self.kanji_check_writing)
        self.tab.teacher_button.bind("<ButtonPress-1>", self.kanji_show_writing)

    def canvas_new_stroke(self, event):
        '''
        Mesure un nouveau clic gauche de l'utilisateur sur le canvas
        et crée la liste de points dans la liste des traits tracés.
        '''
        self.strokes.append([]) # Définit la liste à remplir pour un nouveau trait

    def canvas_draw_stroke(self, event):
        '''
        Appelé quand l'utilisateur maintiens le clic sur le canvas.
        Place un point noir aux coordonnées de la souris, puis ajoute les coordonées au dictionnaire des tracés.
        '''
        if len(self.strokes) != 0 : # Evite d'ajouter des points si la liste de points n'existe pas
            x = event.x
            y = event.y
            cursor_pos = (x, y) # Récupère les coordonnées de la souris (relativement au 0,0 du canvas)
            self.strokes[-1].append(cursor_pos) # Ajoute les coordonnées à la liste de points courante
            self.tab.main_canvas.create_oval(x-1, y-1, x+1, y+1, tags=["user_stroke_dot", f"n_stroke_{len(self.strokes)}"], width=4) # Affichage du point
    
    def canvas_end_stroke(self, event):
        '''
        Permet d'ignorer les clics sans tracé
        '''
        if len(self.strokes) > 0 : # Evite de chercher des points si la liste de points n'existe pas
            if self.strokes[-1] == []:
                self.strokes.pop()

    def end_app(self, event):
        '''
        Termine l'application
        '''
        self.quit()
    
    def clear_canvas(self, event):
        '''
        Supprime tous les points tracés par l'utilisateur (tag : user_stroke_dot) et vide le dictionnaire contenant les tracés.
        '''
        if len(self.strokes) > 0 : # Evite de supprimer inutilement
            self.strokes = []
            self.tab.main_canvas.delete("user_stroke_dot")
            
    
    def clear_last_stroke(self, event):
        '''
        Supprime les derniers points du dernier tracé de l'utilisateur
        '''
        if len(self.strokes) > 0 : # Evite de supprimer inutilement et les bugs 
            self.tab.main_canvas.delete(f"n_stroke_{len(self.strokes)}")
            self.strokes.pop()

    def display_boxes(self, tab, destroy=True):
        '''
        Clears the displayed kanjis in corresponding tab (if any), then :
        - fetches the closest kanji to the user's drawing if in canvas tab
        - splits user input text into individual kanji and displays translation if in dictionary tab
        Then orders their display
        '''
        if destroy :
            for display in self.kanjis_displayed_dico.get(tab,{}).values():
                display.destroy()
            self.n_kanjis_displayed[tab] = 0
            self.kanjis_displayed_dico[tab] = {}

        if tab == "canvas":
            self.display_possible_kanjis()
        elif tab == "text":
            self.display_entry_elements()

    def display_possible_kanjis(self):
        """
        Fetches the closest kanji to the user's drawing
        """
        # Cas du bouton pour comparer les kanjis dans la fenêtre identifier
        client_strokes = (self.controller.drawing_offset(self.strokes)) # Offsets drawing to upper-left corner, then reduces size
        found_kanjis = self.controller.identify(client_strokes) # Returns a list of kanji names (str)
        frame = self.tab.kanji_found_frame

        if found_kanjis == [] : # Si aucun résultat
            self.tab.n_found_label.configure(text="Aucun résultat trouvé")
        else :
            self.tab.n_found_label.configure(text="")
            for kanji in found_kanjis:
                self.kanji_frame_create(frame, kanji) # calls frame create for frame canvas

    def display_entry_elements(self):
        """
        Splits user input text into individual kanji and displays translation
        """
        # Cas du bouton pour découper en caractères l'entrée de recherche dictionnaire
        # Splits input text by whitespace, then makes a single list of every character
        entry = self.tab.text_box.get(1.0,ctk.END).split(sep='\n')[0] # Coupe la liste en ne s'intéressant qu'à la partie avant tout retour à la ligne (\n)
        lang_entry = self.dictionary.async2sync(self.dictionary._get_language(entry)).lang
        if lang_entry == "ja": # Si l'entrée se compose de kanjis
            splitted_entry = list(entry) # Sépare par caractères si japonais
        else :
            splitted_entry = entry.split(sep=" ") # Sépare par mots si français
        found_kanjis = []
        for word in splitted_entry :
            if word != '':
                found_kanjis.append(word)
        frame = self.tab.text_kanji_found_frame

        if found_kanjis == [''] or found_kanjis == []: # Si entrée vide ou aucun mot valide
            self.tab.entry_result_label.configure(text="Entrez du texte pour rechercher")
        else :
            self.search_dictionary(found_kanjis[0]) # Affiche les informations du premier kanji / seul kanji entré
            self.tab.entry_result_label.configure(text="")
            for kanji in found_kanjis:
                self.kanji_frame_create(frame, kanji)

    def kanji_frame_create(self, frame, kanji : str, widget_size = 40, padxy = 2) :
        '''
        Crée une frame contenant un kanji dans le widget spécifié en frame, selon la taille, l'espace et le kanji spécifié
        S'adapte à la taille du contenant frame
        '''
        destroy = True # Définit si les kanjis affichés seront réinitialisé au clic de la kanji_frame
        if frame == self.tab.kanji_found_frame : # correspond à "canvas" ou "text" pour les kanjis affichés dans la tab identification ou dictionnaire respectivement
            display_tab = "canvas"
        elif frame == self.tab.text_kanji_found_frame :
            display_tab = "text"
            destroy = False

        widget_and_pad_size = widget_size + (padxy * 2)
        frame_width = frame.winfo_width()
        # n_widget_large = frame_width // widget_and_pad_size
        n_widget_large = 4
        column = self.n_kanjis_displayed[display_tab] % n_widget_large
        row = self.n_kanjis_displayed[display_tab] // n_widget_large

        kanji_frame = ctk.CTkFrame(frame, width=widget_size, height=widget_size, fg_color="white")
        kanji_display = ctk.CTkLabel(kanji_frame, text = kanji, text_color="black", font=(ctk.CTkFont(family="comic sans ms", size=20)))

        kanji_frame.grid(row = row, column = column, padx=padxy, pady=padxy, sticky="nsew")
        kanji_frame.grid_propagate(False) # Empêche la frame de rétrécir
        kanji_frame.grid_rowconfigure(0, weight=1)
        kanji_frame.grid_columnconfigure(0, weight=1) # Donne la place de frame disponible aux colonnes et lignes 0
        kanji_display.grid(row = 0, column = 0)

        kanji_frame.bind("<ButtonPress-1>", lambda event : self.kanji_tr_tabswitch(kanji,destroy=destroy))
        kanji_display.bind("<ButtonPress-1>", lambda event : self.kanji_tr_tabswitch(kanji,destroy=destroy))
        self.kanjis_displayed_dico[display_tab][self.n_kanjis_displayed[display_tab]] = kanji_frame # Récupère le widget créé dans un dictionnaire
        
        self.n_kanjis_displayed[display_tab] += 1

    def switch_appearance(self, event):
        '''
        Change l'apparence actuelle de l'appli selon la valeur du toggle (light ou dark), se référer à asapp_theme.json
        '''
        appearance_theme = self.appearance.get()
        ctk.set_appearance_mode(appearance_theme)
        print(f"Apparence changée en {appearance_theme}")
    
    def custom_stroke_debug(self, debug_stroke) :
        '''
        DEBUG
        Crée un trait par défaut pour une liste de points
        '''
        for x,y in debug_stroke :
            self.tab.main_canvas.create_oval(x-1, y-1, x+1, y+1, width=4)
    
    def search_dictionary(self, to_search=None):
        """
        Appelée lorsque l'utilisateur appuie sur le bouton de recherche de caractères,
        recherche parmis les kanjis existant ou dans le dictionnaire les informations à afficher
        """
        if to_search is None :
            to_search = self.tab.text_box.get('0.0', "end")
        if self.tab.last_search != to_search:
            self.tab.last_search = to_search
            kanji_name, lang = self.dictionary.translate_language(to_search.split(sep=' ')[0].split(sep='\n')[0])
            if lang == "ja":
                lang = "Mot Français"
            elif lang == "fr":
                lang = "Mot Japonais"
            kanji_desc = lang + "\n." * 6
            self.tab.kanji_name_label.configure(text=kanji_name)
            self.tab.desc_label.configure(text=kanji_desc)
            #self.tab.kanji_name_label.configure(text="No results found") # Cas où aucun résultat trouvé

    def kanji_tr_tabswitch(self, kanji : str, destroy=True):
        '''
        Used when clicking on a proposed kanji frame to switch tab and show its translation
        kanji est le caractère / la chaine correspondant à la frame d'affichage cliquée 
        '''
        self.tab.set(self.tab_name_list[1]) # Passe au deuxième onglet
        self.tab.text_box.delete(0.0,ctk.END) 
        self.tab.text_box.insert(0.0,kanji) # Efface la text_box puis lui rajoute la valeur cliquée
        self.display_boxes("text", destroy=destroy)

    def kanji_show_writing(self, event) : 
        """
        Trace, trait par trait, le kanji entier
        """
        
        kanji = self.tab.teacher_entry.get()
        kanji_db = KanjiDB.the()._kanji_db
        kan = kanji_db[kanji]    
        self.teacher = writeTeacher(kanji=kan)    
        time = 0
        n = 0
        
        while time < self.teacher.total_write_time() : 
            #si le canvas a qqchose affiché
                #le clear
            time += self.teacher.stroke_write_time(n)
            self.custom_stroke_debug(self.teacher.teacher_time(kan.strokes))
            #ensuite l'afficher sur un canvas, mais la je sèche
            n+=1
            
        
    def kanji_check_writing(self, event) : 
        """
        vérifie que le kanji écrit par l'utilisateur est correctement fait, et dans l'ordre
        """
        #récupérer la série de points créée sur le canvas

        return self.teacher.write_teacher(None)
            
        