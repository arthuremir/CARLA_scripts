import carla

client = carla.Client('localhost', 2000)
client.set_timeout(2.0)
actor_list = client.get_world().get_actors()
car_list = actor_list.filter('vehicle.*')
print(f"{len(car_list)} vehicles to be destroyed!")
for car in car_list:
    car.destroy()

