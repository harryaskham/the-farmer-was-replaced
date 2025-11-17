import flags
import Mode
flags.MAIN_FLAGS.add(Mode.TEST)
flags.MAIN_FLAGS.add(Mode.SIMULATE)
flags.MAIN_FLAGS.remove(Mode.RUN)
from farmlib import *
import main
main.main(flags.MAIN_FLAGS)
