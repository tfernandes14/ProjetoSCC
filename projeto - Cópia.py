# No relatorio, incluir a distribuição usada
# Nos varios processos, nao usar valores especificos no self.hold(...), usar distribuiçoes tipo uniforme
# Dps das storages 2 e 4, as coisas so vao (em teoria, para exportaçao, mas nao esta operacional)
# CORRER 24 FUCKING DIAS


YO = 24
DAY = 1440
END = 1440 * YO  # 4320
NUM_DIAS = 0
RODAS = 0
DECKS = 0
SKATES = 0

import salabim as sim
import matplotlib.pyplot as plt


class SimulationManager(sim.Component):
    def process(self):
        global DAY, NUM_DIAS
        print("SIMULATION MANAGER BROOO")
        while True:
            # 480 = 8h / 960 = 16h / 1440 = 24h
            pressingState.set(value=True)
            storage1State.set(value=True)
            cuttingState.set(value=True)
            finishingState.set(value=True)
            paintingState.set(value=True)
            storage2State.set(value=True)
            exportDecksState.set(value=True)

            foundryState.set(value=True)
            storage3State.set(value=True)
            machiningState.set(value=True)
            printingState.set(value=True)
            storage4State.set(value=True)
            exportWheelsState.set(value=True)

            assemblySkatesState.set(value=True)
            yield self.hold(380)
            pressingState.set(value=False)
            yield self.hold(40)  # min 420 do dia
            cuttingState.set(value=False)
            machiningState.set(value=False)
            yield self.hold(5)  # min 425
            foundryState.set(value=False)
            yield self.hold(25)  # min 450
            exportWheelsState.set(value=False)
            assemblySkatesState.set(value=False)
            yield self.hold(10)  # min 460
            paintingState.set(value=False)
            printingState.set(value=False)
            yield self.hold(5)  # min 465
            finishingState.set(value=False)
            yield self.hold(5)  # min 470
            exportDecksState.set(value=False)

            yield self.hold(10)  # min 480
            storage1State.set(value=False)
            storage2State.set(value=False)
            storage3State.set(value=False)
            storage4State.set(value=False)
            yield self.hold(960)
            NUM_DIAS += 1
            if env.now() == END:
                break


class Deck(sim.Component):
    def process(self):
        global DECKS
        # Pressing
        self.enter(waitingLinePressing)
        for press in pressing:
            if press.ispassive():
                press.activate()
                break
        yield self.passivate()

        # Storage 1
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
        yield self.passivate()

        # Decisão final
        if DECKS % 10 == 0 or DECKS % 10 == 1 or DECKS % 10 == 2 or DECKS % 10 == 3 or DECKS % 10 == 4 or DECKS % 10 == 5:  # Vai para montagem de skates
            DECKS += 1
            print("MONTAGEM DOS SKATES")
            print("NUMERO DE DECKS POS FEITO:", DECKS)
            self.enter(waitingLineAssemblyDecks)
            for ska in skateWorker:
                if ska.ispassive():
                    ska.activate()
            yield self.passivate()
        else:  # Vai para exportação
            DECKS += 1
            for i in range(2):
                DeckBox()


class Skate(sim.Component):
    def process(self):
        global SKATES
        aux = []
        print("PRE MONTAGEM SKATES")
        while True:
            while len(waitingLineAssemblyDecks) == 0 or len(waitingLineAssemblyWheels) == 0:
                yield self.passivate()
            if assemblySkatesState.get():
                # print("A BARBARA E FEIA")
                if len(waitingLineAssemblyDecks) >= 2 and len(waitingLineAssemblyWheels) >= 1:
                    print("O TIAGO E GIRO")
                    self.wheel = waitingLineAssemblyWheels.pop()
                    for i in range(2):
                        self.deck = waitingLineAssemblyDecks.pop()
                        aux.append(self.deck)
                    yield self.hold(30)     # 30
                    if self.wheel.ispassive():
                        self.wheel.activate()
                    for i in aux:
                        if i.ispassive():
                            i.activate()
                    SKATES += 48
            else:
                print("WAIT ASSEMBLY")
                yield self.wait((assemblySkatesState, True))


class DeckBox(sim.Component):
    def process(self):
        self.enter(waitingLineExportDecks)
        for exp in exportDecks:
            if exp.ispassive():
                exp.activate()
                break
        yield self.passivate()
        print("NUMERO DE DECKS POS FEITO:", DECKS)


class Wheel(sim.Component):
    def process(self):
        global RODAS
        # Foundry
        self.enter(waitingLineFoundry)
        if foundry.ispassive():
            foundry.activate()
        yield self.passivate()

        # Storage 3
        self.enter(waitingLineStorage3)
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
        yield self.passivate()

        # Decisão final
        if RODAS % 3 == 0 or RODAS % 3 == 1:  # Vai para montagem de skates
            RODAS += 1
            print("MONTAGEM DOS SKATES")
            print("NUMERO DE WHEELS POS FEITO:", RODAS)
            self.enter(waitingLineAssemblyWheels)
            for ska in skateWorker:
                if ska.ispassive():
                    ska.activate()
            yield self.passivate()
        else:  # Vai para exportação
            RODAS += 1
            for i in range(4):
                WheelGroup()


class WheelGroup(sim.Component):
    def process(self):
        self.enter(waitingLineExportWheels)
        exportWheels.activate()
        yield self.passivate()
        print("NUMERO DE WHEELS POS FEITO:", RODAS)


class WheelGenerator(sim.Component):
    def setup(self, num_wheels):
        self.num_wheels = num_wheels

    def process(self):
        while self.num_wheels > 0:
            Wheel()
            self.num_wheels -= 192


class DeckGenerator(sim.Component):
    def setup(self, num_deck):
        self.num_deck = num_deck

    def process(self):
        while self.num_deck > 0:
            Deck()
            self.num_deck -= 24


# ---------------------------------------------------- DECK ------------------------------------------------------------


class Pressing(sim.Component):
    def process(self):
        while True:
            while len(waitingLinePressing) == 0:
                yield self.passivate()
            if pressingState.get():
                self.deck = waitingLinePressing.pop()
                yield self.hold(100)  # 100
                if self.deck.ispassive():
                    self.deck.activate()
            else:
                yield self.wait((pressingState, True))


class Storage1(sim.Component):
    def process(self):
        aux = []
        while True:
            if storage1State.get() is False:
                while len(waitingLineStorage1) > 0:
                    self.deck = waitingLineStorage1.pop()
                    aux.append(self.deck)
                yield self.hold((DAY * (NUM_DIAS + 1)) - env.now())
                for i in aux:
                    if i.ispassive():
                        i.activate()
            else:
                yield self.wait((storage1State, False))


class Cutting(sim.Component):
    def process(self):
        while True:
            while len(waitingLineCutting) == 0:
                yield self.passivate()
            if cuttingState.get():
                self.deck = waitingLineCutting.pop()
                yield self.hold(60)     # 60
                if self.deck.ispassive():
                    self.deck.activate()
            else:
                yield self.wait((cuttingState, True))


class Finishing(sim.Component):
    def process(self):
        while True:
            while len(waitingLineFinishing) == 0:
                yield self.passivate()
            if finishingState.get():
                self.deck = waitingLineFinishing.pop()
                yield self.hold(15)     # 15
                if self.deck.ispassive():
                    self.deck.activate()
            else:
                yield self.wait((finishingState, True))


class Painting(sim.Component):
    def process(self):
        while True:
            while len(waitingLinePainting) == 0:
                yield self.passivate()
            if paintingState.get():
                self.deck = waitingLinePainting.pop()
                yield self.hold(20)     # 20
                if self.deck.ispassive():
                    self.deck.activate()
            else:
                yield self.wait((paintingState, True))


class Storage2(sim.Component):
    def process(self):
        print("CHEGUEI A STORAGE 2")
        aux = []
        while True:
            if storage2State.get() is False:
                while len(waitingLineStorage2) > 0:
                    self.deck = waitingLineStorage2.pop()
                    aux.append(self.deck)
                yield self.hold((DAY * (NUM_DIAS + 1)) - env.now())
                for i in aux:
                    if i.ispassive():
                        i.activate()
            else:
                yield self.wait((storage2State, False))


class PackingDecks(sim.Component):
    def process(self):
        print("CHEGUEI A EXPORTAÇAO DE DECKS")
        while True:
            while len(waitingLineExportDecks) == 0:
                yield self.passivate()
            if exportDecksState.get():
                self.deck = waitingLineExportDecks.pop()
                yield self.hold(10)     # 10
                if self.deck.ispassive():
                    self.deck.activate()
            else:
                yield self.wait((exportDecksState, True))


# ---------------------------------------------------- WHEEL -----------------------------------------------------------


class Foundry(sim.Component):
    def process(self):
        while True:
            while len(waitingLineFoundry) == 0:
                yield self.passivate()
            if foundryState.get():
                self.wheel = waitingLineFoundry.pop()
                yield self.hold(55)     # 55
                if self.wheel.ispassive():
                    self.wheel.activate()
            else:
                yield self.wait((foundryState, True))


class Storage3(sim.Component):
    def process(self):
        aux = []
        while True:
            if storage3State.get() is False:
                while len(waitingLineStorage3) > 0:
                    self.wheel = waitingLineStorage3.pop()
                    aux.append(self.wheel)
                yield self.hold((DAY * (NUM_DIAS + 1)) - env.now())
                for i in aux:
                    if i.ispassive():
                        i.activate()
            else:
                yield self.wait((storage3State, False))


class Machining(sim.Component):
    def process(self):
        while True:
            while len(waitingLineMachining) == 0:
                yield self.passivate()
            if machiningState.get():
                self.wheel = waitingLineMachining.pop()
                yield self.hold(60)     # 60
                if self.wheel.ispassive():
                    self.wheel.activate()
            else:
                yield self.wait((machiningState, True))


class Printing(sim.Component):
    def process(self):
        while True:
            while len(waitingLinePrinting) == 0:
                yield self.passivate()
            if printingState.get():
                self.wheel = waitingLinePrinting.pop()
                yield self.hold(20)     # 20
                if self.wheel.ispassive():
                    self.wheel.activate()
            else:
                yield self.wait((printingState, True))


class Storage4(sim.Component):
    def process(self):
        print("CHEGUEI A STORAGE 4")
        aux = []
        while True:
            if storage4State.get() is False:
                while len(waitingLineStorage4) > 0:
                    self.wheel = waitingLineStorage4.pop()
                    aux.append(self.wheel)
                yield self.hold((DAY * (NUM_DIAS + 1)) - env.now())
                for i in aux:
                    if i.ispassive():
                        i.activate()
            else:
                yield self.wait((storage4State, False))


class PackingWheels(sim.Component):
    def process(self):
        print("CHEGUEI A EXPORTAÇAO DE RODAS")
        while True:
            while len(waitingLineExportWheels) == 0:
                yield self.passivate()
            if exportWheelsState.get():
                self.wheel = waitingLineExportWheels.pop()
                yield self.hold(30)             # 30 - sim.Triangular(29, 31, 30).sample() - sim.Normal(30, 0.5).sample()
                if self.wheel.ispassive():
                    self.wheel.activate()
            else:
                yield self.wait((exportWheelsState, True))

# ------------------------------------------------ SIMULAÇÃO -----------------------------------------------------------


env = sim.Environment(time_unit="minutes", trace=False, random_seed=7654321)

# -------------------- DECKS --------------------

pranchas = (5280 + 8 * 440) / YO

# Filas para pranchas
waitingLinePressing = sim.Queue("Line for pressing")
waitingLineStorage1 = sim.Queue("Line for Storage 1")
waitingLineCutting = sim.Queue("Line for cutting")
waitingLineFinishing = sim.Queue("Line for finishing")
waitingLinePainting = sim.Queue("Line for painting")
waitingLineStorage2 = sim.Queue("Line for Storage 2")
waitingLineExportDecks = sim.Queue("Line for export decks")
pressing = [Pressing() for i in range(4)]
pressingState = sim.State("pressingState", value=True)
storage1 = Storage1()
storage1State = sim.State("storage1State", value=True)
cutting = [Cutting() for i in range(3)]
cuttingState = sim.State("cuttingState", value=True)
finishing = Finishing()
finishingState = sim.State("finishingState", value=True)
painting = Painting()
paintingState = sim.State("paintingState", value=True)
storage2 = Storage2()
storage2State = sim.State("storage2State", value=True)
exportDecks = [PackingDecks() for i in range(2)]
exportDecksState = sim.State("exportDecksState", value=True)

lote_decks = [DeckGenerator(num_deck=pranchas) for i in range(YO)]  # '''for _ in range(22)'''

# -------------------- RODAS --------------------

rodas = (5280 * 4 + 4 * 2640) / YO  # Numero de rodas diarias

# Filas e processos para as rodas
waitingLineFoundry = sim.Queue("Line for foundry")
waitingLineStorage3 = sim.Queue("Line for Storage 3")
waitingLineMachining = sim.Queue("Line for machining")
waitingLinePrinting = sim.Queue("Line for printing")
waitingLineStorage4 = sim.Queue("Line for Storage 4")
waitingLineExportWheels = sim.Queue("Line for export wheels")
foundry = Foundry()
foundryState = sim.State("foundryState", value=True)
storage3 = Storage3()
storage3State = sim.State("storage3State", value=True)
machining = [Machining() for i in range(2)]
machiningState = sim.State("machiningState", value=True)
printing = Printing()
printingState = sim.State("printingState", value=True)
storage4 = Storage4()
storage4State = sim.State("storage4State", value=True)
exportWheels = PackingWheels()
exportWheelsState = sim.State("exportWheelsState", value=True)

lote_rodas = [WheelGenerator(num_wheels=rodas) for i in range(YO)]      # o ciclo for pode ter logica '''for _ in range(22)'''

# -------------------- PACKING OU ASSEMBLY --------------------

waitingLineAssemblyWheels = sim.Queue("Line for assembly (Wheels)")
waitingLineAssemblyDecks = sim.Queue("Line for assembly (Decks)")
assemblySkatesState = sim.State("assemblySkatesState", value=True)
skateWorker = [Skate() for i in range(2)]

gestor = SimulationManager()

env.run(END)

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
waitingLineExportDecks.print_statistics()
print()
waitingLineAssemblyDecks.print_statistics()
print(end='\n\n')

waitingLineFoundry.print_statistics()
print()
waitingLineStorage3.print_statistics()
print()
waitingLineMachining.print_statistics()
print()
waitingLinePrinting.print_statistics()
print()
waitingLineStorage4.print_statistics()
print()
waitingLineExportWheels.print_statistics()
print()
waitingLineAssemblyWheels.print_statistics()

print(end="\n\n")
print("Número de skates feitos:", SKATES)

plt.figure(1)
plt.plot(*waitingLinePressing.length.tx(), drawstyle="steps-post")
plt.title("Waiting Line Pressing")
plt.figure(2)
plt.plot(*waitingLineStorage1.length.tx(), drawstyle="steps-post")
plt.title("Waiting Line Storage 1")
plt.figure(3)
plt.plot(*waitingLineCutting.length.tx(), drawstyle="steps-post")
plt.title("Waiting Line Cutting")
plt.figure(4)
plt.plot(*waitingLineFinishing.length.tx(), drawstyle="steps-post")
plt.title("Waiting Line Finishing")
plt.figure(5)
plt.plot(*waitingLinePainting.length.tx(), drawstyle="steps-post")
plt.title("Waiting Line Painting")
plt.figure(6)
plt.plot(*waitingLineStorage2.length.tx(), drawstyle="steps-post")
plt.title("Waiting Line Storage2")
plt.figure(7)
plt.plot(*waitingLineExportDecks.length.tx(), drawstyle="steps-post")
plt.title("Waiting Line Export Decks")
plt.figure(8)
plt.plot(*waitingLineAssemblyDecks.length.tx(), drawstyle="steps-post")
plt.title("Waiting Line Assembly Decks")
plt.figure(9)
plt.plot(*waitingLineFoundry.length.tx(), drawstyle="steps-post")
plt.title("Waiting Line Foundry")
plt.figure(10)
plt.plot(*waitingLineStorage3.length.tx(), drawstyle="steps-post")
plt.title("Waiting Line Storage3")
plt.figure(11)
plt.plot(*waitingLineMachining.length.tx(), drawstyle="steps-post")
plt.title("Waiting Line Machining")
plt.figure(12)
plt.plot(*waitingLinePrinting.length.tx(), drawstyle="steps-post")
plt.title("Waiting Line Printing")
plt.figure(13)
plt.plot(*waitingLineStorage4.length.tx(), drawstyle="steps-post")
plt.title("Waiting Line Storage4")
plt.figure(14)
plt.plot(*waitingLineExportWheels.length.tx(), drawstyle="steps-post")
plt.title("Waiting Line Export Wheels")
plt.figure(15)
plt.plot(*waitingLineAssemblyWheels.length.tx(), drawstyle="steps-post")
plt.title("Waiting Line Assembly Wheels")
plt.show()
