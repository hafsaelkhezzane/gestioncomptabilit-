from tkinter import *
import mysql.connector as my
from tkinter import simpledialog
from tkinter import messagebox
import tkinter as tk

def login_window():
    login_win = Tk()
    login_win.title('Login')
    login_win.geometry('300x150')
    login_win.minsize(300, 150)
    login_win.configure(bg='#f1f1f1')

    def check_login():
        username = username_entry.get()
        password = password_entry.get()

        # Perform your login authentication here
        # Replace the condition with your actual login check
        if username == 'comptable' and password == 'hafsahafsa':
            login_win.destroy()
            access_database()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    username_label = Label(login_win, text="Username:", font=("Arial", 12), bg='#f1f1f1')
    username_label.pack()

    username_entry = Entry(login_win, font=("Arial", 12))
    username_entry.pack()

    password_label = Label(login_win, text="Password:", font=("Arial", 12), bg='#f1f1f1')
    password_label.pack()

    password_entry = Entry(login_win, show="*", font=("Arial", 12))
    password_entry.pack()

    login_button = Button(login_win, text="Login", command=check_login, font=("Arial", 12))
    login_button.pack(pady=10)

    login_win.mainloop()


def access_database():
    try:
        con = my.connect(
            user='root',
            passwd='',
            host='localhost',
            port=3306,
            database='gestioncomptable'
        )
        if con.is_connected():
            print("Connected to the database")
            # Create a new window for selecting the table
            select_window = Tk()
            select_window.title('Select Table')
            select_window.geometry('600x600')
            select_window.minsize(400, 400)
            select_window.configure(bg='silver')

            # Table selection variable
            selected_table = StringVar()

            def update_table_dropdown():
                cursor = con.cursor()
                try:
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()
                    table_list = [table[0] for table in tables]
                    select_dropdown['menu'].delete(0, 'end')
                    for table in table_list:
                        select_dropdown['menu'].add_command(label=table, command=lambda value=table: selected_table.set(value))
                except my.errors.ProgrammingError as e:
                    print(f"Erreur lors de la récupération de la liste des tables : {e}")
                finally:
                    cursor.close()

            def display_table_contents():
                table_name = selected_table.get()
                if table_name:
                    cursor = con.cursor()
                    try:
                        cursor.execute(f"SELECT * FROM {table_name}")
                        rows = cursor.fetchall()
                        table_text.delete('1.0', END)
                        for row in rows:
                            table_text.insert(END, str(row) + '\n')
                    except my.errors.ProgrammingError as e:
                        print(f"Erreur lors de la récupération des données de la table {table_name} : {e}")
                    finally:
                        cursor.close()

            def return_to_menu():
                select_window.destroy()

            def add_new_table():
                table_name = simpledialog.askstring("Add New Table", "Enter the name of the new table:")
                if table_name:
                    column_data = simpledialog.askstring("Add New Table", "Enter column data (column1_name column1_type, column2_name column2_type, ...):")
                    if column_data:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"CREATE TABLE {table_name} ({column_data})")
                            con.commit()
                            print(f"New table '{table_name}' created successfully.")
                            update_table_dropdown()
                        except my.errors.ProgrammingError as e:
                            print(f"Error creating new table: {e}")
                        finally:
                            cursor.close()

            def add_new_column():
                    table_name = selected_table.get()
                    if table_name:
                        column_name = simpledialog.askstring("Add New Column", "Enter the name of the new column:")
                        if column_name:
                            cursor = con.cursor()
                            try:
                                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} VARCHAR(255)")
                                con.commit()
                                print(f"New column '{column_name}' added to table '{table_name}' successfully.")
                            except my.errors.ProgrammingError as e:
                                print(f"Error adding new column: {e}")
                            finally:
                                cursor.close()

            def delete_column():
                table_name = selected_table.get()
                if table_name:
                    column_name = simpledialog.askstring("Delete Column", "Enter the name of the column to delete:")
                    if column_name:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN {column_name}")
                            con.commit()
                            print(f"Column '{column_name}' deleted from table '{table_name}' successfully.")
                        except my.errors.ProgrammingError as e:
                            print(f"Error deleting column: {e}")
                        finally:
                            cursor.close()

            def change_column_name():
                table_name = selected_table.get()
                if table_name:
                    old_column_name = simpledialog.askstring("Change Column Name", "Enter the old name of the column:")
                    new_column_name = simpledialog.askstring("Change Column Name", "Enter the new name of the column:")
                    if old_column_name and new_column_name:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"ALTER TABLE {table_name} RENAME COLUMN {old_column_name} TO {new_column_name}")
                            con.commit()
                            messagebox.showinfo("Column Name Change", f"Column name '{old_column_name}' changed to '{new_column_name}' successfully.")
                        except my.errors.ProgrammingError as e:
                            messagebox.showerror("Error", f"Error changing column name: {e}")
                        finally:
                            cursor.close()
                    else:
                        messagebox.showwarning("Input Error", "Please enter both the old and new column names.")

            def delete_table():
                   table_name = selected_table.get()
                   if table_name:
                       confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the table '{table_name}'?")
                       if confirm:
                           cursor = con.cursor()
                           try:
                               cursor.execute(f"DROP TABLE {table_name}")
                               con.commit()
                               messagebox.showinfo("Table Deletion", f"Table '{table_name}' deleted successfully.")
                               update_table_dropdown()
                           except my.errors.ProgrammingError as e:
                               messagebox.showerror("Error", f"Error deleting table: {e}")
                           finally:
                               cursor.close()

            def insertion_valeur():
                    # Récupérer les valeurs saisies dans les Entry
                valeurs = [entry.get() for entry in entries]

                try:
                    # Connexion à la base de données
                    con = my.connect(
                        user='root',
                        passwd='',
                        host='localhost',
                        port=3306,
                        database='gestioncomptable'
                    )
                    cursor = con.cursor()

                    # Exécution de la requête d'insertion
                    nom_table = entry_table.get()  # Récupérer le nom de la table depuis le widget Entry
                    colonne1 = "nom_colonne1"  # Remplacer par le nom réel de la première colonne
                    colonne2 = "nom_colonne2"  # Remplacer par le nom réel de la deuxième colonne
                    requete = f"INSERT INTO {nom_table} ({colonne1}, {colonne2}) VALUES (%s, %s)"
                    cursor.execute(requete, tuple(valeurs))
                    con.commit()

                    print("L'enregistrement a été ajouté avec succès.")

                except my.Error as e:
                    print("Erreur lors de l'ajout de l'enregistrement :", e)

                finally:
                    # Fermeture de la connexion à la base de données
                    if con.is_connected():
                        cursor.close()
                        con.close()

             # Créer une fenêtre Tkinter
            fenetre = tk.Tk()

            # Demander à l'utilisateur de saisir le nom de la table
            label_table = tk.Label(fenetre, text="Nom de la table :")
            label_table.pack()
            entry_table = tk.Entry(fenetre)
            entry_table.pack()

            # Créer des Entry pour saisir les valeurs
            entries = []
            for i in range(2):  # Remplacer par le compte approprié
                label = tk.Label(fenetre, text=f"Valeur {i+1} :")
                label.pack()
                entry = tk.Entry(fenetre)
                entry.pack()
                entries.append(entry)
            
            # Table selection label
            select_label = Label(select_window, text="Select Table:", font=("Arial", 12), bg='#f1f1f1')
            select_label.pack()

            # Table selection dropdown
            select_dropdown = OptionMenu(select_window, selected_table, "bilan","visiteur","charge","dépense","client","compte","achat","produit","contacte","détail","détail","employé","enregistrement_visite","facture","fournisseur","grand_livre","journal","ventes","transaaction","entreprise","tva","dette","rapport_financiére","présenter","noter","actif","obtenir","livrer","traiter","contenir","faire","controler","céder","recevoir","tenir")
            select_dropdown.pack()
            select_dropdown.configure(background='DarkTurquoise')

            # Display Table button
            display_button = Button(select_window, text="Display Table", command=display_table_contents, font=("Arial", 12))
            display_button.pack(pady=4)
            display_button.configure(background='DarkTurquoise')

            table_text = Text(select_window, height=10, width=50)
            table_text.pack()

            return_button = Button(select_window, text="Return to Menu", command=return_to_menu, font=("Arial", 12))
            return_button.pack(pady=4)
            return_button.configure(background='CornflowerBlue')

            #ajouter une nouvelle table
            add_table_button = tk.Button(select_window, text="Add New Table", command=add_new_table, font=("Arial", 12))
            add_table_button.pack(pady=4)
            add_table_button.configure(background='DarkTurquoise')

            #ajouter une nouvelle colonne
            add_column_button = tk.Button(select_window, text="Add New Column", command=add_new_column, font=("Arial", 12))
            add_column_button.pack(pady=4)
            add_column_button.configure(background='DarkTurquoise')

            #supprimer une colonne
            delete_column_button = tk.Button(select_window, text="Delete Column", command=delete_column, font=("Arial", 12))
            delete_column_button.pack(pady=4)
            delete_column_button.configure(background='DarkTurquoise')

            #changer le nom d'une colonne
            change_name_button = tk.Button(select_window, text="Change Column Name", command=change_column_name, font=("Arial", 12))
            change_name_button.pack(pady=4)
            change_name_button.configure(background='DarkTurquoise')

            #supprimer une table
            delete_table_button = Button(select_window, text="Delete Table", command=delete_table, font=("Arial", 12))
            delete_table_button.pack(pady=4)
            delete_table_button.configure(background='DarkTurquoise')

            bouton_ajouter = tk.Button(fenetre, text="Insérer", command=insertion_valeur)
            bouton_ajouter.pack()

            def change_table_name():
                current_table_name = table_label.cget("text")  # Get the current table name from the label
                new_table_name = new_table_entry.get()  # Get the new table name from an Entry widget or any other source
                
                # Update the table name in the Tkinter interface
                table_label.config(text=new_table_name)
                
                try:
                    # Connect to the database
                    con = my.connect(
                        user='root',
                        passwd='',
                        host='localhost',
                        port=3306,
                        database='gestioncomptable'
                    )
                    cursor = con.cursor()
                    
                    # Execute the SQL query to rename the table
                    rename_query = f"ALTER TABLE `{current_table_name}` RENAME TO `{new_table_name}`"
                    cursor.execute(rename_query)
                    con.commit()
                    
                    print("Table name changed successfully.")
                
                except my.Error as e:
                    print("Error while changing table name:", e)
                
                finally:
                    # Close the database connection
                    if con.is_connected():
                        cursor.close()
                        con.close()

            # Create a label for the current table name
            table_label = tk.Label(select_window, text="Nom de la table :")
            table_label.pack()

            # Create an Entry widget to input the new table name
            new_table_entry = tk.Entry(select_window)
            new_table_entry.pack()

            # Create a button to trigger the table name change
            change_button = tk.Button(select_window, text="Changer le nom", command=change_table_name)
            change_button.pack()

            select_dropdown = OptionMenu(select_window, selected_table,"bilan","visiteur","charge","dépense","client","compte","achat","produit","contacte","détail","détail","employé","enregistrement_visite","facture","fournisseur","grand_livre","journal","ventes","transaaction","entreprise","tva","dette","rapport_financiére","présenter","noter","actif","obtenir","livrer","traiter","contenir","faire","controler","céder","recevoir","tenir" )
            select_dropdown.pack()

            select_window.mainloop()



    except my.errors as e:
        print(e)
login_window()

fenetre = Tk()
fenetre.geometry('400x400')
fenetre.title('GESTION DE STOCK')
fenetre['bg'] = '#f1f1f1'
fenetre.resizable(height=False, width=False)
fenetre.configure(background='#00BFFF')

image_label = Label(fenetre)
image_label.pack()

# Exit Button
exit_button = Button(fenetre, text="quitter", command=fenetre.quit, font=("Arial", 12))
exit_button.pack(pady=5)

fenetre.mainloop()

