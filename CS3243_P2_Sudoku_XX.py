import sys
import copy
from Queue import Queue

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

### Class containing csp model i.e. variables, domains, edges btw variables, backupForReassignment
class Csp(object):
    def __init__(self, puzzle):
        self.varList = list()
        self.domain = dict()
        self.neighbours = dict()
        self.restore = dict()
        self.initialise(self.transformTo1D(puzzle), puzzle)

    def transformTo1D(self, puzzle):
        output = []
        for i in puzzle:
            for j in i:
                output.append(j)
        return output

    def initialise(self, puzzle1, puzzle2):
        #Init var to PAIR of coordinates from puzzle, varList[index]=var
        for i in range(9):
            for j in range(9):
                self.varList.append( (i, j) )
        #Init domains for each var, var:list()
        self.domain = {v: list(range(1,10)) if puzzle1[i] == 0 else [puzzle1[i]] for \
                       i, v in enumerate(self.varList)}
        
        #form neighbour dict for each var
        for var in self.varList:
            self.neighbours[var] = list()
            for i in range(len(puzzle2)):
                #Check same row
                if (var[0], i) != var:
                    self.neighbours[var].append( (var[0], i) )
                #Check same col
                if (i, var[1]) != var:
                    self.neighbours[var].append( (i, var[1]) )
            #Check same box
            boxRow = (var[0] // 3) * 3
            boxCol = (var[1] // 3) * 3
            for i in range(boxRow, boxRow+3):
                for j in range(boxCol, boxCol+3):
                    if (i, j) != var and (i, j) not in self.neighbours[var]:
                        self.neighbours[var].append( (i, j) )
        #Init restore for each var, var:list()
        self.restore = {v: list() if puzzle1[i] == 0 else [puzzle1[i]] for \
                       i, v in enumerate(self.varList)}

    def isSolved(self):
        for var in self.varList:
            if len(self.domain[var]) > 1:
                return False
        return True

    def unassign(self, var, assignment):
        if var in assignment:
            for (k, value) in self.restore(var):
                self.domain[k].append(value)
            self.restore[var] = []
            del assignment[var]

### Class containing Sudoku solving methods: AC3 and Backtrack
class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

    def runAC3(self, csp):
        qu = self.getConstraints(csp)
        print 'len', qu.qsize()
        count = 0
        while True:
            if qu.empty():
                #print 'lenQ', qu.qsize(), 'count', count
                print 'counter', count
                break
            count += 1
            xI, xJ = qu.get()
            if self.revise(csp, xI, xJ):
                #print 'lenQ', qu.qsize(), 'count', count
                if len(csp.domain[xI]) == 0:
                    print 'xI is ZERO', xI
                    return False
                for xK in csp.neighbours[xI]:
                    #print 'xI', xI
                    #print 'xK', xK
                    if xK != xI:
                        #print 'putting', xK, xI
                        qu.put( (xK, xI) )
        return True

    def revise(self, csp, xI, xJ):
        revised = False
        for i in csp.domain[xI]:
            removeFlag = True
            for j in csp.domain[xJ]:
                if j != i:
                    removeFlag = False
            if removeFlag:
                csp.domain[xI].remove(i)
                print 'd removed', i
                print xI, 'left with', csp.domain[xI]
                revised = True
        return revised

    def getConstraints(self, csp):
        qu = Queue() #Contains a pair of pairs xD
        for cell in csp.neighbours:
            #print 'cell', cell
            #print 'nCell', csp.neighbours[cell], '\nlen', len(csp.neighbours[cell])
            for nCell in csp.neighbours[cell]:
                qu.put( (cell, nCell) )
                #print cell, nCell
        return qu

    def backtrackSearch(self):
        pass

    def getOutput(self, csp):
        for var in csp.domain:
            self.ans[var[0]][var[1]] = csp.domain[var][0]
    
    def solve(self):
        # TODO: Write your code here

        newPuzzle = Csp(self.puzzle)
        pP(self.puzzle)
        print 'Trying AC3'
        if self.runAC3(newPuzzle):
            if newPuzzle.isSolved():
                #TODO ASSIGN
                self.getOutput(newPuzzle)
                print 'AC3 SUCCESS'
                pP(self.ans)
            else:
                print 'Starting backtrack'
                #RUN BACKTRACKING
                assignment = {}
                isAssigned = self.backtrackSearch()
                if isAssigned:
                    #TODO ASSIGN
                    pass
                else:
                    #NO solution, returning original sudoku
                    pass
        # self.ans is a list of lists
        return self.ans

def pP(puzzle):
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            print puzzle[i][j],
        print ""
    

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")