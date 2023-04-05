
class Syringe():
    def __init__(self) -> None:
        self.height: int = 81
    def __repr__(self) -> str:
        return "Syringe()"
class LPen():
    def __init__(self) -> None:
        self.height: int = 64,5
    def __repr__(self) -> str:
        return "LPen()"
    
class SPen():
    def __init__(self) -> None:
        self.height: int = 36.18
    def __repr__(self) -> str:
        return "SPen()"
class Glas():
    def __init__(self) -> None:
        self.height: int = 61.25
    def __repr__(self) -> str:
        return "Glas()"

class LTray():
    def __init__(self, syr_samp: int, syr_batch: int, pen_samp: int, pen_batch: int) -> None:
        self.syr_samp = syr_samp
        self.syr_batch = syr_batch
        self.pen_samp = pen_samp
        self.pen_batch = pen_batch
        self.width : float = 0.116
        self.height : float = 0.231
        self.row : int = 15
        self.col : int = 6
        # self.pos : tuple = (66.38, 64.75)
        # self.start: tuple = (11.68, 7.63)
        self.sep_x = 0.01838
        self.sep_y = 0.015
        self.elevation_syr = 0.10
        self.elevation_pen = 0.40
        ##get actual pose with robot
        self.initial_pose = [-0.4104577419847799, -0.2626529489715343, 0.2972660465054066, 
                             1.8552623321968715, 2.420037547531281, -0.014278932653435552]
        # self.poses: list[list] = [[None]* self.col for _ in range(self.row)]
        # self.poses[0][0] = self.initial_pose

    def create_matrix(self):
        matrix = [[None] * self.col for _ in range(self.row)]
        for i in range(self.syr_batch):
            for j in range(self.syr_samp):
                matrix[i][j] = Syringe() 

        for i in range(self.syr_batch, self.syr_batch+self.pen_batch):
            for j in range(self.pen_samp):
                matrix[i][j] = LPen() 
        return matrix

class STray():
    def __init__(self, pen_samp: int, pen_batch: int) -> None:
        self.pen_samp = pen_samp
        self.pen_batch = pen_batch
        self.width : int = 75.25
        self.height : int = 191
        self.row : int = 12
        self.col : int = 4
        self.pos : tuple = (234.38, 64.75)
        self.start: tuple = (11.6, 10)
        self.sep_x = 17.35 / 1000
        self.sep_y = 15 / 1000
        self.elevation = 0

    def create_matrix(self):
        matrix = [[None] * self.col for _ in range(self.row)]
        for i in range(self.pen_batch):
            for j in range(self.pen_samp):
                matrix[i][j] = SPen() 
        return matrix

class Out_tray():
    def __init__(self, syr_batch: int, Lpen_batch: int, Spen_batch) -> None:
        self.elevation = 10
        self.row = 9    
        self.col = 3
        self.Lpen_batch= Lpen_batch
        self.Spen_batch= Spen_batch
        self.syr_batch = syr_batch
        self.out_samp = syr_batch + Spen_batch + Lpen_batch
        self.sep_row = 0.023
        self.sep_col = 0.02

    
    def create_matrix(self):
        matrix = [[None] * self.col for _ in range(self.row)]
        full_rows = self.out_samp // self.col
        residu = self.out_samp % self.col
        for i in range(full_rows):
            for j in range(self.col):
                matrix[i][j] = Glas()
        for i in range(full_rows, full_rows+1):
            for j in range(residu):
                matrix[i][j] = Glas()
        return matrix

            

# L = LTray(2,4,2,2)
# S = STray(2,2)
# mat = L.create_matrix()
# mat2 = Out_tray(L.syr_batch, L.pen_batch, S.pen_batch).create_matrix()
# print(mat)
# print("mat2")
# print(isinstance(mat2[1][1],Glas))