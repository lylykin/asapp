import customtkinter as ctk
from PIL import Image

class App(ctk.CTk):
    def __init__(self):
        ctk.set_default_color_theme("assets/asapp_theme.json") # Mets un thème custom pour les widget par défaut
        super().__init__()
        self.title("Asapp")
        self.geometry("650x420")

        self.n_strokes = 0 # Nombre de traits dessinés depuis l'init
        self.strokes = {} # Dico stockant les traits tracés sous forme de liste de paires de points associés à un id (1 à infini)

        self.widget_placement()
        self.widget_interact()

    def widget_placement(self):
        '''
        Définis les différents widget à placer dans la fenêtre
        '''
        # Définitions des variables
        self.appearance = ctk.StringVar(value="dark")

        # Définitions des Widget
        self.canvas_frame = ctk.CTkFrame(self) # Stocke le canvas
        self.kanji_found_frame = ctk.CTkScrollableFrame(self) # Stocke les kanji et kana proposés par l'app
        self.main_canvas = ctk.CTkCanvas(self.canvas_frame, bg="white", borderwidth=3, cursor="tcross") 
        logo = ctk.CTkImage(light_image=Image.open("assets/logo.png"), size=(50, 50))
        # ctk.CTkImage(light_image=Image.open("<path to light mode image>"), dark_image=Image.open("<path to dark mode image>"), size=(30, 30))
        self.logo_label = ctk.CTkLabel(self, image=logo, text="App Logo")  # display image with a CTkLabel
        self.compare_button = ctk.CTkButton(self.canvas_frame, border_width=3, corner_radius=5, anchor="center", text="Comparer le caractère")
        self.clear_button = ctk.CTkButton(self.canvas_frame, border_width=3, corner_radius=5, anchor="center", text="Effacer")
        self.correct_button = ctk.CTkButton(self.canvas_frame, border_width=3, corner_radius=5, anchor="center", text="Corriger")
        self.exit_button = ctk.CTkButton(self, border_width=3, corner_radius=5, anchor="center", text="Quitter")
        self.appearance_switch = ctk.CTkSwitch(self, textvariable=self.appearance, offvalue="light", onvalue="dark", text="theme", command=self.switch_appearance)

        # Définition de l'état des widgets par défaut
        self.appearance_switch.select()

        # Position des widgets dans l'app
        self.logo_label.grid(row=0,column=0)
        self.canvas_frame.grid(row=1,column=1, sticky="nsew")
        self.kanji_found_frame.grid(row=1,column=3, sticky="nsew")
        self.exit_button.grid(row=3,column=0, sticky="s")
        self.appearance_switch.grid(row=2, column=0, sticky="s")

        # Position des widget dans la canvas_frame
        self.main_canvas.grid(row=0,column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.compare_button.grid(row=1, column = 0, columnspan=2, padx=15, pady=5, sticky="ew") 
        self.clear_button.grid(row=2, column=1, padx=5, pady=5, sticky="e")
        self.correct_button.grid(row=2,column=0,padx=5, pady=5,sticky = "w")

    def widget_interact(self):
        '''
        Définis les liaisons entre les widget et les interactions de l'utilisateur
        '''
        self.main_canvas.bind("<B1-Motion>", self.canvas_draw_stroke) # Détection de mouvement avec clic gauche de la souris sur le canvas
        self.main_canvas.bind("<ButtonPress-1>", self.canvas_new_stroke)
        self.main_canvas.bind("<ButtonRelease-1>", self.canvas_end_stroke) # debug pour l'instant
        self.exit_button.bind("<ButtonPress-1>", self.end_app)
        self.clear_button.bind("<ButtonPress-1>", self.clear_canvas)
        self.correct_button.bind("<ButtonPress-1>", self.clear_last_stroke)

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
            self.main_canvas.create_oval(x-1, y-1, x+1, y+1, tags=["user_stroke_dot", f"n_stroke_{self.n_strokes}"], width=4) # Affichage du point

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
            self.main_canvas.delete("user_stroke_dot")
            self.strokes.clear()
    
    def clear_last_stroke(self, event):
        '''
        Supprime les derniers points du dernier tracé de l'utilisateur
        '''
        int_last_stroke = self.n_strokes
        if int_last_stroke > 0 : # Evite de supprimer inutilement et les bugs
            self.n_strokes += -1
            self.main_canvas.delete(f"n_stroke_{int_last_stroke}")
            self.strokes.pop(int_last_stroke)
    
    def switch_appearance(self):
        '''
        Change l'apparence actuelle de l'appli selon la valeur du toggle (light ou dark), se référer à asapp_theme.json
        '''
        appearance_theme = self.appearance.get()
        ctk.set_appearance_mode(appearance_theme)
        print(f"Apparence changée en {appearance_theme}")
