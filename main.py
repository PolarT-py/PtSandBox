import sys
from game import *

if __name__ == "__main__":
    sb = SandBox()

    while sb.running:
        sb.get_events()
        sb.update()
        sb.draw()
    pygame.quit()
    sys.exit()
