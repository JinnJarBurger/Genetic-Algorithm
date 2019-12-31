import random
import numpy as np
from math import factorial as fact
from queen import Queen
from numba import jit


class Genetic:

    @staticmethod
    @jit()
    def chromosome(n):
        chrom = []
        for i in range(n):
            chrom.append(random.randint(1, n))
        return chrom

    def population(self, n):
        chroms = []
        for i in range(50):
            chroms.append(self.chromosome(n))
        return chroms

    @staticmethod
    def make_queen(chrom):
        queens = []
        for i in range(1, len(chrom) + 1):
            queens.append(Queen([len(chrom) - (chrom[i - 1] - 1), i], False))
        return queens

    def attack_count(self, chrom):
        count = 0
        n = len(chrom)
        queens = self.make_queen(chrom)
        for j in range(n):
            # queen for comparison
            queen1 = queens[j]
            for i in range(n):
                # queen to be compared with
                queen2 = queens[i]
                if queen1 != queen2:
                    for k in range(1, n + 1):
                        # diagonal positions
                        pos_diag = [[queen1.pos[0] - (queen1.pos[0] - k),
                                     queen1.pos[1] + (queen1.pos[0] - k)],
                                    [queen1.pos[0] - (queen1.pos[0] - k),
                                     queen1.pos[1] - (queen1.pos[0] - k)]]

                        # horizontal/vertical positions
                        pos_hori_ver = [queen1.pos[0], queen1.pos[1]]

                        # diagonal check
                        if 1 <= int(pos_diag[0][0]) <= n and 1 <= int(pos_diag[0][1]) <= n:
                            if queen2.pos == pos_diag[0] and not queen2.visited:
                                count += 1
                                break

                        if 1 <= int(pos_diag[1][0]) <= n and 1 <= int(pos_diag[1][1]) <= n:
                            if queen2.pos == pos_diag[1] and not queen2.visited:
                                count += 1
                                break

                        # horizontal/vertical check
                        if queen2.pos[0] == pos_hori_ver[0] and not queen2.visited:
                            count += 1
                            break

                        if queen2.pos[1] == pos_hori_ver[1] and not queen2.visited:
                            count += 1
                            break

            queen1.visited = True

        return count

    @staticmethod
    def selection(chroms, fit):
        for i in range(len(chroms)):
            for j in range(i + 1, len(chroms)):
                if fit[i] < fit[j]:
                    temp1 = fit[i]
                    temp2 = chroms[i]
                    fit[i] = fit[j]
                    chroms[i] = chroms[j]
                    fit[j] = temp1
                    chroms[j] = temp2
        while not len(chroms) <= 2:
            chroms.pop()
            chroms.pop()
        l = []
        for i in range(2):
            if i % 2 == 0:
                l.append(chroms[1])
            elif i % 2 != 0:
                l.append(chroms[0])
            '''elif i == 3:
                l.append(chroms[-1])
            '''
        return l

    @staticmethod
    def cross_over(chroms):
        option = random.randint(1, 4)
        if option <= 2:
            rand_ind = random.randint(0, len(chroms[0]) - 1)
            for i in range(len(chroms[0])):
                if i >= rand_ind:
                    temp = chroms[0][i]
                    chroms[0][i] = chroms[1][i]
                    chroms[1][i] = temp
            '''rand_ind = random.randint(0, len(chroms[0])-1)
            for i in range(len(chroms[0])):
                if i >= rand_ind:
                    temp = chroms[2][i]
                    chroms[2][i] = chroms[3][i]
                    chroms[3][i] = temp
            '''
        elif option >= 2:
            range1 = random.randint(0, len(chroms[0]) - 1)
            range2 = random.randint(0, len(chroms[0]) - 1)
            if range1 > range2:
                temp = range1
                range1 = range2
                range2 = temp
            for i in range(len(chroms[0])):
                if range1 <= i <= range2:
                    temp = chroms[0][i]
                    chroms[0][i] = chroms[1][i]
                    chroms[1][i] = temp
            '''range1 = random.randint(0, len(chroms[0]) - 1)
            range2 = random.randint(0, len(chroms[0]) - 1)
            if range1 > range2:
                temp = range1
                range1 = range2
                range2 = temp
            for i in range(len(chroms[0])):
                if range1 <= i <= range2:
                    temp = chroms[2][i]
                    chroms[2][i] = chroms[3][i]
                    chroms[3][i] = temp
            '''
        return chroms

    @staticmethod
    def mutation(chroms):
        nxt = True
        ind_done = []
        for i in range(len(chroms)):
            if Genetic.dupli_check(chroms[i]):
                j = Genetic.return_dupli(chroms[i])
                chroms[i][j] = random.randint(1, len(chroms[i]))
                ind_done.append(i)
        if len(ind_done) == len(chroms):
            nxt = False
        if nxt:
            option = random.randint(0, 3)
            if option == 1:
                for i in range(len(chroms)):
                    if i in ind_done:
                        continue
                    randind = random.randint(0, len(chroms[i]) - 1)
                    for j in range(len(chroms[i])):
                        if j == randind:
                            chroms[i][j] = random.randint(1, len(chroms[i]))
            if option == 2:
                for i in range(len(chroms)):
                    if i in ind_done:
                        continue
                    randind = random.randint(0, len(chroms[i]) - 1)
                    for j in range(len(chroms[i])):
                        if j == randind:
                            chroms[i][j] = random.randint(1, len(chroms[i]))
                            if j + 1 <= len(chroms[i]) - 1:
                                chroms[i][j + 1] = random.randint(1, len(chroms[i]))
            if option == 3:
                for i in range(len(chroms)):
                    if i in ind_done:
                        continue
                    randind = random.randint(0, len(chroms[i]) - 1)
                    for j in range(len(chroms[i])):
                        if j == randind:
                            chroms[i][j] = random.randint(1, len(chroms[i]))
                            if j + 1 <= len(chroms[i]) - 1:
                                chroms[i][j + 1] = random.randint(1, len(chroms[i]))
                            if j + 2 <= len(chroms[i]) - 1:
                                chroms[i][j + 2] = random.randint(1, len(chroms[i]))
        return chroms

    @staticmethod
    def return_dupli(chrom, ind=0, setlist=None):
        if setlist is None:
            setlist = set()
        if chrom[ind] in setlist:
            return ind
        else:
            setlist.add(chrom[ind])
            ind = ind + 1
            return Genetic.return_dupli(chrom, ind, setlist)

    @staticmethod
    def dupli_check(chrom):
        if len(chrom) != len(set(chrom)):
            return True
        else:
            return False

    @staticmethod
    def max_fitness(n):
        return int((fact(n)) / ((fact(2)) * (fact(n - 2))))

    def fitness(self, chrom):
        return self.max_fitness(len(chrom)) - self.attack_count(chrom)

    @staticmethod
    def chessboard(chrom):
        print()
        board = np.zeros((len(chrom), len(chrom)), dtype=object)
        board[:] = 'x'
        for i in range(len(chrom)):
            board[len(chrom) - chrom[i]][i] = 'Q'
        print("Chessboard:\n")
        for i in range(len(chrom)):
            for j in range(len(chrom)):
                print(board[i][j], end=" ")
            print()
        print()
        print("(Q --> Queen)")

    def genetic(self, n):
        # initial population
        chroms = self.population(n)

        # calculating fitness
        fit = []
        for i in range(len(chroms)):
            fit.append(self.fitness(chroms[i]))

        # genetic process
        while True:
            if max(fit) == self.max_fitness(n):
                getind = fit.index(max(fit))
                break
            chroms = self.selection(chroms, fit)
            chroms = self.cross_over(chroms)
            chroms = self.mutation(chroms)
            for i in range(len(chroms)):
                fit[i] = self.fitness(chroms[i])
        return chroms[getind]


obj = Genetic()
num = int(input('Enter number of queens: '))
opt = obj.genetic(num)
print("Best chromosome:-", opt)
Genetic.chessboard(opt)
