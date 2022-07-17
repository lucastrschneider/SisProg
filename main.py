from prog_sys.event_motor import EventMotor
from prog_sys.memory import Memory

if __name__ == "__main__":
    mem = Memory()

    if id(mem) == id(Memory()):
        print("Singleton works, both variables contain the same instance.")
    else:
        print("Singleton failed, variables contain different instances.")