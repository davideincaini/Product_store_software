
from product_store_modulus import Store

store = Store()
store.load_data()


cmd = None

while cmd!="chiudi":
        
        cmd = input("Inserisci un comando: ").strip().lower()

        if cmd == 'aggiungi':
          store.add_product()
          

        elif cmd == 'vendita':
            store.sell_product()
            

        elif cmd == 'elenca':
            store.list_products()

        elif cmd == 'profitti':
         print("Profitto lordo= €{:.2f}".format(store.gross_profit()), "Profitto netto= €{:.2f}".format(store.net_profit()))

        elif cmd == 'aiuto':
            store.help_menu()

        elif cmd == 'chiudi':
            store.close_store()
            break

        else:
            print("Comando non valido")
            print("I comandi disponibili sono i seguenti:")
            print("- aggiungi: aggiungi un prodotto al magazzino")
            print("- elenca: elenca i prodotti in magazzino")
            print("- vendita: registra una vendita effettuata")
            print("- profitti: mostra profitti totali")
            print("- aiuto: mostra i possibili comandi")
            print("- chiudi: esci dal programma")


