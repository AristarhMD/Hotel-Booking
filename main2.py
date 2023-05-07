import pandas

df = pandas.read_csv("hotels.csv", dtype={"id":str})


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

    @classmethod
    def get_hotel_count(cls, data):
        return len(data)

    def __eq__(self, other):
        if self.hotel_id == other.hotel_id:
            return True
        else:
            return False



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


    @property
    def the_customer_name(self):
        name = self.customer_name.strip()
        name = name.title
        return name

    @staticmethod
    def convert(amount):
        return amount * 1.2

