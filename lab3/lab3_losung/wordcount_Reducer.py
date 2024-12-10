import Splitter as sp
import Mapper as mp
import Reducer as rd

import constPipe as const
import sys

me = str(sys.argv[1])

if __name__ == "__main__":
    # Argument aus der Konsole lesen
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])  # Portnummer aus den Argumenten
    const.PORT1 = port  # Setze den Port (falls nötig)

    reducer = rd.Reducer(port)
    reducer.start()

#reducers = {
#    rd.Reducer(const.PORT1),
#    rd.Reducer(const.PORT2)
#}

#for reducer in reducers:
#    reducer.start()