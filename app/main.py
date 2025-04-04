# app/main.py

from llibreries import bd, login

def menu():
    bd.connectar()  # Inicialitza la base de dades
    while True:
        print("\n=== GESTOR ESPAMUS+ ===")
        print("1. Registrar-se")
        print("2. Iniciar sessió")
        print("3. Sortir")
        opcio = input("Opció: ")

        if opcio == "1":
            login.registrar()
        elif opcio == "2":
            login.iniciar_sessio()
        elif opcio == "3":
            print("Fins aviat!")
            break
        else:
            print("Opció no vàlida")

if __name__ == "__main__":
    menu()
