import numpy as np
import random
import matplotlib.pyplot as plt

class RaceCar:
    def __init__(self, car_id, color, tank_capacity, fuel_consumption_per_km, max_speed, initial_acceleration, braking_acceleration, initial_fuel, weight):
        self.car_id = car_id
        self.color = color
        self.tank_capacity = tank_capacity
        self.fuel_consumption_per_km = fuel_consumption_per_km
        self.max_speed = max_speed
        self.initial_acceleration = initial_acceleration
        self.braking_acceleration = braking_acceleration
        self.fuel = initial_fuel 
        self.weight = weight
        self.distance_covered = 0
        self.remaining_distance = 900
        self.time = 0
        self.fuel_log = [initial_fuel]
        self.wait_time = 0   

    def move(self, time_step):
        fuel_consumed = self.fuel_consumption_per_km * (self.max_speed / 60) * time_step
        self.fuel -= fuel_consumed
        self.distance_covered += self.max_speed * time_step / 60
        self.remaining_distance = 900 - self.distance_covered 
        self.time += time_step
        self.fuel_log.append(self.fuel)

    def refuel(self, fuel_needed):
        if self.distance_covered % 300 == 0:
            self.fuel += fuel_needed
            if self.fuel > self.tank_capacity:
                self.fuel = self.tank_capacity
            self.fuel_log.append(self.fuel)
            self.wait_time += fuel_needed
            self.time += fuel_needed
            self.weight += fuel_needed * 0.8 
            self.max_speed = self.max_speed * (1 - fuel_needed * 0.01)    
            self.initial_acceleration = self.initial_acceleration * (1 - fuel_needed * 0.005)

    def status(self):
        return {
            'car_id': self.car_id,
            'color': self.color,
            'distance_covered': self.distance_covered,
            'remaining_distance': self.remaining_distance,
            'fuel': self.fuel,
            'time': self.time,
            'wait_time': self.wait_time
        }

def generate_random_car(car_id):
    colors = ['Red', 'Blue', 'Green', 'Yellow', 'Black', 'White']
    color = random.choice(colors)
    
    tank_capacity = random.randint(40,70) 
    fuel_consumption_per_km = round(random.uniform(0.12, 0.2), 2)
    max_speed = random.randint(100, 130)
    initial_acceleration = random.uniform(3, 7) 
    braking_acceleration = random.uniform(3, 6)
    initial_fuel = random.randint(40, tank_capacity)
    weight = random.randint(900, 1200)
    
    return RaceCar(car_id, color, tank_capacity, fuel_consumption_per_km, max_speed, initial_acceleration, braking_acceleration, initial_fuel, weight)

def ask_for_refuel(car):
    if car.fuel <= 0:
        print(f"Car {car.car_id} is out of fuel!")
        return True
    elif car.remaining_distance <= 300:
        response = input(f"Car {car.car_id} is approaching a fuel station. Do you want to refuel (yes/no)? ")
        if response.lower() == 'yes':
            return True
    return False

def run_race():
    cars = [generate_random_car(i) for i in range(1, 4)]
    time_step = 1
    winner = None 

    while all(car.remaining_distance > 0 for car in cars):
        for car in cars:
            car.move(time_step)

            if car.distance_covered % 300 == 0:
                if ask_for_refuel(car):
                    fuel_needed = car.fuel_consumption_per_km * 300
                    car.refuel(fuel_needed)
            
            if car.remaining_distance <= 0 and winner is None:
                winner = car.car_id
                print(f"Car {car.car_id} ({car.color}) has finished the race first!")

    for car in cars:
        status = car.status()
        print(f"Car {status['car_id']} ({status['color']}) - Distance Covered: {status['distance_covered']} km, Remaining Distance: {status['remaining_distance']} km, Fuel: {status['fuel']} liters, Time: {status['time']} minutes, Wait Time: {status['wait_time']} seconds")

    return winner

def run_multiple_races(num_races):
    winners = []
    for race_num in range(num_races):
        print(f"\nRace {race_num + 1}:")
        winner = run_race()
        winners.append(winner)
        print(f"Winner of Race {race_num + 1}: Car {winner}")
    
    print("\nWinners of all races:")
    for i, winner in enumerate(winners, 1):
        print(f"Race {i}: Car {winner}")

run_multiple_races(1)