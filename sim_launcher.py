import flags
import Mode
flags.MAIN_FLAGS.add(Mode.SIMULATE)
from farmlib import *
import main
main.main(flags.MAIN_FLAGS)
