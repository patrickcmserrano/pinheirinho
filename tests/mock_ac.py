# Mocking the Assetto Corsa API for local testing
# This file mimics the structure of 'ac' and 'acsys' modules

class _AC_SYS_MOCK:
    class CS:
        SpeedKMH = 0
        WorldPosition = 1
        # Add others as needed

sys = _AC_SYS_MOCK()

def console(msg):
    print("[AC_MOCK_CONSOLE] {}".format(msg))

def getCarState(car_id, query_type):
    if query_type == sys.CS.WorldPosition:
        return (0.0, 0.0, 0.0)
    elif query_type == sys.CS.SpeedKMH:
        return 0.0
    return 0

def log(msg):
    print("[AC_MOCK_LOG] {}".format(msg))
