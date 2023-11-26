# Function to calculate total price of booking
def calculate_total_price(start_date, end_date, car_price_per_day, child_seat, insurance_type):
    rental_days = (end_date - start_date).days + 1
    insurance_cost = 0
    child_seat_cost = 0

    if insurance_type == 'young':
        insurance_cost = 50
    elif insurance_type == 'standard':
        insurance_cost = 40
    elif insurance_type == 'senior':
        insurance_cost = 60

    if child_seat:
        child_seat_cost = 15

    total_price = rental_days * car_price_per_day + insurance_cost + child_seat_cost
    return total_price
