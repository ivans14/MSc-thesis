import random
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

class Tray():
    def __init__(self, syr_samp: int, syr_batch: int, Lpen_samp: int, Lpen_batch: int,Spen_samp: int, Spen_batch: int) -> None:
        self.syr_samp = syr_samp
        self.syr_batch = syr_batch
        self.Lpen_samp = Lpen_samp
        self.Lpen_batch = Lpen_batch
        self.Spen_samp = Spen_samp
        self.Spen_batch = Spen_batch
        self.width : float = 0.116
        self.height : float = 0.231
        self.row : int = 26
        self.col : int = 6
        # self.pos : tuple = (66.38, 64.75)
        # self.start: tuple = (11.68, 7.63)
        self.sep_x = 0.024
        self.sep_x_double = self.sep_x*6
        self.sep_y = 0.01425
        self.elevation_syr = 0.10
        self.elevation_pen = 0.40
        ##get actual pose with robot
        self.initial_pose = [-0.4104577419847799, -0.2626529489715343, 0.2972660465054066, 
                             1.8552623321968715, 2.420037547531281, -0.014278932653435552]
        # self.poses: list[list] = [[None]* self.col for _ in range(self.row)]
        # self.poses[0][0] = self.initial_pose

    def create_matrix(self, only_decap):
        matrix = [[None] * self.col for _ in range(self.row)]
        row = 0
        col = 0
        count = 0
        if only_decap:
            while count < self.Lpen_samp + self.Spen_samp:
                print(row,col)
                if count < self.Spen_samp:
                    matrix[row][col] = SPen()
                else: 
                    matrix[row][col] = LPen()
                col += 1
                if col > 5:
                    col = 0
                    row += 1
                count += 1

            

        else:
            for i in range(self.syr_batch):
                col = 0
                for j in range(self.syr_samp):
                    if col>5:
                        row+=1
                        col=0
                    # row=count+i
                    print(row,col)
                    matrix[row][col] = Syringe() 
                    col += 1 
                row+=1
            for i in range(row, row+self.Lpen_batch):
                for j in range(self.Lpen_samp):
                    matrix[i][j] = LPen() 
                row += 1
            for i in range(row, row+self.Spen_batch):
                for j in range(self.Spen_samp):
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
        self.sep_col = 0.02306
        self.sep_row = 0.02

    
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