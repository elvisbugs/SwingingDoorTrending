import numpy as np

class SwingingDoor:
    def __init__(self, first_point : tuple, deviation : float = 0.1, 
                t_max : float = 30.0) -> None : 

        self.t_max = t_max

        self.deviation = deviation

        y1 = first_point[1]
        self._superior_dev = y1 + deviation
        self._inferior_dev = y1 - deviation

        self._superior_line = float('inf')
        self._inferior_line = float('-inf')
        self.last_point = first_point

        self.compressed_data = list()

    def update_door(self, new_y: float) -> None:
        self._superior_dev = new_y + self.deviation
        self._inferior_dev = new_y - self.deviation

    def _generate_line(self, current_point: tuple, limit: float) -> float:
        x2 = current_point[0]
        y2 = current_point[1]

        return (self.t_max * (y2 - limit) + x2 * limit) / x2
         
    def check_door(self, current_point : tuple) -> bool:
        """Checks if the door is closed getting the points in `t_max` for the 
        superior and inferior line, if the inferior point is greater than 
        the superior point the door is closed, otherwise, it's open and the 
        data needs to be stored

        Args:
            last_point (tuple): x,y of the last point taked

        Returns:
            bool: True for closed door and False for open door
        """

        door_status = True

        #if x=0 skip the check of door
        if current_point[0] != 0:
            superior_line = self._generate_line(current_point, self._superior_dev)
            inferior_line = self._generate_line(current_point, self._inferior_dev)

            if superior_line > self._superior_line:
                self._superior_line = superior_line
            
            if inferior_line < self._inferior_line:
                self.inferior_line = inferior_line

            door_status = self._inferior_line > self._superior_line

        if door_status: #opened door, don't need to store the data
            self.last_point = current_point
        else: #closed door, need to store the data and last value
            self.compressed_data.append(self.last_point)
            self.compressed_data.append(current_point)
            self.update_door(current_point[1]) #updates the door with the new y

        return door_status
 