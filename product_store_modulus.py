import json
import csv
from datetime import datetime

class Store:


  def __init__(self):
        self.product_list = [] # List of products in stock
        self.sell_list = []
        

  def add_product(self):

    """
    Adds a product to the stock.
    If the product is already in stock the addition requires only the product name and quantity.
    """

    product_name = input("Nome del prodotto: ")
    
    try:
        quantity = float(input("Quantità: "))
        if quantity <= 0 :
            raise ValueError("La quantità deve essere maggiore di zero!")
    except ValueError as ve:
        print(f"Input invalido: {ve}")
        return
    
    for product in self.product_list:
        if product['product_name'] == product_name: # Check if the product name is already in the product list.
            product['quantity'] += quantity # If the product is already present, update the quantity
            print(f"Aggiornata quantità per {product_name}: {product['quantity']}")
            self.save_data()
            return

    try:
        purchase_price = float(input(f"Prezzo di acquisto {product_name}: "))
        if purchase_price <= 0 :
            raise ValueError ("Il prezzo di acquisto deve essere maggiore di zero") 
        sale_price = float(input(f"Prezzo di vendita {product_name}: "))
        if sale_price <= 0 :
            raise ValueError ("Il prezzo di vendita deve essere maggiore di zero")
    except ValueError as ve:
        print(f"Input invalido: {ve}")
        return
       
    
    new_product = {'product_name': product_name, 'quantity': quantity, 'purchase_price': purchase_price, 'sale_price': sale_price}
    self.product_list.append(new_product)
    self.save_data()
    print(f"AGGIUNTO: {quantity} x {product_name} ")


    
     
  def sell_product(self):

     """
      records a sale that was made.
      products sold will be subtracted from the warehouse inventory
     """

     total_sale = 0
     current_sale =  [] # Temporary list for current sale
     

     while True:
            try:
                product_name = input("Nome del prodotto: ")
                quantity = float(input("Quantità: "))
                if quantity <= 0:
                    raise ValueError("La quantità deve essere un numero positivo.")
            except ValueError as e:
                print(f"Error: {e}")
                continue

            sold_product = None
            for product in self.product_list:
              if product['product_name'] == product_name:
               sold_product = product
               break

            if sold_product:
                if sold_product['quantity'] < quantity:
                    print(f"Errore: Quantità  di {product_name} insufficiente in magazzino.")
                else:
                    sale_amount = quantity * sold_product['sale_price']
                    total_sale += sale_amount
                    
                    sale_details = {
                        'product_name': product_name,
                        'quantity': quantity,
                        'sale_price': sold_product['sale_price'],
                        'purchase_price': sold_product['purchase_price'],
                        'sale_amount': round(sale_amount,2),
                        'sell_datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

                    
                    current_sale.append(sale_details)


                    sold_product['quantity'] -= quantity
                    if sold_product['quantity'] == 0:          
                     self.product_list.remove(sold_product)    # Remove the product from the list if the quantity is zero.
                    
                    self.save_data()
                    self.save_sale_to_csv(sale_details)  # Add sale to CSV
            else:
                print(f"Errore: il prodotto {product_name} non è presente in magazzino.")
        
            add_another = input("Aggiungere un altro prodotto? (si/no): ").strip().lower()
            if add_another != "si":
                break

           
     self.sell_list.extend(current_sale)

     print("VENDITA REGISTRATA\n")
     for product in current_sale:
        print(f"{product['quantity']} x {product['product_name']} €{product['sale_price']:.2f}")

     
     print(f"\nVendite Totali: €{total_sale:.2f}\n")



  def list_products(self):

      """
      lists products in stock
      """
      print()
      print("PRODOTTO QUANTITA' PREZZO")
      for product in self.product_list:
        print(f"{product['product_name']} {product['quantity']:.0f} €{product['sale_price']}")
      print()



  def gross_profit(self):

      """
      calculates gross profits
      """

      sales_data = self.load_sales_from_csv()
      gross_profit = sum(float(sale['sale_amount']) for sale in sales_data)
      return gross_profit


  def net_profit(self):

     """ 
     calculates net profits
     """
     sales_data = self.load_sales_from_csv()
     net_profit = 0

     for sale in sales_data:
            sale_quantity = float(sale['quantity'])
            sale_price = float(sale['sale_price'])
            purchase_price = float(sale['purchase_price'])  
            sale_amount = float(sale['sale_amount'])

            profit = (sale_price - purchase_price) * sale_quantity
            net_profit += profit

     return net_profit



  def help_menu(self):

      """
      shows the possible commands
      """

      print("Comandi possibili:")
      print("- aggiungi: aggiungi un prodotto al magazzino")
      print("- elenca: elenca i prodotti in magazzino")
      print("- vendita: registra una vendita effettuata")
      print("- profitti: mostra profitti totali")
      print("- aiuto: mostra i possibili comandi")
      print("- chiudi: esci dal programma")


  def close_store(self):

      """
      exit the program
      """
      self.save_data()
      print("Arrivederci.")



  def load_data(self):

      """
      upload warehouse inventory
      """

      try:
            with open('stock_inventory.json', 'r') as file:
                self.product_list = json.load(file)
      except FileNotFoundError:
            print("Il tuo magazzino è vuoto, inizia a riempirlo!")



  def save_data(self):

      """
      save warehouse inventory
      """

      with open('stock_inventory.json', 'w') as file:
            json.dump(self.product_list, file, indent=4)



  def save_sale_to_csv(self, sale_details):
      
       """
         saves sales made within a csv file
         """
      
       fieldnames = ['product_name', 'quantity', 'sale_price', 'purchase_price', 'sale_amount', 'sell_datetime']
       with open('sales_data.csv', 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(sale_details)

     
  def load_sales_from_csv(self):
       
       """
       load the sales data from csv
       """
       
       sales_data = []
       try:
            with open('sales_data.csv', 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    sales_data.append(row)
       except FileNotFoundError:
            pass  
       return sales_data

