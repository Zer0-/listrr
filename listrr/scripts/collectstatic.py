from bricks import Bricks
from bricks.static_builder import establish_static_assets
from listrr.application import components, routemap

if __name__ == "__main__":
    bricks = Bricks()
    for component in components:
        bricks.add(component)
    bricks.add(routemap)
    establish_static_assets(bricks)

