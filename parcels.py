# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 17:03:49 2024

@author: Alex
"""

import datetime

class Customer:
    """Represents a customer with stored details."""
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number

class User:
    """Represents a system user (Admin, Manager, Employee)."""
    def __init__(self, name, phone_number, role):
        self.name = name
        self.phone_number = phone_number
        self.role = role

class Parcel:
    """Represents a parcel with tracking details and status updates."""
    def __init__(self, parcel_id, recipient, status="Pending"):
        self.parcel_id = parcel_id
        self.recipient = recipient
        self.status = status
        self.history = [] # Track status changes with timestamps

    def update_status(self, new_status):
        self.status = new_status
        event = {
            "status": new_status,
            "timestamp": datetime.datetime.now()
        }
        self.history.append(event)
        message = ""
        if new_status == "Received at Office":
            message = "Your parcel has been received at the office."
        elif new_status == "Delivered at Office":
            message = "Your parcel has been delivered to the office."
        elif new_status == "Collected by Customer":
            message = "Your parcel has been collected."
        
        if message:
            send_sms(self.recipient.phone_number, message)

class Payment:
    """Handles payment processing with various methods."""
    def __init__(self, amount, method):
        self.amount = amount
        self.method = method # 'Pay on Delivery', 'Mpesa', 'Cash'
        self.status = "Unpaid"

    def make_payment(self):
        if self.method == "Mpesa":
            self.process_mpesa()
        else:
            self.status = "Paid"
            print(f"Payment of {self.amount} via {self.method} completed.")

    def process_mpesa(self):
        self.status = "Paid"
        print(f"Payment of {self.amount} via Mpesa completed.")

# Utility functions
def send_sms(phone_number, message):
    print(f"Sending SMS to {phone_number}: {message}")

def print_receipt(parcel):
    print("\n====== Wahesco Interparcel Limited ======")
    print("========== PARCEL RECEIPT ==============")
    print(f"Parcel ID: {parcel.parcel_id}")
    print(f"Recipient: {parcel.recipient.name}")
    print(f"Phone Number: {parcel.recipient.phone_number}")
    print(f"Status: {parcel.status}")
    print("History:")
    for event in parcel.history:
        print(f" - {event['status']} at {event['timestamp']}")
    print("========================================\n")

def print_daily_report(report_data):
    print("\n===== DAILY REPORT - Wahesco Interparcel Limited =====")
    print(f"Date: {datetime.datetime.now().date()}")
    for entry in report_data:
        print(f"Parcel ID: {entry['Parcel ID']}, Status: {entry['Status']}, Date: {entry['Date']}, Recipient: {entry['Recipient']}")
    print("========================================\n")

class ParcelManagementSystem:
    def __init__(self):
        self.parcels = {}
        self.users = []
        self.customers = [] # Simulate customer database

    def add_user(self, name, phone_number, role):
        user = User(name, phone_number, role)
        self.users.append(user)
        return user

    def add_customer(self, name, phone_number):
        existing_customer = self.find_customer_by_phone(phone_number)
        if existing_customer:
            return existing_customer # Return existing customer if found
        customer = Customer(name, phone_number)
        self.customers.append(customer)
        return customer

    def find_customer_by_phone(self, phone_number):
        for customer in self.customers:
            if customer.phone_number == phone_number:
                return customer
        return None

    def add_parcel(self, parcel_id, recipient, payment_amount, payment_method):
        parcel = Parcel(parcel_id, recipient)
        self.parcels[parcel_id] = parcel
        payment = Payment(payment_amount, payment_method)
        parcel.update_status("Received at Office")
        if payment.method != "Mpesa":
            payment.make_payment()

    def update_parcel_status(self, parcel_id, new_status):
        parcel = self.parcels.get(parcel_id)
        if parcel:
            parcel.update_status(new_status)
            if new_status == "Collected by Customer":
                print_receipt(parcel)
        else:
            print("Parcel not found.")

    def generate_daily_report(self):
        today = datetime.datetime.now().date()
        start_date = datetime.datetime.combine(today, datetime.time.min)
        end_date = datetime.datetime.combine(today, datetime.time.max)
        report_data = self.generate_report(start_date, end_date)
        print_daily_report(report_data)

    def generate_report(self, start_date, end_date):
        report = []
        for parcel in self.parcels.values():
            for event in parcel.history:
                if start_date <= event["timestamp"] <= end_date:
                    report.append({
                        "Parcel ID": parcel.parcel_id,
                        "Recipient": parcel.recipient.name,
                        "Status": event["status"],
                        "Date": event["timestamp"]
                    })
        return report

    def user_interface(self):
        print("\n========== Welcome to Wahesco Interparcel Limited ==========")
        print("Options:")
        print("1. Add Parcel")
        print("2. Update Parcel Status")
        print("3. Generate Daily Report")
        print("4. Add Customer")
        print("5. Exit")
        
        while True:
            choice = input("\nChoose an option (1-5): ")
            
            if choice == '1':
                parcel_id = input("Enter Parcel ID: ")
                phone_number = input("Enter Recipient Phone Number: ")
                customer = self.find_customer_by_phone(phone_number)
                
                if not customer:
                    print("Customer not found. Adding new customer.")
                    name = input("Enter Recipient Name: ")
                    customer = self.add_customer(name, phone_number)
                
                amount = float(input("Enter Payment Amount: "))
                method = input("Enter Payment Method (Mpesa, Cash, Pay on Delivery): ")
                self.add_parcel(parcel_id, customer, amount, method)
                print("Parcel added successfully.")

            elif choice == '2':
                parcel_id = input("Enter Parcel ID: ")
                status = input("Enter New Status (Received at Office, Delivered at Office, Collected by Customer): ")
                self.update_parcel_status(parcel_id, status)

            elif choice == '3':
                self.generate_daily_report()

            elif choice == '4':
                name = input("Enter Customer Name: ")
                phone_number = input("Enter Customer Phone Number: ")
                self.add_customer(name, phone_number)
                print("Customer added successfully.")
            
            elif choice == '5':
                print("Exiting Wahesco Interparcel Limited system.")
                break
            
            else:
                print("Invalid option. Please try again.")

# Example Usage
parcel_system = ParcelManagementSystem()

# Initial users and customers for demonstration
parcel_system.add_user("AdminUser", "+1234567890", "Admin")
parcel_system.add_customer("Alice", "+1234567893")
parcel_system.add_customer("Bob", "+1234567894")

# Launch the one-page interface
parcel_system.user_interface()
