import mysql.connector

# Establish MySQL connection
def connect_to_db():
    conn = mysql.connector.connect(
        host="localhost", 
        user="root",  # replace with your MySQL username
        password="Nandhagopal@123",  # replace with your MySQL password
        database="railway_management"
    )
    return conn

# Add a new train
def add_train():
    train_name = input("Enter Train Name: ")
    source = input("Enter Source Station: ")
    destination = input("Enter Destination Station: ")
    available_seats = int(input("Enter Available Seats: "))

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO trains (train_name, source, destination, available_seats)
        VALUES (%s, %s, %s, %s)
    """, (train_name, source, destination, available_seats))
    conn.commit()
    print("Train added successfully!")
    conn.close()

# View all trains
def view_all_trains():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trains")
    trains = cursor.fetchall()
    if not trains:
        print("No trains available.")
    else:
        print("Train ID | Train Name | Source | Destination | Available Seats")
        for train in trains:
            print(f"{train[0]} | {train[1]} | {train[2]} | {train[3]} | {train[4]}")
    conn.close()

# Book a ticket
def book_ticket():
    train_id = int(input("Enter Train ID: "))
    passenger_name = input("Enter Passenger Name: ")
    no_of_seats = int(input("Enter Number of Seats: "))

    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT available_seats FROM trains WHERE train_id = %s", (train_id,))
    available_seats = cursor.fetchone()

    if available_seats and available_seats[0] >= no_of_seats:
        cursor.execute("""
            INSERT INTO bookings (train_id, passenger_name, no_of_seats)
            VALUES (%s, %s, %s)
        """, (train_id, passenger_name, no_of_seats))

        cursor.execute("""
            UPDATE trains SET available_seats = available_seats - %s
            WHERE train_id = %s
        """, (no_of_seats, train_id))

        conn.commit()
        print(f"Ticket booked successfully for {passenger_name}!")
    else:
        print("Not enough available seats.")
    
    conn.close()

# View all booked tickets
def view_all_booked_tickets():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.booking_id, t.train_name, b.passenger_name, b.no_of_seats 
        FROM bookings b
        JOIN trains t ON b.train_id = t.train_id
    """)
    bookings = cursor.fetchall()

    if not bookings:
        print("No tickets booked yet.")
    else:
        print("Booking ID | Train Name | Passenger Name | No of Seats")
        for booking in bookings:
            print(f"{booking[0]} | {booking[1]} | {booking[2]} | {booking[3]}")
    conn.close()

# Cancel a booking
def cancel_booking():
    booking_id = int(input("Enter Booking ID to cancel: "))
    
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT train_id, no_of_seats FROM bookings WHERE booking_id = %s", (booking_id,))
    booking = cursor.fetchone()

    if booking:
        train_id, no_of_seats = booking
        cursor.execute("DELETE FROM bookings WHERE booking_id = %s", (booking_id,))
        cursor.execute("""
            UPDATE trains SET available_seats = available_seats + %s
            WHERE train_id = %s
        """, (no_of_seats, train_id))

        conn.commit()
        print(f"Booking {booking_id} canceled successfully!")
    else:
        print("Booking not found.")
    
    conn.close()

# Main menu
def main():
    while True:
        print("\n=== Railway Management System ===")
        print("1. Add Train")
        print("2. View All Trains")
        print("3. Book Ticket")
        print("4. View All Booked Tickets")
        print("5. Cancel Booking")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == "1":
            add_train()
        elif choice == "2":
            view_all_trains()
        elif choice == "3":
            book_ticket()
        elif choice == "4":
            view_all_booked_tickets()
        elif choice == "5":
            cancel_booking()
        elif choice == "6":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
