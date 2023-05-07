import pandas

df = pandas.read_csv("hotels.csv", dtype={"id":str})
df_cards = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pandas.read_csv("card_security.csv", dtype=str)


class Hotel:

    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def available(self):
        """Checks if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False

    def book(self):
        """Books the hotel by changing the availability from yes to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)


class ReservationTicker:

    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def get_ticket(self):
        content = f"""
        Thank you for your reservation!
        Here are your booking data:
        Name:{self.customer_name}
        Hotel name: {self.hotel.name}"""

        return content


class SpaHotel(Hotel):
    def book_spa_package(self):
        pass

class SpaReservationTicket:
    def __init__(self, customer_name, spa_object):
        self.customer_name = customer_name
        self.spa = spa_object

    def get_ticket(self):
        content = f"""
        Thank you for your SPA reservation!
        Here are your SPA booking data:
        Name:{self.customer_name}
        Hotel name: {self.spa.name}"""

        return content

class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {"number":self.number, "expiration": expiration,
                     "holder": holder, "cvc": cvc}
        if card_data in df_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_cards_security.loc[df_cards_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False



print(df)
hotel_ID = input("Enter the ID od the hotel: ")
hotel = Hotel(hotel_ID)
if hotel.available():
    credit_card = SecureCreditCard(number="1234567890123456")
    if credit_card.validate(expiration="12/26", holder="JOHN SMITH", cvc="123"):
        if credit_card.authenticate(given_password="mypass"):
            hotel.book()
            name = input("Enter your name: ")
            reservation_ticket = ReservationTicker(customer_name=name, hotel_object=hotel)
            print(reservation_ticket.get_ticket())
            spa_question = input("Do you want to book a spa package?")
            if spa_question == "yes":
                spa_reservation = SpaReservationTicket(customer_name=name, spa_object=hotel)
                print(spa_reservation.get_ticket())
            else:
                print("An error occur!")
        else:
            print("Credit Card authentication failed!")
    else:
        print("There was a big problem with your payment, contact support!")
else:
    print("Hotel is not free")