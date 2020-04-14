from car import Env

if __name__ == "__main__":
    car = Env()
    car.reset()
    try:
        while True:
            pass
    finally:
        car.destroy_actors()
        print("Actors removed!")

