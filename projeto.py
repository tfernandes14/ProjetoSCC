# Criar uma linha de montagem (pressing -> cutting -> ...)
# Storage - self.hold(16h)

import salabim as sim


class Deck(sim.Component):
    def process(self):
        # Pressing
        self.enter(waitingLinePressing)
        for press in pressing:
            if press.ispassive():
                press.activate()
                break
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


class Wheel(sim.Component):
    def process(self):
        # Foundry
        self.enter(waitingLineFoundry)
        if foundry.ispassive():
            foundry.activate()
        yield self.passivate()

        # Machining
        self.enter(waitingLineMachining)
        for mach in machining:
            if mach.ispassive():
                mach.activate()
            yield self.passivate()

        # Printing
        self.enter(waitingLinePrinting)
        if printing.ispassive():
            printing.activate()
        yield self.passivate()


class WheelGenerator(sim.Component):
    def setup(self, num_wheels):
        self.num_wheels = num_wheels

    def process(self):
        while self.num_wheels > 0:
            Wheel()
            self.num_wheels -= 1
            yield self.hold(sim.Uniform(200, 400).sample())


class DeckGenerator(sim.Component):
    def setup(self, num_deck):
        self.num_deck = num_deck

    def process(self):
        while self.num_deck > 0:
            Deck()
            self.num_deck -= 1
            yield self.hold(sim.Uniform(200, 400).sample())


class Pressing(sim.Component):
    def process(self):
        while True:
            while len(waitingLinePressing) == 0:
                yield self.passivate()
            self.deck = waitingLinePressing.pop()
            yield self.hold(100)
            self.deck.activate()


class Cutting(sim.Component):
    def process(self):
        while True:
            while len(waitingLineCutting) == 0:
                yield self.passivate()
            self.deck = waitingLineCutting.pop()
            yield self.hold(60)
            self.deck.activate()


class Finishing(sim.Component):
    def process(self):
        while True:
            while len(waitingLineFinishing) == 0:
                yield self.passivate()
            self.deck = waitingLineFinishing.pop()
            yield self.hold(15)
            self.deck.activate()


class Painting(sim.Component):
    def process(self):
        while True:
            while len(waitingLinePainting) == 0:
                yield self.passivate()
            self.deck = waitingLinePainting.pop()
            yield self.hold(20)
            self.deck.activate()


class Foundry(sim.Component):
    def process(self):
        while True:
            while len(waitingLineFoundry) == 0:
                yield self.passivate()
            self.wheel = waitingLineFoundry.pop()
            yield self.hold(55)
            self.wheel.activate()


class Machining(sim.Component):
    def process(self):
        while True:
            while len(waitingLineMachining) == 0:
                yield self.passivate()
            self.wheel = waitingLineMachining.pop()
            yield self.hold(60)
            self.wheel.activate()


class Printing(sim.Component):
    def process(self):
        while True:
            while len(waitingLinePrinting) == 0:
                yield self.passivate()
            self.wheel = waitingLinePrinting.pop()
            yield self.hold(20)
            self.wheel.activate()


env = sim.Environment(time_unit="minutes", trace=True)


# Filas para pranchas
pranchas = (5280 + 8 * 440) / 22

waitingLinePressing = sim.Queue("Line for pressing")
waitingLineCutting = sim.Queue("Line for cutting")
waitingLineFinishing = sim.Queue("Line for finishing")
waitingLinePainting = sim.Queue("Line for painting")
pressing = [Pressing() for i in range(4)]
cutting = [Cutting() for i in range(3)]
finishing = Finishing()
painting = Painting()

lote_decks = [DeckGenerator(num_deck=pranchas) for i in range(22)]

# Filas para rodas
rodas = (5280 * 4 + 4 * 2640) / 22

waitingLineFoundry = sim.Queue("Line for foundry")
waitingLineMachining = sim.Queue("Line for machining")
waitingLinePrinting = sim.Queue("Line for printing")
foundry = Foundry()
machining = [Machining() for i in range(2)]
printing = Printing()

lote_rodas = [WheelGenerator(num_wheels=rodas) for i in range(22)]

env.run(200)  # 10560
waitingLinePressing.print_statistics()
waitingLineCutting.print_statistics()
waitingLineFinishing.print_statistics()
waitingLinePainting.print_statistics()
waitingLineFoundry.print_statistics()
waitingLineMachining.print_statistics()
waitingLinePrinting.print_statistics()