# No relatorio, incluir a distribuição usada
# Nos varios processos, nao usar valores especificos no self.hold(...), usar distribuiçoes tipo uniforme
# Dps das storages 2 e 4, as coisas nao vao para lado nenhum
# As coisas estao a funcionar bem para os decks mas nao para as rodas (foundry da asneiras)


"""while (fila de espera) > 0:
    fila.pop()"""

DAY = 1440
END = 4320
NUM_DIAS = 0

import salabim as sim


class SimulationManager(sim.Component):
    def process(self):
        global DAY, NUM_DIAS
        print("SIMULATION MANAGER BROOO")
        while True:
            # 480 = 8h / 960 = 16h / 1440 = 24h
            if 480 + DAY * NUM_DIAS > env.now() or DAY * (NUM_DIAS + 1) < env.now():  # Intervalo de horas que se trabalha
                print("TOCA A TRABALHAR BROOO")
                trabalho.set(value=True)
                yield self.hold(60)
            elif 480 + DAY * NUM_DIAS <= env.now() <= DAY * (NUM_DIAS + 1):
                print("VAO DORMIR MALTINHA")
                trabalho.set(value=False)
                yield self.hold(60)
            if env.now() == DAY * (NUM_DIAS + 1):
                NUM_DIAS += 1
                yield self.hold(60)
            if env.now() == END:
                break


class Deck(sim.Component):
    def process(self):
        # Pressing
        self.enter(waitingLinePressing)
        for press in pressing:
            if press.ispassive():
                press.activate()
                break
        yield self.passivate()

        # Storage 1
        """print("YOOOOO " + str((DAY * (NUM_DIAS + 1)) - env.now()))
        print("NUM_DIAS: " + str(NUM_DIAS))"""
        self.enter(waitingLineStorage1)
        yield self.passivate()

        # Cutting
        self.enter(waitingLineCutting)
        for cutt in cutting:
            if cutt.ispassive():
                cutt.activate()
                break
        yield self.passivate()

        # Finishing
        self.enter(waitingLineFinishing)
        if finishing.ispassive():
            finishing.activate()
        yield self.passivate()

        # Painting
        self.enter(waitingLinePainting)
        if painting.ispassive():
            painting.activate()
        yield self.passivate()

        # Storage 2
        self.enter(waitingLineStorage2)
        storage2.activate()
        yield self.passivate()


class Wheel(sim.Component):
    def process(self):
        # Foundry
        self.enter(waitingLineFoundry)
        if foundry.ispassive():
            foundry.activate()
        yield self.passivate()

        # Storage 3
        self.enter(waitingLineStorage3)
        storage3.activate()
        yield self.passivate()

        # Machining
        self.enter(waitingLineMachining)
        for mach in machining:
            if mach.ispassive():
                mach.activate()
                break
        yield self.passivate()

        # Printing
        self.enter(waitingLinePrinting)
        if printing.ispassive():
            printing.activate()
        yield self.passivate()

        # Storage 4
        self.enter(waitingLineStorage4)
        storage4.activate()
        yield self.passivate()


class WheelGenerator(sim.Component):
    def setup(self, num_wheels):
        self.num_wheels = num_wheels

    def process(self):
        global DAY, NUM_DIAS
        while self.num_wheels > 0:
            Wheel()
            self.num_wheels -= 1


class DeckGenerator(sim.Component):
    def setup(self, num_deck):
        self.num_deck = num_deck

    def process(self):
        global DAY, NUM_DIAS
        while self.num_deck > 0:
            Deck()
            self.num_deck -= 1


# ---------------------------------------------------- DECK ------------------------------------------------------------


class Pressing(sim.Component):
    def process(self):
        while True:
            while len(waitingLinePressing) == 0:
                yield self.passivate()
            if trabalho.get():
                self.deck = waitingLinePressing.pop()
                yield self.hold(100)  # Este valor nao pode ser 100, usar uma distribuição qq
                self.deck.activate()
            else:
                yield self.wait((trabalho, True))


class Storage1(sim.Component):
    def process(self):
        aux = []
        while True:
            if trabalho.get() is False:
                while len(waitingLineStorage1) > 0:
                    self.deck = waitingLineStorage1.pop()
                    aux.append(self.deck)
                yield self.hold((DAY * (NUM_DIAS + 1)) - env.now())
                for i in aux:
                    i.activate()
            else:
                yield self.wait((trabalho, False))


class Cutting(sim.Component):
    def process(self):
        while True:
            while len(waitingLineCutting) == 0:
                yield self.passivate()
            if trabalho.get():
                self.deck = waitingLineCutting.pop()
                yield self.hold(60)
                self.deck.activate()
            else:
                yield self.wait((trabalho, True))


class Finishing(sim.Component):
    def process(self):
        while True:
            while len(waitingLineFinishing) == 0:
                yield self.passivate()
            if trabalho.get():
                self.deck = waitingLineFinishing.pop()
                yield self.hold(15)
                self.deck.activate()
            else:
                yield self.wait((trabalho, True))


class Painting(sim.Component):
    def process(self):
        while True:
            while len(waitingLinePainting) == 0:
                yield self.passivate()
            if trabalho.get():
                self.deck = waitingLinePainting.pop()
                yield self.hold(20)
                self.deck.activate()
            else:
                yield self.wait((trabalho, True))


class Storage2(sim.Component):
    def process(self):
        print("CHEGUEI A STORAGE 2")
        """aux = []
        while True:
            if trabalho.get() is False:
                while len(waitingLineStorage2) > 0:
                    self.deck = waitingLineStorage2.pop()
                    aux.append(self.deck)
                yield self.hold((DAY * (NUM_DIAS + 1)) - env.now())
                for i in aux:
                    i.activate()
            else:
                yield self.wait((trabalho, False))"""


# ---------------------------------------------------- WHEEL -----------------------------------------------------------


class Foundry(sim.Component):
    def process(self):
        while True:
            while len(waitingLineFoundry) == 0:
                yield self.passivate()
            if trabalho.get():
                self.wheel = waitingLineFoundry.pop()
                yield self.hold(55)
                self.wheel.activate()
            else:
                yield self.wait((trabalho, True))


class Storage3(sim.Component):
    def process(self):
        aux = []
        while True:
            if trabalho.get() is False:
                while len(waitingLineStorage3) > 0:
                    self.deck = waitingLineStorage3.pop()
                    aux.append(self.deck)
                yield self.hold((DAY * (NUM_DIAS + 1)) - env.now())
                for i in aux:
                    i.activate()
            else:
                yield self.wait((trabalho, False))


class Machining(sim.Component):
    def process(self):
        while True:
            while len(waitingLineMachining) == 0:
                yield self.passivate()
            if trabalho.get():
                self.wheel = waitingLineMachining.pop()
                yield self.hold(60)
                self.wheel.activate()
            else:
                yield self.wait((trabalho, True))


class Printing(sim.Component):
    def process(self):
        while True:
            while len(waitingLinePrinting) == 0:
                yield self.passivate()
            if trabalho.get():
                self.wheel = waitingLinePrinting.pop()
                yield self.hold(20)
                self.wheel.activate()
            else:
                yield self.wait((trabalho, True))


class Storage4(sim.Component):
    def process(self):
        print("CHEGUEI A STORAGE 4")
        """aux = []
        while True:
            if trabalho.get() is False:
                while len(waitingLineStorage1) > 0:
                    self.deck = waitingLineStorage1.pop()
                    aux.append(self.deck)
                yield self.hold((DAY * (NUM_DIAS + 1)) - env.now())
                for i in aux:
                    i.activate()
            else:
                yield self.wait((trabalho, False))"""


env = sim.Environment(time_unit="minutes", trace=True)

# Filas para pranchas
pranchas = (5280 + 8 * 440) / 22

waitingLinePressing = sim.Queue("Line for pressing")
waitingLineStorage1 = sim.Queue("Storage 1")
waitingLineCutting = sim.Queue("Line for cutting")
waitingLineFinishing = sim.Queue("Line for finishing")
waitingLinePainting = sim.Queue("Line for painting")
waitingLineStorage2 = sim.Queue("Storage 2")
pressing = [Pressing() for i in range(4)]
storage1 = Storage1()
cutting = [Cutting() for i in range(3)]
finishing = Finishing()
painting = Painting()
storage2 = Storage2()

lote_decks = [DeckGenerator(num_deck=pranchas)]     # '''for _ in range(22)'''

# Filas para rodas
rodas = (5280 * 4 + 4 * 2640) / 22

waitingLineFoundry = sim.Queue("Line for foundry")
waitingLineStorage3 = sim.Queue("Storage 3")
waitingLineMachining = sim.Queue("Line for machining")
waitingLinePrinting = sim.Queue("Line for printing")
waitingLineStorage4 = sim.Queue("Storage 4")
foundry = Foundry()
storage3 = Storage3()
machining = [Machining() for i in range(2)]
printing = Printing()
storage4 = Storage4()

lote_rodas = [WheelGenerator(num_wheels=rodas)]      # o ciclo for pode ter logica '''for _ in range(22)'''

trabalho = sim.State("trabalho", value=True)
gestor = SimulationManager()

env.run(END)  # 10560

waitingLinePressing.print_statistics()
print()
waitingLineStorage1.print_statistics()
print()
waitingLineCutting.print_statistics()
print()
waitingLineFinishing.print_statistics()
print()
waitingLinePainting.print_statistics()
print()
waitingLineStorage2.print_statistics()
print()

waitingLineFoundry.print_statistics()
print()
waitingLineStorage3.print_statistics()
print()
waitingLineMachining.print_statistics()
print()
waitingLinePrinting.print_statistics()
print()
waitingLineStorage4.print_statistics()
