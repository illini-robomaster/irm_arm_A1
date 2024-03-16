# Illinois RoboMaster 2024
from util.typedef import Types

class Motor:
    """Wrapper for MOTOR_{send,recv}"""
    def __init__(self, cdll, fd,
                 id_=0, mode=0,
                 T=0.0, W=0.0, Pos=0.0, K_P=0.0, K_W=0.0):
        self.cdll = cdll
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
        self.state_recv = dict.fromkeys(self.state_send)  # Populate with None

        self.update_motor_from_state(self.motor_send, self.state_send)
        self.update_state_from_motor(self.motor_recv, self.state_recv)

    @staticmethod
    def update_motor_from_state(motor, state):
        """Update a typedef.Types.MOTOR_{send,recv} object from a state dict
        Expected bindings for typedef.Types.MOTOR_send instance:
        - K_P       :: float
        - K_W       :: float
        - Pos       :: float
        - T         :: float
        - W         :: float
        - id        :: int
        - mode      :: int
        It is unnessecary (and unexpected) to provide:
        - hex_len   :: int
        - motor_send_data
                    :: typedef.Types.MasterComdDataV3
        - send_time :: int
        These will be automatically generated in Motor(...).set_state_send(...)
        help(motor.Motor.update_state_from_motor) for typedef.Types.MOTOR_recv
        """
        for key in state:
            setattr(motor, key, state[key])

    @staticmethod
    def update_state_from_motor(motor, state):
        """Update a state dict from a typedef.Types.MOTOR_{send,recv} object
        Expected bindings for typedef.Types.MOTOR_recv instance:
        - Acc       :: int
        - LW        :: float
        - MError    :: int
        - Pos       :: float
        - T         :: float
        - Temp      :: int
        - W         :: float
        - acc       :: typedef.Types.c_float_Array_3
        - correct   :: int
        - gyro      :: typedef.Types.c_float_Array_3
        - hex_len   :: int
        - mode      :: int
        - motor_id  :: int
        - motor_recv_data
                    :: typedef.Types.ServoComdDataV3
        - recv_time :: int
        Keys not specified here will not experience side effects
        help(motor.Motor.update_motor_from_state) for typedef.Types.MOTOR_send
        """
        new_state = {attr: getattr(motor, attr)
                     for attr in dir(motor)
                     if not attr.startswith('_')}
        state |= new_state

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
        # Update motor_send.{hex_len,motor_send_data}
        self.cdll.modify_data(Types.byref(self.motor_send))

    def send(self):
        """Send the current MOTOR_send to fd"""
        self.cdll.send_recv(self.fd,
            Types.byref(self.motor_send), Types.byref(self.motor_recv))

    def recv(self):
        """Update state_recv from current MOTOR_recv"""
        self.cdll.extract_data(Types.byref(self.motor_recv))
        self.update_state_from_motor(self.motor_recv, self.state_recv)

    def get_state_send(self, *keys):
        """Return a shallow copy of state_send if no keys are provided
        Return the value corresponding to the key if one key provided
        Return a list of values if multiple keys are provided
        """
        if not keys:
            ret = self.state_send.copy()
        elif len(keys) == 1:
            ret = self.state_send[keys[0]]
        else:
            ret = [self.state_send[k]
                   for k in keys]
        return ret

    def get_state_recv(self, *keys):
        """Return a shallow copy of state_recv if no keys are provided
        Return the value corresponding to the key if one key provided
        Return a list of values if multiple keys are provided
        """
        if not keys:
            ret = self.state_recv.copy()
        elif len(keys) == 1:
            ret = self.state_recv[keys[0]]
        else:
            ret = [self.state_recv[k]
                   for k in keys]
        return ret

    def stop(self):
        """Reset everything but id to 0"""
        id_ = self.state_send.id
        new_state = dict.fromkeys(self.state_send, 0)
        new_state['id'] = id_
        self.set_state_send(**new_state)
        self.send()
