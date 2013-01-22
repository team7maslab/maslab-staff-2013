import stateMachine, time, sys

runTime = 180

state = stateMachine.State()

try:
    stopTime = time.time() + runTime
    timeLeft = stopTime - time.time()

    state.stopTime = stopTime
    state.nextState(stopTime)
except KeyboardInterrupt:
    sys.exit(0)
