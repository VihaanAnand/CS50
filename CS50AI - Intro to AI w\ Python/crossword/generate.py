import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for i in self.crossword.variables:
            length = i.length
            for j in self.domains[i].copy():
                if len(j) != length:
                    self.domains[i].remove(j)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlaps = self.crossword.overlaps[x, y]
        if overlaps == None:
            return False
        changed = False
        for i in self.domains[x].copy():
            wordviable = False
            try:
                letter = i[overlaps[0]]
            except:
                continue
            for j in self.domains[y]:
                try:
                    otherletter = j[overlaps[1]]
                except:
                    continue
                if letter == otherletter:
                    wordviable = True
                    break
            if wordviable == False:
                self.domains[x].remove(i)
                changed = True
        return changed

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            arcs = list(self.crossword.overlaps.keys())
        while len(arcs) > 0:
            current = arcs[0]
            arcs = arcs[1:]
            revised = self.revise(current[0], current[1])
            if revised:
                overlaps = list(self.crossword.overlaps.keys())
                for i in overlaps:
                    if i[0] in current or i[1] in current:
                        arcs.append(i)
        for i in self.domains:
            if len(self.domains[i]) == 0:
                return False
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for i in list(self.domains.keys()):
            if i not in assignment or assignment[i] == None:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for i in assignment.keys():
            val = assignment[i]
            if len(val) != i.length:
                return False
        intersections = self.crossword.overlaps
        for i in intersections:
            try:
                val = assignment[i[0]]
                val2 = assignment[i[1]]
                cells = intersections[i]
                if val[cells[0]] != val2[cells[1]]:
                    return False
            except:
                a = 0
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        domain_test = {}
        for val in self.domains[var]:
            domain_test[val] = 0
        neighbours = self.crossword.neighbors(var)
        for val in self.domains[var]:
            for var2 in neighbours:
                for val2 in self.domains[var2]:
                    try:
                        if self.crossword.overlaps[val, val2]:
                            x, y = self.crossword.overlaps[val, val2]
                            if val[x] != val2[y]:
                                domain_test[val] += 1
                    except:
                        a = 0
        # WHAT THE 41 IS WRONG WITH THIS FUNCTION
        sorted_values = sorted(domain_test, key=domain_test.get, reverse=True)
        return sorted_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        if self.assignment_complete(assignment):
            return None
        assignment_test = {}
        degree_test = {}
        for var in self.domains:
            try:
                if not assignment[var] or assignment[var] == None:
                    assignment_test[var] = len(self.domains[var])
                    degree_test[var] = -1 * len(self.crossword.neighbors(var))
            except:
                assignment_test[var] = len(self.domains[var])
                degree_test[var] = -1 * len(self.crossword.neighbors(var))
        sorted_variables = sorted(assignment_test, key=lambda x: (
            assignment_test[x], degree_test[x]))
        return sorted_variables[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        copy = assignment.copy()
        if self.assignment_complete(assignment):
            return assignment
        variable = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(variable, assignment):
            assignment[variable] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result != None:
                    return result
                assignment[variable] = copy[variable]
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
