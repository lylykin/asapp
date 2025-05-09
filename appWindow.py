import customtkinter as ctk
from PIL import Image

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Asapp")
        self.geometry("600x600")
        self.widget_placement()
        self.widget_interact()

        self.n_strokes = 0 # Nombre de traits dessinés depuis l'init
        self.strokes = {} # Dico stockant les traits tracés sous forme de liste de paires de points associés à un id (1 à infini)
        
    def widget_placement(self):
        '''
        Définis les différents widget à placer dans la fenêtre
        '''
        self.main_canvas = ctk.CTkCanvas(width=800, height=800, bg="white")
        logo = ctk.CTkImage(light_image=Image.open("assets/logo.png"), size=(30, 30))
        # (light_image=Image.open("<path to light mode image>"), dark_image=Image.open("<path to dark mode image>"), size=(30, 30))
        self.logo_label = ctk.CTkLabel(self, image=logo, text="App Logo")  # display image with a CTkLabel

        self.logo_label.grid(row=0,column=0)
        self.main_canvas.grid(row=1,column=1)

    def widget_interact(self):
        '''
        Définis les liaisons entre les widget et les interactions de l'utilisateur
        '''
        self.main_canvas.bind("<B1-Motion>", self.canvas_draw_stroke) # Détection de mouvement avec clic gauche de la souris sur le canvas
        self.main_canvas.bind("<ButtonPress-1>", self.canvas_new_stroke)
        self.main_canvas.bind("<ButtonRelease-1>", self.canvas_end_stroke) # debug pour l'instant

    def canvas_new_stroke(self, event):
        '''
        Mesure un nouveau clic gauche de l'utilisateur et ajoute 1 au compteur (initialement nul) des traits tracés
        '''
        self.n_strokes += 1
        self.strokes[self.n_strokes] = [] # Définis la liste à remplir pour un nouveau trait
    
    def canvas_end_stroke(self, event):
        '''
        Permet d'observer le résultat du stockage des points du tracé
        ! temporaire !
        '''
        print(self.strokes[self.n_strokes])

    def canvas_draw_stroke(self, event):
        x = event.x
        y = event.y
        cursor_pos = (x, y) # Récupère les coordonnées de la souris (relativement au 0,0 du canvas)
        self.strokes[self.n_strokes].append(cursor_pos) # Ajoute les coordonnées à la liste de points courante
        self.main_canvas.create_oval(x-1, y-1, x+1, y+1, fill='black', width=4) # Affichage du point
        print(f"pos : {cursor_pos}, n_strokes : {self.n_strokes}") # DEBUG


asapp = App()
asapp.mainloop()

