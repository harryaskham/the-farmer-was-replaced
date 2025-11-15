import flags
flags.MAIN_FLAGS.append(Mode.SIMULATE)
from farmlib import *
import main
main.main(flags.MAIN_FLAGS)
