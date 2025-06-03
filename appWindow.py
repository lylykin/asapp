import customtkinter as ctk
from tabview import TabView
from PIL import Image
from controller import Controller
from dictionary import Dictionary


class App(ctk.CTk):
    
    def __init__(self):
        ctk.set_default_color_theme("assets/asapp_theme.json") # Mets un thème custom pour les widget par défaut
        super().__init__()
        self.title("Asapp")
        self.geometry("750x500")
        self.resizable(False,True)

        self.controller = Controller()
        self.dictionary = Dictionary()
        
        self.tab_name_list = ["Identifier un caractère", "Dictionnaire"] # Noms des onglets que l'on donne, impérativement Strings
        self.tab = TabView(self, self.tab_name_list, self.controller)
        for tab_name in self.tab_name_list:
            self.tab._tab_dict[tab_name].grid_configure(ipady=300)
        self.tab._segmented_button.configure(font=ctk.CTkFont(family="Arial", size=12, weight="bold"))

        self.n_strokes = 0 # Nombre de traits dessinés depuis l'init
        self.strokes = {} # Dico stockant les traits tracés sous forme de liste de paires de points associés à un id (1 à infini)
        self.n_kanjis_displayed = {} # Nombre de caractères affichés sur la droite de chaque tab, contient 1 entier associée à chaque tab
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
        self.logo_label = ctk.CTkLabel(self, image=logo, text="") # display image with a CTkLabel
        self.exit_button = ctk.CTkButton(self, border_width=3, corner_radius=5, anchor="center", text="Quitter")
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
        self.tab.compare_button.bind("<Button-1>", lambda event : self.display_possible_kanjis('canvas'))
        self.tab.search_text_button.bind("<Button-1>", lambda event : self.display_possible_kanjis('text'))
        self.appearance_switch.bind("<ButtonPress-1>", self.switch_appearance)
        self.tab.search_text_button.bind("<ButtonPress-1>", self.search_dictionary)

    def canvas_new_stroke(self, event):
        '''
        Mesure un nouveau clic gauche de l'utilisateur sur le canvas
        et ajoute 1 au compteur (initialement nul) des traits tracés.
        '''
        self.n_strokes += 1
        self.strokes[self.n_strokes] = [] # Définis la liste à remplir pour un nouveau trait
    
    def canvas_end_stroke(self, event):
        '''
        Permet d'observer le résultat du stockage des points du tracé
        ! TEMPORAIRE !
        '''
        if self.strokes.get(self.n_strokes, "list_missing") != "list_missing" : # Evite de récupérer des points si la liste de points n'existe pas
            
            print(f"Liste de points :\n{self.strokes[self.n_strokes]}\nNombre de points : {len(self.strokes[self.n_strokes])}")

    def canvas_draw_stroke(self, event):
        '''
        Appelé quand l'utilisateur maintiens le clic sur le canvas.
        Place un point noir aux coordonnées de la souris, puis ajoute les coordonées au dictionnaire des tracés.
        '''
        if self.strokes.get(self.n_strokes, "list_missing") != "list_missing" : # Evite d'ajouter des points si la liste de points n'existe pas
            x = event.x
            y = event.y
            cursor_pos = (x, y) # Récupère les coordonnées de la souris (relativement au 0,0 du canvas)
            self.strokes[self.n_strokes].append(cursor_pos) # Ajoute les coordonnées à la liste de points courante
            self.tab.main_canvas.create_oval(x-1, y-1, x+1, y+1, tags=["user_stroke_dot", f"n_stroke_{self.n_strokes}"], width=4) # Affichage du point

    def end_app(self, event):
        '''
        Termine l'application
        '''
        self.quit()
    
    def clear_canvas(self, event):
        '''
        Supprime tous les points tracés par l'utilisateur (tag : user_stroke_dot) et vide le dictionnaire contenant les tracés.
        '''
        if self.n_strokes > 0 : # Evite de supprimer inutilement
            self.n_strokes = 0
            self.tab.main_canvas.delete("user_stroke_dot")
            self.strokes.clear()
    
    def clear_last_stroke(self, event):
        '''
        Supprime les derniers points du dernier tracé de l'utilisateur
        '''
        int_last_stroke = self.n_strokes
        if int_last_stroke > 0 : # Evite de supprimer inutilement et les bugs
            self.n_strokes += -1
            self.tab.main_canvas.delete(f"n_stroke_{int_last_stroke}")
            self.strokes.pop(int_last_stroke)

    def display_possible_kanjis(self, button : str):
        '''
        Clears the displayed kanjis in corresponding tab (if any), then :
        - fetches the closest kanji to the user's drawing if in canvas tab
        - splits user input text into individual kanji if in dictionary tab
        Then orders their display
        '''
        for display in self.kanjis_displayed_dico.get(button,{}).values():
            display.destroy()
        self.n_kanjis_displayed[button] = 0
        self.kanjis_displayed_dico[button] = {}

        if button == 'canvas':
            client_strokes = self.controller.reduce_dotlist_size(self.controller.drawing_offset(self.strokes)) # Offsets drawing to upper-left corner, then reduces size
            found_kanjis = self.controller.identify(client_strokes) # Returns a list of kanji names (str)
            frame = self.tab.kanji_found_frame

        
        if button == 'text' :
            # Splits input text by whitespace, then makes a single list of every character
            raw_kanjis = self.tab.text_box.get(1.0,ctk.END).split()
            print(raw_kanjis)
            found_kanjis = []
            for s in raw_kanjis :
                for k in s :
                    found_kanjis.append(k)
            frame = self.tab.text_kanji_found_frame

        if found_kanjis == [] : # Si aucun résultat
            self.tab.n_found_label.configure(text="Aucun résultat trouvé")
        else :
            self.tab.n_found_label.configure(text="")
            print(found_kanjis)
            for kanji in found_kanjis:
                self.kanji_frame_create(frame, kanji, button)

    def kanji_frame_create(self, frame, kanji : str, button, widget_size = 40, padxy = 2) :
        '''
        Crée une frame contenant un kanji dans le widget spécifié en frame, selon la taille, l'espace et le kanji spécifié
        S'adapte à la taille du contenant frame
        '''
        widget_and_pad_size = widget_size + padxy
        frame_width = frame.winfo_width() - 100 # Prise en compte du slider de la frame pour l'affichage des widgets
        n_widget_large = frame_width // widget_and_pad_size
        column = self.n_kanjis_displayed[button] % n_widget_large
        row = self.n_kanjis_displayed[button] // n_widget_large

        kanji_frame = ctk.CTkFrame(frame, width=widget_size, height=widget_size, fg_color="white")
        kanji_display = ctk.CTkLabel(kanji_frame, text = kanji, text_color="black", font=(ctk.CTkFont(family="comic sans ms", size=20)))

        kanji_frame.grid(row = row, column = column, padx=padxy, pady=padxy, sticky="nsew")
        kanji_frame.grid_propagate(False)  # Empêche la frame de rétrécir
        kanji_frame.grid_rowconfigure(0, weight=1)
        kanji_frame.grid_columnconfigure(0, weight=1) # Donne la place de frame disponible aux colonnes et lignes 0
        kanji_display.grid(row = 0, column = 0)

        kanji_frame.bind("<ButtonPress-1>", lambda event : self.controller.kanji_tr_tabswitch(self.tab, self.tab_name_list, kanji))
        kanji_display.bind("<ButtonPress-1>", lambda event : self.controller.kanji_tr_tabswitch(self.tab, self.tab_name_list, kanji))
        self.kanjis_displayed_dico[button][self.n_kanjis_displayed[button]] = kanji_frame # Récupère le widget créé dans un dictionnaire
        
        self.n_kanjis_displayed[button] += 1
    
#    def kanji_tr_tabswitch_trigger(self, event) :
#        kanji_frame = event.widget
#        kanji = kanji_frame.kanji_display.text
#        self.controller.kanji_tr_tabswitch(self.tab, self.tab_name_list, kanji)
    # USAGE ? 

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
            
            
    def dico_widget(self, dico, event) : 
        pass
    
    def search_dictionary(self, event):
        """
        Appelée lorsque l'utilisateur appuie sur une touche du clavier, recherche parmis les kanjis existant ou dans le dictionnaire les informations à afficher
        """
        to_search = self.tab.text_box.get(1.0,ctk.END)
        to_search_failsafe_list = to_search.split(sep='\n') # Coupe la liste en ne s'intéressant qu'à la partie avant tout retour à la ligne (\n)
        to_search = to_search_failsafe_list[0]
        if self.tab.last_search != to_search and to_search !="":
            self.tab.last_search = to_search
            # INSERER LE PROCESS DE RECHERCHE
            # Récupérer dans les variables ci-dessous les informations
            found = True # Mettre une condition selon si un caractère ou mot trouvé dans le dico
            if found :
                kanji_name, lang = self.dictionary.translate_language(to_search)
                if lang == "ja":
                    lang = "Mot Français"
                elif lang == "fr":
                    lang = "Mot Japonais"
                kanji_desc = lang + "\n." * 10
                self.tab.kanji_name_label.configure(text=kanji_name)
                self.tab.desc_label.configure(text=kanji_desc)
            else :
                self.tab.kanji_name_label.configure(text="No results found")