"""
Fitxer principal del projecte 'Gestió Hotelera Espamus+'

Aquest fitxer és el punt d'entrada de l'aplicació.
- Mostra el menú principal per interactuar amb l'usuari.
- Inicia la connexió amb la base de dades.
- Permet registrar usuaris nous i iniciar sessió.
- Crida les funcions corresponents segons l'opció seleccionada.
"""

from llibreries import login 

def main():
    login.crear_taula_usuaris()
    sortir = True
    while sortir:
        print("\n1. Registrar-se")
        print("2. Iniciar sessió")
        print("3. Sortir")
        opcio = input("Escull una opció: ")

        if opcio == "1":
            usuari = input("Introdueix un nom d'usuari: ")
            contrasenya = input("Introdueix una contrasenya: ")
            login.registrar_usuari(usuari, contrasenya)
        elif opcio == "2":
            usuari = input("Usuari: ")
            contrasenya = input("Contrasenya: ")
            login.iniciar_sessio(usuari, contrasenya)
        elif opcio == "3":
            print("Sortint...")
            sortir = False
        else:
            print("Opció no vàlida.")

if __name__ == "__main__":
    main()
