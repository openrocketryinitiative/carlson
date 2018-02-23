# Test Logger

import logger

if __name__ == "__main__":

    l = logger.Logger()

    data = [1, 2, 3, 4, 5, 6]
    l.write(data)
    l.write("Wrote `data` to disk.", logger.DEBUG)

    data = [7, 4, 7, 3, 7, 4]
    l.write(data)
    l.write("Wrote new `data` to disk.", logger.DEBUG)