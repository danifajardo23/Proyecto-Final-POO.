import tkinter as tk

# --- Singleton ---
class ArmController:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.state = "idle"
        return cls._instance
    def move(self, command):
        print(f"[Controller] Ejecutando: {command}")
        self.state = command

# --- Strategy ---
class ControlStrategy:
    def control(self):
        pass

class ManualControl(ControlStrategy):
    def control(self):
        return "Control manual activado"

# --- Observer ---
class Observer:
    def update(self, state):
        pass

class Logger(Observer):
    def update(self, state):
        print(f"[Logger] Nuevo estado: {state}")

# --- Adapter ---
class OldAPI:
    def do_action(self):
        return "Ejecutando acción antigua"

class Adapter:
    def __init__(self, old_api):
        self.old_api = old_api
    def execute(self):
        return self.old_api.do_action()

# --- Factory Method ---
class Movement:
    def execute(self):
        pass

class MoveUp(Movement):
    def execute(self):
        return "Brazo movido arriba"

class MoveDown(Movement):
    def execute(self):
        return "Brazo movido abajo"

class moveAgarrar(Movement):
    def execute(self):
        return "Brazo agarando un baso"

class moveSaludar(Movement):
    def execute(self):
        return "Brazo dando la mano"


class MovementFactory:
    @staticmethod
    def create(direction):
        if direction == "up":
            return MoveUp()
        elif direction == "down":
            return MoveDown()
        elif direction == "agarrar":
            return moveAgarrar()
        elif direction == "saludar":
            return moveSaludar()
        else:
            raise ValueError("Dirección inválida")

# --- Robotic Arm con Observer ---
class RoboticArm:
    def __init__(self):
        self.observers = []
        self.position = 0
    def add_observer(self, obs):
        self.observers.append(obs)
    def notify(self, msg):
        for obs in self.observers:
            obs.update(msg)
    def move(self, movement):
        result = movement.execute()
        self.position += 1
        self.notify(result)
        return result

# --- Interfaz Tkinter ---
def main():
    controller = ArmController()
    arm = RoboticArm()
    arm.add_observer(Logger())
    strategy = ManualControl()
    print(strategy.control())

    old_api = OldAPI()
    adapter = Adapter(old_api)
    print("[Adapter] " + adapter.execute())

    def move_up():
        mov = MovementFactory.create("up")
        res = arm.move(mov)
        controller.move(res)
        lbl.config(text=res)

    def move_down():
        mov = MovementFactory.create("down")
        res = arm.move(mov)
        controller.move(res)
        lbl.config(text=res)

    def move_agarrar():
        mov = MovementFactory.create("agarrar")
        res = arm.move(mov)
        controller.move(res)
        lbl.config(text=res)

    def move_saludar():
        mov = MovementFactory.create("saludar")
        res = arm.move(mov)
        controller.move(res)
        lbl.config(text=res)

    # Tkinder
    win = tk.Tk()
    win.title("Simulador Brazo Robótico")
    tk.Button(win, text="Mover Arriba", command=move_up).pack(pady=5)
    tk.Button(win, text="Mover Abajo", command=move_down).pack(pady=5)
    tk.Button(win, text="Agarrando un vaso", command=move_agarrar).pack(pady=5)
    tk.Button(win, text="dando la mano", command=move_saludar).pack(pady=5)
    lbl = tk.Label(win, text="Esperando orden...")
    lbl.pack(pady=20)
    win.mainloop()

main()
