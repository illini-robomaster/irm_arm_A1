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
        motor.id = state['id']
        motor.mode = state['mode']
        motor.T = state['T']
        motor.W = state['W']
        motor.Pos = state['Pos']
        motor.K_P = state['K_P']
        motor.K_W = state['K_W']

    @staticmethod
    def update_state_from_motor(motor, state):
        state['id'] = motor.id
        state['mode'] = motor.mode
        state['T'] = motor.T
        state['W'] = motor.W
        state['Pos'] = motor.Pos
        state['K_P'] = motor.K_P
        state['K_W'] = motor.K_W

    def set_state_send(self, new_state):
        # [s]elf [k]eys
        sk_set = set(self.state)
        # [n]ew --
        nk_set = set(new_state)
        existing_keys = sk_set | (sk_set & nk_set)
        for k in existing_keys:
            self.state[k] = new_state['k']
        self.update_motor_from_state(self.motor_send, self.state_send)

    def send(self):
        self.cdll.modify_data(Types.byref(self.motor_send))
        self.cdll.send_recv(self.fd, Types.byref(self.motor_send),
                                     Types.byref(self.motor_recv))

    def recv(self):
        self.cdll.extract_data(Types.byref(self.motor_recv))
        self.update_state_from_motor(self.motor_recv, self.state_recv)

    def get_state_send(self):
        return self.state_send.copy()

    def get_state_recv(self):
        return self.state_recv.copy()

    def stop(self):
        # Reset everything but `id` to 0
        id_ = self.state_send.id
        new_state = dict.fromkeys(self.state_send, 0)
        new_state['id'] = id_
        self.set_state(new_state)
        self.send()

