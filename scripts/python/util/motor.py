# Illinois RoboMaster 2024
from util.typedef import Types

class Motor:
    """Wrapper for MOTOR_{send,recv}"""
    def __init__(self, cdll, fd, id_, mode, T, W, Pos, K_P, K_W):
        self.cdll = cdll  # cdll
        self.fd = fd

        self.motor_send = Types.MOTOR_send()
        self.motor_recv = Types.MOTOR_recv()
        self.state_send = {
            'id': id_,    # Motor id
            'mode': mode, # Mode: 0 is stop, 5 is open-loop slow rotation, 10 is close-loop control
            'T': T,       # Feedforward torque
            'W': W,       # Angular velocity
            'Pos': Pos,   # Angle position
            'K_P': K_P,   # kp parameter in PID
            'K_W': K_W,   # kd parameter in PID
        }
        self.state_recv = dict.fromkeys(self.state_send, 0.0)

        self.update_motor_from_state(self.motor_send, self.state_send)
        self.update_state_from_motor(self.motor_recv, self.state_recv)

    @staticmethod
    def update_motor_from_state(motor, state):
        """Update a MOTOR_* object from a state dict"""
        motor.id = state['id']
        motor.mode = state['mode']
        motor.T = state['T']
        motor.W = state['W']
        motor.Pos = state['Pos']
        motor.K_P = state['K_P']
        motor.K_W = state['K_W']

    @staticmethod
    def update_state_from_motor(motor, state):
        """Update a state dict from a MOTOR_* object"""
        state['id'] = motor.id
        state['mode'] = motor.mode
        state['T'] = motor.T
        state['W'] = motor.W
        state['Pos'] = motor.Pos
        state['K_P'] = motor.K_P
        state['K_W'] = motor.K_W

    def set_state_send(self, **new_state):
        """Set the state_send dictionary and update MOTOR_send"""
        # [s]elf [k]eys, [n]ew ...
        sk_set = set(self.state)
        nk_set = set(new_state)

        existing_keys = sk_set | (sk_set & nk_set)
        self.state |= {k: v
                       for k, v in new_state.items()
                       if k in existing_keys}
        self.update_motor_from_state(self.motor_send, self.state_send)

    def send(self):
        """Send the current MOTOR_send to fd"""
        self.cdll.modify_data(Types.byref(self.motor_send))
        self.cdll.send_recv(self.fd,
            Types.byref(self.motor_send), Types.byref(self.motor_recv))

    def recv(self):
        """Update state_recv from current MOTOR_recv"""
        self.cdll.extract_data(Types.byref(self.motor_recv))
        self.update_state_from_motor(self.motor_recv, self.state_recv)

    def get_state_send(self):
        """Return a shallow copy of state_send"""
        return self.state_send.copy()

    def get_state_recv(self):
        """Return a shallow copy of state_recv"""
        return self.state_recv.copy()

    def stop(self):
        """Reset everything but id to 0"""
        id_ = self.state_send.id
        new_state = dict.fromkeys(self.state_send, 0)
        new_state['id'] = id_
        self.set_state_send(**new_state)
        self.send()
