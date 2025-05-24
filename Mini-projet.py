import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import csv
import os


UTILISATEURS = {
    "ISMAIL": "2006",
    "MOUAD": "2005"
}

def verifier_auth(username, password):
    return username in UTILISATEURS and UTILISATEURS[username] == password

def afficher_erreur(parent):
    messagebox.showerror("Erreur", "Identifiants incorrects", parent=parent)


FICHIER_CSV = "data/collection_jeux.csv"
CHAMPS = ["titre", "studio", "annee", "genre", "plateforme"]

def initialiser_fichier():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(FICHIER_CSV):
        with open(FICHIER_CSV, "w") as f:
            writer = csv.DictWriter(f, fieldnames=CHAMPS)
            writer.writeheader()

def ajouter_jeu(donnees):
    with open(FICHIER_CSV, "a") as f:
        writer = csv.DictWriter(f, fieldnames=CHAMPS)
        writer.writerow(donnees)

def lister_jeux():
    jeux = []
    with open(FICHIER_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            jeux.append(row)
    return jeux

def rechercher_jeux(critere, valeur):
    resultats = []
    with open(FICHIER_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if valeur.lower() in row[critere].lower():
                resultats.append(row)
    return resultats

def supprimer_jeu(titre):
    lignes = []
    with open(FICHIER_CSV, "r") as f:
        reader = csv.DictReader(f)
        lignes = [row for row in reader]

    with open(FICHIER_CSV, "w") as f:
        writer = csv.DictWriter(f, fieldnames=CHAMPS)
        writer.writeheader()
        for ligne in lignes:
            if ligne["titre"] != titre:
                writer.writerow(ligne)

def creer_interface_login(root):
 
    bg_color = "#1a1a2e" 
    btn_color = "#4cc9f0"  
    text_color = "#ffffff"  
    
    root.configure(bg=bg_color)
    
    frame_login = tk.Frame(root, bg=bg_color)
    frame_login.pack(pady=100)
    

    logo_label = tk.Label(frame_login, text="🎮 ", font=("Arial", 50), bg=bg_color)
    logo_label.grid(row=0, columnspan=2, pady=10)
    

    title_label = tk.Label(frame_login, text="Connexion", font=("Arial", 16, "bold"), bg=bg_color, fg=text_color)
    title_label.grid(row=1, columnspan=2, pady=10)
    

    tk.Label(frame_login, text="Name of admin:", bg=bg_color, fg=text_color).grid(row=2, column=0, padx=5, pady=5)
    entry_username = tk.Entry(frame_login)
    entry_username.grid(row=2, column=1, padx=5, pady=5)
    

    tk.Label(frame_login, text="Password:", bg=bg_color, fg=text_color).grid(row=3, column=0, padx=5, pady=5)
    entry_password = tk.Entry(frame_login, show="*")
    entry_password.grid(row=3, column=1, padx=5, pady=5)
    

    def connexion():
        if verifier_auth(entry_username.get(), entry_password.get()):
            frame_login.destroy()
            creer_interface_principale(root)
        else:
            afficher_erreur(frame_login)
    
    btn_login = tk.Button(frame_login, text="Connexion", command=connexion,bg=btn_color, fg="black", relief=tk.RAISED, borderwidth=3,font=("Arial", 10, "bold"))
    btn_login.grid(row=4, columnspan=2, pady=10, ipadx=10)




def creer_interface_principale(root):
  
    bg_color = "#1a1a2e"  
    btn_color = "#4cc9f0"
    text_color = "#ffffff" 
    highlight_color = "#f72585"  
    
    root.configure(bg=bg_color)
    
  
    header_frame = tk.Frame(root, bg=bg_color)
    header_frame.pack(fill=tk.X, pady=10)
    
    logo_label = tk.Label(header_frame, text="🎮", font=("Arial", 30), bg=bg_color)
    logo_label.pack(side=tk.LEFT, padx=20)
    
    title_label = tk.Label(header_frame, text="Gestion de Collection de Jeux",font=("Arial", 16, "bold"), bg=bg_color, fg=highlight_color)
    title_label.pack(side=tk.LEFT)

  
    frame_form = tk.Frame(root, bg=bg_color)
    frame_form.pack(pady=10, fill=tk.X)
    
    entries = {}
    for i, champ in enumerate(CHAMPS):
        tk.Label(frame_form, text=f"{champ.title()}:", bg=bg_color, fg=text_color).grid(row=i//3, column=(i%3)*2, padx=5, pady=5, sticky="e")
        entries[champ] = tk.Entry(frame_form, width=25)
        entries[champ].grid(row=i//3, column=(i%3)*2+1, padx=5, pady=5, sticky="w")


    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Treeview", 
                    background="#16213e",
                    foreground=text_color,
                    rowheight=25,
                    fieldbackground="#16213e",
                    borderwidth=0)
    style.map('Treeview', 
              background=[('selected', highlight_color)],
              foreground=[('selected', 'white')])
    
    tree = ttk.Treeview(root, columns=CHAMPS, show="headings", height=15)
    for champ in CHAMPS:
        tree.heading(champ, text=champ.title())
        tree.column(champ, width=150)
    
    tree.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

 
    def effacer_champs():
        for entry in entries.values():
            entry.delete(0, tk.END)
    
    def afficher_jeux():
        for item in tree.get_children():
            tree.delete(item)
        for jeu in lister_jeux():
            tree.insert("", tk.END, values=[jeu[c] for c in CHAMPS])
    
    def ajouter_jeu_ui():
        donnees = {k: v.get() for k, v in entries.items()}
        if not all(donnees.values()):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis")
            return
        try:
            annee = int(donnees["annee"])
            if annee < 1970 or annee > 2027:
                raise ValueError
           
        except ValueError:
            messagebox.showerror("Erreur", "Année (1970-2027) ")
            return
        
        ajouter_jeu(donnees)
        effacer_champs()
        afficher_jeux()
        messagebox.showinfo("Succès", "Jeu ajouté à la collection!")

  
    frame_recherche = tk.Frame(root, bg=bg_color)
    frame_recherche.pack(pady=5)

    tk.Label(frame_recherche, text="Critère:", bg=bg_color, fg=text_color).grid(row=0, column=0, padx=5, pady=5)
    critere_var = tk.StringVar(value="titre")
    options = ["titre", "studio", "genre", "plateforme"]
    menu_critere = tk.OptionMenu(frame_recherche, critere_var, *options)
    menu_critere.config(bg=bg_color, fg=text_color, highlightbackground=bg_color)
    menu_critere.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_recherche, text="Valeur:", bg=bg_color, fg=text_color).grid(row=0, column=2, padx=5, pady=5)
    entry_valeur = tk.Entry(frame_recherche)
    entry_valeur.grid(row=0, column=3, padx=5, pady=5)

    def rechercher_jeux_ui():
        resultats = rechercher_jeux(critere_var.get(), entry_valeur.get())
        for item in tree.get_children():
            tree.delete(item)
        for jeu in resultats:
            tree.insert("", tk.END, values=[jeu[c] for c in CHAMPS])
    
    def supprimer_jeu_ui():
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Aucun jeu sélectionné")
            return
        titre = tree.item(selection[0])["values"][0]
        if messagebox.askyesno("Confirmation", f"Supprimer '{titre}' de la collection?"):
            supprimer_jeu(titre)
            afficher_jeux()

   
    frame_btn = tk.Frame(root, bg=bg_color)
    frame_btn.pack(pady=10)
    
    actions = [
        ("Ajouter", ajouter_jeu_ui),
        ("Afficher tout", afficher_jeux),
        ("Rechercher", rechercher_jeux_ui),
        ("Supprimer", supprimer_jeu_ui),
        ("Effacer", effacer_champs)
    ]
    
    for i, (texte, cmd) in enumerate(actions):
        btn = tk.Button(frame_btn, text=texte, command=cmd,
                       bg=btn_color if i%2==0 else highlight_color, 
                       fg="black", relief=tk.RAISED, borderwidth=3,
                       font=("Arial", 10, "bold"))
        btn.grid(row=0, column=i, padx=5, ipadx=10)
    
    afficher_jeux()

if __name__ == "__main__":
    initialiser_fichier()
    root = tk.Tk()
    root.title("game collection management")
    creer_interface_login(root)
    root.mainloop()