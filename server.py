import tkinter as tk
import tkinter.messagebox as messagebox
import random
import tkinter as tk
import time
class PageAccueil:
    def __init__(self, callback):
        self.callback = callback

        self.root = tk.Tk()
        self.root.title("Page d'accueil")

        self.label = tk.Label(self.root, text="Entrez votre nom:" , bg="#f5f5b5")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=10)

        self.button = tk.Button(self.root, text="Commencer la partie", command=self.start_game , bg="#E27A1E" , font=("Helvetica", 12) )
        self.root["bg"]="#f5f5b5"
        self.root.geometry("300x150")
        self.root.resizable(width=False, height=False)
        self.button.pack(pady=10)

    def start_game(self):
        nom_joueur = self.entry.get()
        if nom_joueur:
            self.root.destroy()  # Ferme la fenêtre d'accueil
            self.callback(nom_joueur)  # Appelle la fonction de rappel avec le nom du joueur

    def run(self):
        self.root.mainloop()

class PopupVictoire(tk.Toplevel):
    def __init__(self, vainqueur , master):
        super().__init__()

        self.title("Victoire")
        self.geometry("300x150")
        self.resizable(width=False , height= False)
        self.config()
        label = tk.Label(self, text=f"Le joueur {vainqueur.getNom()} a gagné!", bg="#f5f5b5" , font=("Helvetica", 12))
        label.pack(pady=10)
        bouton_quitter = tk.Button(self, text="QUITTER",command=lambda: self.quitter_toutes_fenetres(master), bg="#E27A1E", font=("Helvetica", 12))
        bouton_quitter.pack(pady=10)
                            
    def quitter_toutes_fenetres(self , master):
        # Obtenez toutes les fenêtres actives et détruisez-les
        for widget in self.winfo_children():
            widget.destroy()
        master.destroy()
            
class Joueur:
        def __init__(self , Nom , pion , couleur):
            self.Nom=Nom
            self.nbpion=9
            self.pion=pion
            self.couleur=couleur
        def eliminer(self):
            self.nbpion-=1
        def rupturePion (self):
            return self.nbpion == 0
        def nbPion( self):
            return self.nbpion
        def getNom ( self):
            return self.Nom
        def getPion(self):
            return self.pion
        def getCouleur(self):
            return self.couleur
class Moulin:
    def __init__(self, master , joueurs):
        self.master = master
        self.joueurs=joueurs
        self.master.title("Jeu du Moulin")
        self.buttons_frame = tk.Frame(self.master)
        self.buttons_frame.place(x=160 , y=120)
        self.buttons = []
        self.main= 0
        self.elimination=False
        self.deplacement=False
        self.pile0= self.creer_colonne_boutons(joueurs[0].getCouleur(), col=40 , row=95)[0]#dessin de la pile des pions pour jouer0
        self.pile1= self.creer_colonne_boutons(joueurs[1].getCouleur() , col=540 , row=95)[0]#dessin de la pile des pions pour jouer1
        self.pions=[]
        self.pions.append(self.creer_colonne_boutons(joueurs[0].getCouleur(), col=40 , row=95)[1])
        self.pions.append(self.creer_colonne_boutons(joueurs[1].getCouleur(), col=540 , row=95)[1])
        self.coordonne=[]# enregistre les coordonné a deplacer 
        self.messageLabel1 = tk.Label(self.master, text=" JEU DU MOULIN " , font=("Helvetica", 12) , bg="#8B4513" , padx=20 , pady=10 )
        self.messageLabel1.place(x=170 , y=15)
        self.messageLabel2 = tk.Label(self.master, text="2023-2024" , font=("Helvetica", 12) , bg="#D2B48C" , padx=20 , pady=10 )
        self.messageLabel2.place(x=170 , y=480)
        self.nomJouer0 =  tk.Label(self.master, text=self.joueurs[0].getNom(), font=("Helvetica", 12) , bg="#D2B48C" , padx=1 , pady=1)
        self.nomJouer0.place(x=30 , y=55)
        self.nomJouer1 =  tk.Label(self.master, text=self.joueurs[1].getNom(), font=("Helvetica", 12) , bg="#8B4513" , padx=1 , pady=1)
        self.nomJouer1.place(x=520 , y=55)
        self.indexBtn =  [(0, 0), (0, 3), (0, 6), (1, 1), (1, 3), (1, 5),
                        (2, 2), (2, 3), (2, 4), (3, 0), (3, 1), (3, 2),
                        (3, 4), (3, 5), (3, 6), (4, 2), (4, 3), (4, 4),
                        (5, 1), (5, 3), (5, 5), (6, 0), (6, 3), (6, 6)]
        
        for i in range(7):
            row_buttons = []
            for j in range(7):
                btn = tk.Button(self.buttons_frame, text=' ', width=4, height=2, command=lambda i=i, j=j: self.place_pion(i, j), bg="#FFFFFF")
                btn.grid(row=i, column=j , padx=0 , pady=0)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
        self.master.geometry("650x650")
        self.master['bg']="#f5f5b5"
        self.set_spaces_unclickable()

        
    def place_pion(self, row, col):
        text= self.buttons[row][col].cget("text") #pour eviter de changer n'importe comment 
        self.messageLabel1.config(bg="#8B4513")
        self.messageLabel2.config(bg="#D2B48C")
        if (self.elimination):
            prob = self.eliminer(row , col , self.joueurs[0] , self.joueurs[1])
            if(not prob):# cas ou eliminer retourne false cest ya un probleme
                self.messageLabel2.config(text="ELIMINE UN PION O !! " , bg="red")
                return
            if( prob == -111):
                pass 
            if (not self.elimination):# dans le cas ou l'elimination engendre un autre alignement
                self.main = (self.main+1) % 2 #Passez la main au prochain
                time.sleep(0.1)
                self.PlacerMachine()
                self.main=0
                self.messageLabel1.config(text="NOMBRE DE O :"+str(self.nbPion("O" , self.buttons)))
                self.messageLabel2.config(text="NOMBRE DE X : "+str(self.nbPion("X" , self.buttons)))
            return
        self.messageLabel1.config(text="NOMBRE DE O :"+str(self.nbPion("O" , self.buttons)))
        self.messageLabel2.config(text="NOMBRE DE X : "+str(self.nbPion("X" , self.buttons)) , bg="#D2B48C")
        if( not self.joueurs[self.main].rupturePion()):
            if ( not self.aligne(row,col)):#SI LE BOUTON N'EST PAS ALIGNE
                if (text ==" "):
                        self.joueurs[self.main].eliminer()#un pion eliminer de la pile
                        self.update_pile(self.pions[self.main] ,self.joueurs[self.main].nbPion())
                        if self.main == 0:
                            self.buttons[row][col].config(text="X" , bg="#D2B48C")
                            if (not self.aligne(row,col)):#si les x deviennent aligné on garde la main
                                self.main=1
                            else:
                                self.elimination = True #il peut modifier les pions du camps adverse  
                
        else:
            if( self.buttons[row][col].cget("text") == self.joueurs[self.main].getPion()):
                self.buttons[row][col].config(relief=tk.SUNKEN)
                self.deplacement=True
                if ( self.nbPion("X", self.buttons)>3):
                    if( self.estCeQuePossible(self.buttons[row][col].cget("text"))):#Dans le cas ou le bouton n'est plus deplacable il a perdu
                        self.messageLabel2.config(text="VEUILLEZ DEPLACER L'UN DES PIONS X \n VERS UNE CASE VERT-CLAIR \n PLUS DE PIONS DISPO" , bg="#00FF00")
                        self.coordonne = self.deplacable(row,col ,"#00FF00")
                        return
                    else:
                        self.afficher_popup_victoire(self.joueurs[(self.main+1)%2])
                else:
                    self.coordonne = [row , col]   #3 eme Phase
            else:
                self.messageLabel2.config(text="VOUS N'AVEZ PLUS DE PIONS DANS LA PILE !\n DEPLACER CEUX SUR LA TABLE" , bg="red")
        if(self.deplacement):
                self.messageLabel1.config(text="NOMBRE DE O :"+str(self.nbPion("O" , self.buttons)))
                self.messageLabel2.config(text="NOMBRE DE X : "+str(self.nbPion("X" , self.buttons)) , bg="#D2B48C")
                eff = self.deplacer(self.coordonne[0:2] , row ,col)# deplacement du Pion
                self.blanchir()
                if (self.aligne(row,col)):
                    self.elimination=True
                else:
                    if(eff):#si le deplacement est effectué
                        self.main = (self.main + 1)%2
                        self.PlacerMachine()
                        self.main=0 
                    else:
                        if( self.nbPion("X" , self.buttons) != 3):
                            self.messageLabel2.config(text="ESSAYER AVEC UN AUTRE PION X ")
                        else:
                            self.messageLabel2.config(text="DEPLACER UN DES PIONS X \n DANS UNE CASE BLANCHE")
                return 
            
        if ( self.main == 1):           
            self.PlacerMachine()
            self.main=0 
            self.messageLabel1.config(text="NOMBRE DE O :"+str(self.nbPion("O" , self.buttons)))
        
    def blanchir(self):
        for i in self.indexBtn:#remettre tous les autres boutons verts blancs
                    if( self.buttons[i[0]][i[1]].cget("bg")=="#00FF00" or  self.buttons[i[0]][i[1]].cget("bg") == "#0a9c53"):
                        self.buttons[i[0]][i[1]].config(bg="#FFFFFF"  ,relief = tk.RAISED)
                        
    def eliminer( self , row , col , eliminant , eliminé):#eliminer un PION ADVERSE
        if(self.buttons[row][col].cget("text") != eliminant.getPion() and self.buttons[row][col].cget("text") != " " ):
            self.buttons[row][col].config(text=" " , bg="#FFFFFF")
            if(not self.aligne(row , col)):
                    self.elimination=False
            if (self.perdre(eliminé.getPion()) and eliminé.nbPion()== 0 ):
                self.afficher_popup_victoire(eliminant)
                return -111   
            return True
        return False
        
    def nbPion(self, pion, tableau):
        nb = 0

        if any(isinstance(row, list) for row in tableau):
            # Tableau à deux dimensions (liste de listes)
            for row in tableau:
                nb += sum(1 for button in row if button.cget("text") == pion)
        else:
            # Tableau à une dimension (simple liste)
            nb = sum(1 for button in tableau if button.cget("text") == pion)

        return nb

    def perdre(self, Pion):
        return self.nbPion(Pion, self.buttons) < 3 or not self.estCeQuePossible(Pion)
    
    def set_spaces_unclickable(self):
        for i in range(7):
            for j in range(7):
                if (i, j) not in [(0, 0), (0, 3), (0, 6), (1, 1), (1, 3), (1, 5),
                               (2, 2), (2, 3), (2, 4), (3, 0), (3, 1), (3, 2),
                               (3, 4), (3, 5), (3, 6), (4, 2), (4, 3), (4, 4),
                               (5, 1), (5, 3), (5, 5), (6, 0), (6, 3), (6, 6)]:
                    self.set_button_unclickable(i, j)

    def set_button_unclickable(self, row, col):
        self.buttons[row][col].config(state=tk.DISABLED, relief=tk.SUNKEN, bd=0, bg="#CCCCCC", highlightbackground="#CCCCCC")
    
    
    def aligne(self, row, col):
        cible = self.buttons[row][col].cget("text")
        coordonnéesBtn = [
            (0, 0), (0, 3), (0, 6),
            (1, 1), (1, 3), (1, 5),
            (2, 2), (2, 3), (2, 4),
            (3, 0), (3, 1), (3, 2),
            (3, 4), (3, 5), (3, 6),
            (4, 2), (4, 3), (4, 4),
            (5, 1), (5, 3), (5, 5),
            (6, 0), (6, 3), (6, 6)
        ]
        if cible != " ":
            # Parcours de la ligne
            listLigne = [coordonnee for coordonnee in coordonnéesBtn if coordonnee[0] == row]
            indexL = listLigne.index((row, col))
            tableau = []
            if 0 <= indexL - 1 < len(listLigne) and 0 <= indexL + 1 < len(listLigne) and listLigne[indexL + 1] != (3, 4) and listLigne[indexL - 1] != (3, 2):  # l'element n'est pas aux abords
                tableau.append(listLigne[indexL - 1])
                tableau.append(listLigne[indexL + 1])
            elif indexL - 1 < 0:  # element colonne 0
                tableau = listLigne[1:3]
            elif indexL + 1 >= len(listLigne):  # element colonne 6
                tableau = listLigne[-3:-1]
            elif 0 <= indexL + 1 < len(listLigne) and listLigne[indexL + 1] != (3, 4):  # element juste avant la case du centre
                tableau = listLigne[indexL + 1:]
            elif listLigne[indexL - 1] != (3, 2):  # element juste apres la case du centre
                 tableau = listLigne[0:2]
            if len(tableau) == 2 and self.buttons[tableau[0][0]][tableau[0][1]].cget("text") == self.buttons[tableau[1][0]][tableau[1][1]].cget("text") == cible:
                return True
            # Parcours de la colonne
            tableau = []
            listCol = [coordonnee for coordonnee in coordonnéesBtn if coordonnee[1] == col]
            indexC = listCol.index((row, col))
            if 0 <= indexC - 1 < len(listCol) and 0 <= indexC + 1 < len(listCol) and listCol[indexC + 1] != (4, 3) and listCol[indexC - 1] != (2, 3):  # l'element n'est pas aux abords
                tableau.append(listCol[indexC - 1])
                tableau.append(listCol[indexC + 1])
            elif indexC - 1 < 0:  # element ligne 0
                tableau = listCol[1:2 + 1]
            elif indexC + 1 >= len(listCol):  # element ligne 6
                tableau = listCol[-3:-1]
            elif 0 <= indexC + 1 < len(listCol) and listCol[indexC + 1] != (4, 3):  # element juste avant la case du centre
                tableau = listCol[indexC + 1:]
            elif listCol[indexC - 1] != (2, 3):  # element juste apres la case du centre
                tableau = listCol[0:2] 
            if len(tableau) == 2 and self.buttons[tableau[0][0]][tableau[0][1]].cget("text") == self.buttons[tableau[1][0]][tableau[1][1]].cget("text") == cible:
                return True
        return False 
    
    def creer_colonne_boutons(self, color , col , row):
        colonne_frame = tk.Frame(self.master)
        colonne_frame.place(x=col , y=row)  
        boutons=[]
        for i in range(9):
            bouton = tk.Button(colonne_frame, text=" ", width=4, height=2, bg=color,state=tk.DISABLED, relief=tk.SUNKEN, bd=0, highlightbackground="#CCCCCC")
            bouton.grid(row=i, column=0, pady=1)
            boutons.append(bouton)
        return (colonne_frame,boutons)

    def update_pile( self , boutons , ind):
        boutons[ind].config(bg="#CCCCCC")
    
    def deplacable( self , row , col , couleur):
            index_btn= [(0, 0), (0, 3), (0, 6), (1, 1), (1, 3), (1, 5),
                        (2, 2), (2, 3), (2, 4), (3, 0), (3, 1), (3, 2),
                        (3, 4), (3, 5), (3, 6), (4, 2), (4, 3), (4, 4),
                        (5, 1), (5, 3), (5, 5), (6, 0), (6, 3), (6, 6)]
            if( (row,col) in index_btn):
                listLigne = [coordonnee for coordonnee in index_btn if coordonnee[0] == row] 
                listCol= [coordonnee for coordonnee in index_btn if coordonnee[1] == col]
                indexligne = listLigne.index((row , col))
                indexCol = listCol.index((row , col ))
                lignebool=False
                colBool=False
                if( self.nbPion(self.joueurs[self.main].getPion() , self.buttons)>3): #CAS DE LA PHASE 2
                    #deplasable ligne
                    if( indexligne != len(listLigne)-1 and self.buttons[listLigne[indexligne+1][0]][listLigne[indexligne+1][1]].cget("text") == " "and listLigne[indexligne+1]!=(3,4) ):
                        self.buttons[listLigne[indexligne+1][0]][listLigne[indexligne+1][1]].config(bg=couleur)
                        lignebool=True
                    if ( indexligne != 0 and self.buttons[listLigne[indexligne-1][0]][listLigne[indexligne-1][1]].cget("text") == " " and listLigne[indexligne-1] != (3 , 2)):
                        self.buttons[listLigne[indexligne-1][0]][listLigne[indexligne-1][1]].config(bg=couleur)
                        lignebool=True
                    #deplacable colonne
                    if( indexCol != len(listCol)-1 and self.buttons[listCol[indexCol+1][0]][listCol[indexCol+1][1]].cget("text")==" " and listCol[indexCol + 1] != (4,3) ):
                        self.buttons[listCol[indexCol+1][0]][listCol[indexCol+1][1]].config(bg=couleur)
                        colBool=True
                    if ( indexCol != 0 and self.buttons[listCol[indexCol-1][0]][listCol[indexCol-1][1]].cget("text") == " " and listCol[indexCol-1] != (2 , 3)):
                        self.buttons[listCol[indexCol-1][0]][listCol[indexCol-1][1]].config(bg=couleur)
                        colBool=True
                    return( row, col , colBool or lignebool)
                if self.nbPion(self.joueurs[self.main].getPion() , self.buttons) == 3:#3eme Phase
                    for index in self.indexBtn:
                        if( self.buttons[index[0]][index[1]].cget("bg") == "#FFFFFF" and self.buttons[index[0]][index[1]].cget("text") == " " ):
                            self.buttons[index[0]][index[1]].config(bg="#00FF00")
                    return ( row , col ,True)
            return(-1,-1 , False)#ECHEC
    
    def deplacer ( self , ancienneCordonne ,row , col):#DEPLACEMENT MANUEL
        selection = False
        print("ancienne Cordonne :" , ancienneCordonne[0])
        if( self.nbPion("X" , self.buttons) > 3):#2 phase
            selection = self.buttons[row][col].cget("text") == " "  and  (self.buttons[row][col].cget("bg")=="#00FF00" )  and self.acote(ancienneCordonne , row , col)
        if (self.nbPion("X" , self.buttons)==3):#3eme phase 
            selection = self.buttons[row][col].cget("text") == " "
        if( selection):
                    self.buttons[row][col].config(text= self.joueurs[self.main].getPion() , bg=self.joueurs[self.main].getCouleur())
                    self.buttons[ancienneCordonne[0]][ancienneCordonne[1]].config(text=' ', bg="#FFFFFF"  ,relief = tk.RAISED)        
                    self.deplacement=False 
                    self.blanchir()
                    return True
            
        return False #ECHEC
       
    def acote( self , ancienneCordonnee , row , col):#deplacement sur la meme ligne ou colonne sinon NOOOON
            return ( row == ancienneCordonnee[0]) or ( col == ancienneCordonnee[1])
        
    def estCeQuePossible( self , Pion):#POSSIBLITE DE DEPLACEMENT 
        possible = False
        index_btn= [(0, 0), (0, 3), (0, 6), (1, 1), (1, 3), (1, 5),
                        (2, 2), (2, 3), (2, 4), (3, 0), (3, 1), (3, 2),
                        (3, 4), (3, 5), (3, 6), (4, 2), (4, 3), (4, 4),
                        (5, 1), (5, 3), (5, 5), (6, 0), (6, 3), (6, 6)] 
        for i in index_btn:
            if(self.buttons[i[0]][i[1]].cget("text") == Pion):
              possible = possible or self.deplacable(i[0],i[1] ,"#0a9c53")[2]
               
        return possible
                
    
    def afficher_popup_victoire(self, vainqueur):#VAINQUEUR
        popup_victoire = PopupVictoire(vainqueur , self.master)
        popup_victoire.transient(self.master)
        popup_victoire.grab_set()

    def cherchePion(self , pion):#PLACE LES PIONS AUTOMATIQUEMENT SOIT POUR ALIGNER SOIT POUR BLOQUER L'ADVERSAIRE
        colonne = []
        for i in range(6):
            nbPionLigne = self.nbPion(pion, self.buttons[i])
            m=0
            if nbPionLigne == 2:
                for j in self.buttons[i]:
                    if j.cget("text") == " " and j.cget("bg") == "#FFFFFF":
                        time.sleep(0.1)
                        j.config(text="O", bg="#8B4513")
                        self.joueurs[self.main].eliminer()#un pion eliminer de la pile
                        self.update_pile(self.pions[1] ,self.joueurs[1].nbPion())
                        return (i , m , True)
                    m+=1
            else:
                colonne = [ligne[i] for ligne in self.buttons]
                nbPionLigne = self.nbPion(pion, colonne)
                if nbPionLigne == 2:
                    for j in colonne:
                        if j.cget("text") == " " and j.cget("bg") == "#FFFFFF":
                            j.config(text="O", bg="#8B4513")
                            self.joueurs[self.main].eliminer()#un pion eliminer de la pile
                            self.update_pile(self.pions[1] ,self.joueurs[1].nbPion())
                            return (m , i ,True) 
                        m+=1   
        return (-1 , -1 , False)
    
    def PlacerMachine(self): #JOUER AUTOMATIQUEMENT
        suite=False
        if( self.joueurs[1].rupturePion()):#deplacer un pion automatiquement
             self.messageLabel1.config(text="NOMBRE DE O :"+str(self.nbPion("O" , self.buttons)))
             ord = self.deplacerMachine()
             self.blanchir()
             if( self.aligne(ord[0] , ord[1])):
                 print("ELIMINATION PAR DEPLACEMENT")
                 el = self.eliminerMachine()
                 self.messageLabel2.config(text="VOUS AVEZ PERDU UN PION !" , bg="red")
             time.sleep(0.1)
             self.messageLabel1.config(text="NOMBRE DE O :"+str(self.nbPion("O" , self.buttons)))
             return
        cordonne = self.cherchePion("O")
        if( cordonne[2]):
            cordO = cordonne[0:2]
            if(self.aligne(cordO[0] , cordO[1])):
                suite = True# 3 pions O sont aligne
                if( suite ):
                    print("ELIMIATION PAR ALIGNEMENT !")
                    el = self.eliminerMachine()
                    self.messageLabel2.config(text="VOUS AVEZ PERDU UN PION !" , bg="red")
            return
        #empecher former un alignement des X
        if( (not suite) and self.cherchePion("X")[2]):
                time.sleep(0.1)
                return True 
        if (not suite):#PLACEMENT ALEATIORE
            coodronne = self.indexBtn[random.randrange(24)]
            while (self.buttons[coodronne[0]][coodronne[1]].cget("text") != " "):
                coodronne = self.indexBtn[random.randrange(24)]
            self.buttons[coodronne[0]][coodronne[1]].config(text="O", bg="#8B4513")
            self.joueurs[self.main].eliminer()#un pion eliminer de la pile
            self.update_pile(self.pions[1] ,self.joueurs[1].nbPion())
            time.sleep(0.1)
            return True

    def deplacerMachine(self):#DEPLACEMENT AUTOMATIQUE
        # Chercher un bouton O deplacable
        for coordonne in self.indexBtn:
            if (self.buttons[coordonne[0]][coordonne[1]].cget("text") == "O" and self.deplacable(coordonne[0], coordonne[1], "#00FF00")[2]):
                    break
        deplacable_btn = None
        for i in self.indexBtn:
            if self.buttons[i[0]][i[1]].cget("bg") == "#00FF00" and self.acote(coordonne , i[0] , i[1]):
                deplacable_btn = i
                break
        if deplacable_btn:
            # Deplacer le bouton O vers le bouton deplacable
            self.buttons[coordonne[0]][coordonne[1]].config(text=' ',bg="#FFFFFF"  )
            self.buttons[deplacable_btn[0]][deplacable_btn[1]].config(text="O", bg="#8B4513")
            time.sleep(0.1)
            return deplacable_btn
        else:
            print(coordonne)
            return (-1 ,-1)
        
    def eliminerMachine( self ):#ELIMINATION AUTOMATIQUE
        coordonne = self.indexBtn[random.randrange(24)]
        while( self.buttons[coordonne[0]][coordonne[1]].cget("text") != "X"):
                    coordonne = self.indexBtn[random.randrange(24)]
        self.buttons[coordonne[0]][coordonne[1]].config(text=" " , bg="#FFFFFF"  ,relief = tk.RAISED)
        perte =self.perdre("X")
        self.blanchir()
        if( perte and self.joueurs[0].rupturePion()):
            self.afficher_popup_victoire(self.joueurs[1])
            return -111   
        return coordonne      

def main():
    # Créer la page d'accueil
    page_accueil = PageAccueil(lambda nom: initialiser_jeu(nom))
    # Exécuter la page d'accueil
    page_accueil.run()

def initialiser_jeu(nom_joueur):
    # Créer une instance du jeu avec le nom du joueur
    root = tk.Tk()
    j0 = Joueur(" "+nom_joueur.upper()+" ", "X", "#D2B48C")
    j1 = Joueur("MACHINE", "O", "#8B4513")
    joueurs = [j0, j1]
    app = Moulin(root, joueurs)
    root.resizable(width=False, height=False)
    root.mainloop()
if __name__ == "__main__":
    main()



  
