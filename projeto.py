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
        self.enter("")


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


env = sim.Environment(time_unit="minutes", trace=True)

pranchas = (5280 + 8 * 440) / 22
rodas = (5280 * 4 + 4 * 2640) / 22

# Filas para pranchas
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
waitingLineFoundry = sim.Queue("Line for foundry")
waitingLineMachining = sim.Queue("Line for machining")
waitingLinePrinting = sim.Queue("Line for printing")

lote_rodas = [WheelGenerator(num_wheels=rodas) for i in range(22)]

env.run(200)  # 10560
waitingLinePressing.print_statistics()
waitingLineCutting.print_statistics()
waitingLineFinishing.print_statistics()
waitingLinePainting.print_statistics()