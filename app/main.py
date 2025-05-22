"""
 Fitxer principal del projecte 'Gestió Hotelera Espamus+'
 
 Aquest fitxer és el punt d'entrada de l'aplicació.
 - Mostra el menú principal per interactuar amb l'usuari.
 - Inicia la connexió amb la base de dades.     
 - Permet registrar usuaris nous i iniciar sessió.
 - Crida les funcions corresponents segons l'opció seleccionada.  
 """

from llibreries import login, manteniment

def main():
    login_correcte, usuari = login.iniciar_gui()
    if login_correcte:
        manteniment.obrir_finestra_manteniment(usuari)

if __name__ == "__main__":
    main()