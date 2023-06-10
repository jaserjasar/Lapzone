import os
import tkinter as tk
from tkinter import messagebox
import datetime


class LapzoneApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lapzone")
        self.geometry("800x600")

        # Create the main window
        self.customer_details_frame = CustomerDetailsLabel(self)
        self.customer_details_frame.pack(side="top", fill="both", padx=10, pady=10)

        self.purchase_label = PurchaseLabel(self)
        self.purchase_label.pack(side="left", fill="both", padx=10, pady=10)

        self.service_list_label = ServiceListLabel(self)
        self.service_list_label.pack(side="right", fill="both", padx=10, pady=10)

        self.create_banner_label()

    def create_banner_label(self):
        banner_label = BannerLabel(self)
        banner_label.pack(side="bottom", pady=10)


class CustomerDetailsLabel(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Customer Details", font=("Arial", 16, "bold"), padx=10, pady=10)
        self.configure(background="lightblue")

        # Create labels in customer details section
        tk.Label(self, text="Name:").grid(row=0, column=0, sticky="e")
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, sticky="w")

        tk.Label(self, text="Phone:").grid(row=1, column=0, sticky="e")
        self.phone_entry = tk.Entry(self)
        self.phone_entry.grid(row=1, column=1, sticky="w")

        tk.Label(self, text="Payment Mode:").grid(row=2, column=0, sticky="e")
        self.payment_mode_var = tk.StringVar(value="UPI")
        payment_mode_options = ["UPI", "Cash", "Card"]
        self.payment_mode_dropdown = tk.OptionMenu(self, self.payment_mode_var, *payment_mode_options)
        self.payment_mode_dropdown.grid(row=2, column=1, sticky="w")

        tk.Label(self, text="Date:").grid(row=3, column=0, sticky="e")
        self.date_entry = tk.Entry(self)
        self.date_entry.grid(row=3, column=1, sticky="w")
        self.date_entry.insert(0, datetime.date.today().strftime("%d-%m-%Y"))


class PurchaseLabel(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Purchase List", font=("Arial", 16, "bold"), padx=10, pady=10)
        self.configure(background="lightblue")

        # Create labels in purchase list section
        tk.Label(self, text="Item:").grid(row=0, column=0, sticky="e")
        self.item_name_entry = tk.Entry(self)
        self.item_name_entry.grid(row=0, column=1, sticky="w")

        tk.Label(self, text="Price:").grid(row=1, column=0, sticky="e")
        self.price_entry = tk.Entry(self)
        self.price_entry.grid(row=1, column=1, sticky="w")

        tk.Label(self, text="Quantity:").grid(row=2, column=0, sticky="e")
        self.quantity_entry = tk.Entry(self)
        self.quantity_entry.grid(row=2, column=1, sticky="w")

        # Create buttons
        button_frame = tk.Frame(self)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.add_button = tk.Button(button_frame, text="Add to List", command=self.add_purchase_item)
        self.add_button.grid(row=0, column=0, padx=5)

        self.generate_button = tk.Button(button_frame, text="Generate Bill", command=self.generate_purchase_bill)
        self.generate_button.grid(row=0, column=1, padx=5)

        # Create purchase list text area
        self.purchase_list_text = tk.Text(self, width=40, height=10)
        self.purchase_list_text.grid(row=4, column=0, columnspan=2)

    def add_purchase_item(self):
        item_name = self.item_name_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()

        if item_name and price and quantity:
            item_total = float(price) * int(quantity)
            self.purchase_list_text.insert(tk.END, f"{item_name}: {price} x {quantity} = {item_total}\n")

            # Clear the input fields
            self.item_name_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Missing Details", "Please enter all purchase details.")

    def generate_purchase_bill(self):
        customer_name = self.master.customer_details_frame.name_entry.get()
        customer_phone = self.master.customer_details_frame.phone_entry.get()
        payment_mode = self.master.customer_details_frame.payment_mode_var.get()
        date = self.master.customer_details_frame.date_entry.get()

        if customer_name and customer_phone and payment_mode and date:
            bill_content = f"Customer Details:\nName: {customer_name}\nPhone: {customer_phone}\n\n"
            bill_content += f"Purchase List:\n{self.purchase_list_text.get('1.0', tk.END)}\n"

            total_amount = self.calculate_total_amount()
            bill_content += f"Total Amount: {total_amount}\n\n"
            bill_content += f"Payment Mode: {payment_mode}\nDate: {date}"

            # Save the bill content to a file
            file_name = f"purchase_invoice_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
            file_path = os.path.join("bills", file_name)  # Assuming "bills" is a directory to store the bills
            with open(file_path, "w") as file:
                file.write(bill_content)

            messagebox.showinfo("Invoice Generated", f"Invoice generated successfully!\nFile saved at: {file_path}")
        else:
            messagebox.showerror("Missing Details", "Please enter all customer details.")

    def calculate_total_amount(self):
        lines = self.purchase_list_text.get("1.0", tk.END).split("\n")
        total = 0.0
        for line in lines:
            if line:
                item_total = line.split("=")[-1].strip()
                total += float(item_total)
        return total


class ServiceListLabel(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Service List", font=("Arial", 16, "bold"), padx=10, pady=10)
        self.configure(background="lightblue")

        # Create labels in service list section
        tk.Label(self, text="Service:").grid(row=0, column=0, sticky="e")
        self.service_name_entry = tk.Entry(self)
        self.service_name_entry.grid(row=0, column=1, sticky="w")

        tk.Label(self, text="Price:").grid(row=1, column=0, sticky="e")
        self.price_entry = tk.Entry(self)
        self.price_entry.grid(row=1, column=1, sticky="w")

        tk.Label(self, text="Quantity:").grid(row=2, column=0, sticky="e")
        self.quantity_entry = tk.Entry(self)
        self.quantity_entry.grid(row=2, column=1, sticky="w")

        # Create buttons
        button_frame = tk.Frame(self)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.add_button = tk.Button(button_frame, text="Add to List", command=self.add_service_item)
        self.add_button.grid(row=0, column=0, padx=5)

        self.generate_button = tk.Button(button_frame, text="Generate Bill", command=self.generate_service_bill)
        self.generate_button.grid(row=0, column=1, padx=5)

        # Create service list text area
        self.service_list_text = tk.Text(self, width=40, height=10)
        self.service_list_text.grid(row=4, column=0, columnspan=2)

    def add_service_item(self):
        service_name = self.service_name_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()

        if service_name and price and quantity:
            self.service_list_text.insert(tk.END, f"{service_name}: {price} x {quantity}\n")

            # Clear the input fields
            self.service_name_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Missing Details", "Please enter all service details.")

    def generate_service_bill(self):
        customer_name = self.master.customer_details_frame.name_entry.get()
        customer_phone = self.master.customer_details_frame.phone_entry.get()
        payment_mode = self.master.customer_details_frame.payment_mode_var.get()
        date = self.master.customer_details_frame.date_entry.get()

        if customer_name and customer_phone and payment_mode and date:
            bill_content = f"Customer Details:\nName: {customer_name}\nPhone: {customer_phone}\n\n"
            bill_content += f"Service List:\n{self.service_list_text.get('1.0', tk.END)}\n"

            total_amount = self.calculate_total_amount()
            bill_content += f"Total Amount: {total_amount}\n\n"
            bill_content += f"Payment Mode: {payment_mode}\nDate: {date}"

            # Save the bill content to a file
            file_name = f"service_invoice_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
            file_path = os.path.join("bills", file_name)  # Assuming "bills" is a directory to store the bills
            with open(file_path, "w") as file:
                file.write(bill_content)

            messagebox.showinfo("Invoice Generated", f"Invoice generated successfully!\nFile saved at: {file_path}")
        else:
            messagebox.showerror("Missing Details", "Please enter all customer details.")

    def calculate_total_amount(self):
        lines = self.service_list_text.get("1.0", tk.END).split("\n")
        total = 0.0
        for line in lines:
            if line:
                price, quantity = line.split(":")[-1].strip().split("x")
                total += float(price) * int(quantity)
        return total



class BannerLabel(tk.Label):
    def __init__(self, parent):
        super().__init__(parent, text="Welcome to Lapzone", font=("Arial", 24, "bold"), bg="lightblue",
                         fg="black", padx=20, pady=10)


if __name__ == "__main__":
    # Create the 'bills' directory if it doesn't exist
    if not os.path.exists("bills"):
        os.makedirs("bills")

    app = LapzoneApp()
    app.mainloop()
