# A main file for running one instance of the game
from interactions import interact
from person import Person
import random

def simple_run():
    all_peeps = [Person(randomize_emotions=15) for _ in range(10)]

    while True:
        user_input = input('Press Enter to continue or type "exit" to quit: ')
        if user_input.lower() == 'exit':
            break
        P1, P2 = random.sample(all_peeps, 2)
        interact(P1, P2, strength=0.5)
        P1.pretty_print()
        P2.pretty_print()

        if (P1.ES.anger == 100 and P2.ES.anger == 100):
            print(f"{P1.name} and {P2.name} got angry and fought!")
        
        if (P1.ES.jealousy == 100):
            print(f"{P1.name} got jealous and will be spreading rumours!")
        
        if (P2.ES.jealousy == 100):
            print(f"{P2.name} got jealous and will be spreading rumours!")

def main():
    # simple_run()
    p = Person(randomize_stats=200)
    p2 = Person()
    p.pretty_print()
    p2.pretty_print()

if __name__ == '__main__':
    main()