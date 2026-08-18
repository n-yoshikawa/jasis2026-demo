import time

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from magician import MagicianController
from picus import PicusWired


class MySDL:   
    def __init__(self):
        self.home_pose = (200, 0, 100)
        self.dobot = MagicianController()
        self.picus = PicusWired("46781074")
        self.return_home()

    def return_home(self) -> str:
        """
        Move the robot arm to its predefined home position.
        """
        try:
            self.dobot.move_arm(z=self.home_pose[2])
            self.dobot.move_arm(x=self.home_pose[0])
            self.dobot.move_arm(y=self.home_pose[1])
            # self.dobot.move_arm(self.home_pose[0], self.home_pose[1], self.home_pose[2])
            return "robot returned home successfully"
        except Exception as e:
            print(e)
            return f"failed to return home, error: {e}"

    def move_above_beaker(self) -> str:
        """
        Move the robot above the beaker.
        """
        try:
            self.dobot.move_arm(z=100)
            self.dobot.move_arm(x=200)
            self.dobot.move_arm(y=0)
            return f"robot moved to above the beaker"
        except Exception as e:
            raise ToolError(f"failed to move to color well, error: {e}")
    
    def add_base(self, volume: float) -> str:
        """
        Add volume (mL) of base in the beaker.
        Volume must be between 0 to 10.
        """
        try:
            self.dobot.move_arm(z=100)
            self.dobot.move_arm(x=200)
            self.dobot.move_arm(y=75)

            self.aspirate(volume)
            self.move_above_beaker()
            self.dispense(volume)
            self.stir_beaker()
            return f"{volume} mL of base was added to the beaker"
        except Exception as e:
            raise ToolError(f"failed to add base, error: {e}")

    def add_acid(self, volume: float) -> str:
        """
        Add volume (ml) of acid in the beaker.
        Volume must be between 0 to 10.
        """
        try:
            self.dobot.move_arm(z=100)
            self.dobot.move_arm(x=200)
            self.dobot.move_arm(y=-75)

            self.aspirate(volume)
            self.move_above_beaker()
            self.dispense(volume)
            self.stir_beaker()
            return f"{volume} mL of acid was added to the beaker"
        except Exception as e:
            raise ToolError(f"failed to move to mix well, error: {e}")

    def aspirate(self, volume: float) -> str:
        """
        Aspirate the specified liquid volume (in mL).

        The arm moves to aspirate height, performs aspiration,
        and returns to the home Z position.

        Args:
          volume: Liquid volume to aspirate.
        """
        try:
            self.dobot.move_arm(z=0)
            self.picus.aspirate(volume)
            return f"robot aspirated {volume} mL"
        except Exception as e:
            raise ToolError(f"robot failed to aspirate {volume} mL, error: {e}")

    def dispense(self, volume: float) -> str:
        """
        Dispense the specified liquid volume (in mL).

        The arm performs dispensing without moving Z position.

        Args:
          volume: Liquid volume to dispense.
        """
        try:
            self.dobot.move_arm(z=70)
            self.picus.dispense(volume)
            self.picus.blow_out()
            return f"robot dispensed {volume} mL"
        except Exception as e:
            print(e)
            raise ToolError(f"robot failed to dispense {volume} mL, error: {e}")


    def stir_beaker(self) -> str:
        """Stirs beaker."""
        self.move_above_beaker()
        for _ in range(2):
            self.aspirate(10)
            time.sleep(2)
            self.dispense(10)
            time.sleep(2)
        self.move_above_beaker()
        return "Finish stirring beaker."
   
if __name__ == "__main__":
    sdl = MySDL()
    mcp = FastMCP("Self-driving laboratory controller")
    mcp.tool(sdl.return_home)
    # mcp.tool(sdl.move_above_beaker)
    mcp.tool(sdl.add_acid)
    mcp.tool(sdl.add_base)
    # mcp.tool(sdl.aspirate)
    # mcp.tool(sdl.dispense)
    # mcp.tool(sdl.stir_beaker) 
    mcp.run(transport="http", host="0.0.0.0", port=8001)