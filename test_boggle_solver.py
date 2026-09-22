import unittest
import sys

sys.path.append("/home/codio/workspace/")  # PATH so unittest can find boggle_solver.py

from boggle_solver import Boggle


class BoggleTestBase(unittest.TestCase):
    """Shared helper so every test frame stays short and consistent."""

    def check(self, grid, dictionary, expected):
        mygame = Boggle(grid, dictionary)
        solution = sorted(w.upper() for w in mygame.getSolution())
        expected = sorted(w.upper() for w in expected)
        self.assertEqual(expected, solution)


class TestSuite_Alg_Scalability_Cases(BoggleTestBase):
    """Grid-size scalability: 3x3 up through 8x8, plus a large no-match dictionary."""

    def test_Normal_case_3x3(self):
        grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
        dictionary = ["abc", "abdhi", "abi", "ef", "cfi", "dea"]
        expected = ["abc", "abdhi", "cfi", "dea"]
        self.check(grid, dictionary, expected)

    def test_Normal_case_4x4(self):
        grid = [
            ["A", "B", "C", "D"],
            ["E", "F", "G", "H"],
            ["I", "J", "K", "L"],
            ["M", "N", "O", "P"],
        ]
        dictionary = ["abfg", "efjk", "abf", "xyz"]
        expected = ["abf", "abfg", "efjk"]
        self.check(grid, dictionary, expected)

    def test_Normal_case_5x5(self):
        grid = [
            ["A", "B", "C", "D", "E"],
            ["F", "G", "H", "I", "J"],
            ["K", "L", "M", "N", "O"],
            ["P", "Q", "R", "S", "T"],
            ["U", "V", "W", "X", "Y"],
        ]
        dictionary = ["abgh", "fklq", "abg", "zzz", "qrs"]
        expected = ["abg", "abgh", "fklq", "qrs"]
        self.check(grid, dictionary, expected)

    def test_Normal_case_8x8(self):
        grid = [[chr(65 + ((r * 8 + c) % 26)) for c in range(8)] for r in range(8)]
        # First row spells a straight horizontal chain; first column spells a
        # straight vertical chain -- both easy to verify by eye against the grid.
        dictionary = ["abcd", "aiq", "zzzzzzzz"]
        expected = ["abcd", "aiq"]
        self.check(grid, dictionary, expected)

    def test_Large_Dictionary_No_Matches(self):
        grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
        dictionary = ["zzz", "qqq", "xxx", "yyy", "www"]
        expected = []
        self.check(grid, dictionary, expected)


class TestSuite_Simple_Edge_Cases(BoggleTestBase):
    """Degenerate grids, structural rules, and input validation."""

    def test_SquareGrid_case_1x1(self):
        # All dictionary words are under 3 letters, so setDictionary filters
        # them all out, leaving an empty (but non-None) dictionary -> invalid.
        grid = [["A"]]
        dictionary = ["a", "b", "c"]
        expected = []
        self.check(grid, dictionary, expected)

    def test_EmptyGrid_case_0x0(self):
        # [[]] has one row, but that row is an empty list -> setGrid rejects it.
        grid = [[]]
        dictionary = ["hello", "there", "general", "kenobi"]
        expected = []
        self.check(grid, dictionary, expected)

    def test_Ragged_Grid_Is_Invalid(self):
        # Rows of different lengths fail setGrid's rectangular check.
        grid = [["A", "B", "C"], ["D", "E"]]
        dictionary = ["abc"]
        expected = []
        self.check(grid, dictionary, expected)

    def test_Grid_With_Non_String_Cell_Is_Invalid(self):
        grid = [["A", 5, "C"], ["D", "E", "F"], ["G", "H", "I"]]
        dictionary = ["abc"]
        expected = []
        self.check(grid, dictionary, expected)

    def test_Dictionary_Words_All_Too_Short_Filtered(self):
        grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
        dictionary = ["ab", "de", "gh"]
        expected = []
        self.check(grid, dictionary, expected)

    def test_Dictionary_Not_A_List_Is_Invalid(self):
        grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
        dictionary = "abc"  # a string, not a list
        expected = []
        self.check(grid, dictionary, expected)

    def test_Dictionary_With_Non_String_Entry_Invalidates_Whole_Dictionary(self):
        grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
        dictionary = ["cat", 5, "dog"]
        expected = []
        self.check(grid, dictionary, expected)

    def test_Grid_Not_A_List_Is_Invalid(self):
        grid = "ABC"
        dictionary = ["abc"]
        expected = []
        self.check(grid, dictionary, expected)

    def test_No_Words_In_Grid(self):
        grid = [["X", "Y", "Z"], ["Q", "W", "R"], ["T", "P", "L"]]
        dictionary = ["cat", "dog", "bird"]
        expected = []
        self.check(grid, dictionary, expected)

    def test_Duplicate_Letters_Immediate_Loop(self):
        # Two A's sit right next to each other; a solver must not treat
        # them as the same cell.
        grid = [["A", "A", "B"], ["C", "D", "E"], ["F", "G", "H"]]
        dictionary = ["aa", "aab"]
        expected = ["aab"]
        self.check(grid, dictionary, expected)

    def test_Duplicate_Letters_Later_Loop(self):
        # Same letter reappears, but only one instance is actually adjacent
        # to the path that needs it.
        grid = [["A", "B", "A"], ["C", "D", "E"], ["F", "G", "H"]]
        dictionary = ["aba", "aca"]
        expected = ["aba"]
        self.check(grid, dictionary, expected)

    def test_Words_Cant_Reuse_A_Cell(self):
        grid = [["A", "B"], ["C", "D"]]
        dictionary = ["abcabd", "abcd"]  # abcabd would require revisiting A and B
        expected = ["abcd"]
        self.check(grid, dictionary, expected)

    def test_Word_That_Takes_The_Entire_Grid(self):
        grid = [["A", "B"], ["D", "C"]]
        dictionary = ["abcd"]
        expected = ["abcd"]
        self.check(grid, dictionary, expected)

    def test_Single_Row_Grid(self):
        grid = [["A", "B", "C", "D"]]
        dictionary = ["abc", "abcd", "bcd", "dcba"]
        expected = ["abc", "abcd", "bcd", "dcba"]
        self.check(grid, dictionary, expected)

    def test_Single_Column_Grid(self):
        grid = [["A"], ["B"], ["C"], ["D"]]
        dictionary = ["abc", "abcd", "bcd"]
        expected = ["abc", "abcd", "bcd"]
        self.check(grid, dictionary, expected)


class TestSuite_Complete_Coverage(BoggleTestBase):
    """Directional coverage, path complexity, and multi-word results."""

    def test_All_Directions_From_Center_Cell(self):
        # Center cell has all 8 neighbors reachable; only a real 3+ letter
        # word should surface, not the raw 2-letter neighbor pairs.
        grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
        dictionary = ["ea", "eb", "ec", "ed", "ef", "eg", "eh", "ei", "dea"]
        expected = ["dea"]
        self.check(grid, dictionary, expected)

    def test_Winding_Path_Spiral(self):
        grid = [["A", "B", "C"], ["H", "I", "D"], ["G", "F", "E"]]
        dictionary = ["abcdefghi", "abc"]
        expected = ["abc", "abcdefghi"]
        self.check(grid, dictionary, expected)

    def test_Multiple_Words_Sharing_Letters(self):
        grid = [["C", "A", "T"], ["O", "R", "S"], ["G", "E", "D"]]
        dictionary = ["cat", "car", "cot", "art", "rat", "zzz"]
        expected = ["art", "car", "cat", "rat"]
        self.check(grid, dictionary, expected)

    def test_Case_Insensitivity(self):
        grid = [["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"]]
        dictionary = ["ABC", "AbDhI"]
        expected = ["abc", "abdhi"]
        self.check(grid, dictionary, expected)

    def test_Pathologically_Slow_Repeated_Letter_Grid(self):
        # 6x6 grid of a single repeated letter stresses the backtracking search.
        grid = [["A"] * 6 for _ in range(6)]
        dictionary = ["aaa", "aaaa", "aaaaa", "zzz"]
        expected = ["aaa", "aaaa", "aaaaa"]
        self.check(grid, dictionary, expected)

    def test_Returns_All_Matching_Words(self):
        grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
        dictionary = ["abc", "abdhi", "cfi", "dea", "bad", "zzz"]
        expected = ["abc", "abdhi", "bad", "cfi", "dea"]
        self.check(grid, dictionary, expected)


class TestSuite_Qu_and_St(BoggleTestBase):
    """'Qu' / 'St' combined-tile rules: each tile's letters are consumed
    as a single atomic unit -- a path can't stop partway through one."""

    def test_Simple_Qu_Case(self):
        grid = [["Qu", "E", "S"], ["X", "Y", "T"]]
        dictionary = ["quest"]
        expected = ["quest"]
        self.check(grid, dictionary, expected)

    def test_Simple_St_Case(self):
        grid = [["St", "A", "R"], ["B", "C", "D"], ["E", "F", "G"]]
        dictionary = ["star"]
        expected = ["star"]
        self.check(grid, dictionary, expected)

    def test_Qu_And_St_Combine_In_One_Word(self):
        # "quest" formed from just two tiles: Qu -> E -> St
        grid = [["Qu", "E"], ["X", "St"]]
        dictionary = ["quest"]
        expected = ["quest"]
        self.check(grid, dictionary, expected)

    def test_Start_Word_Using_St_Tile_Chain(self):
        grid = [["St", "A"], ["T", "R"]]
        dictionary = ["start"]
        expected = ["start"]
        self.check(grid, dictionary, expected)

    def test_Qu_Tile_Counts_As_Two_Chars_For_Min_Length(self):
        # "Qu" + one more tile is enough to reach the 3-letter minimum.
        grid = [["A", "Qu", "B"]]
        dictionary = ["aqu", "aqub"]
        expected = ["aqu", "aqub"]
        self.check(grid, dictionary, expected)

    def test_Multichar_Tile_Must_Be_Consumed_Atomically(self):
        # "St" tile can't stop after just the 's' -- so "abs" (which would end
        # mid-tile) is never found, even though it's a valid dictionary word
        # and even though "abst" (using the whole tile) is found.
        grid = [["A", "B", "St"]]
        dictionary = ["abst", "abs"]
        expected = ["abst"]
        self.check(grid, dictionary, expected)

    def test_Bare_Q_Tile_Can_End_A_Word(self):
        # A lone "Q" tile (not combined with "u") behaves like any other
        # single-letter tile -- nothing in the code stops a word ending on it.
        grid = [["A", "B", "Q"]]
        dictionary = ["abq"]
        expected = ["abq"]
        self.check(grid, dictionary, expected)

    def test_Separate_Q_And_U_Tiles_Form_Word(self):
        # Q and U as two distinct single-letter cells (not a combined "Qu"
        # tile) still chain together normally.
        grid = [["A", "Q", "U"], ["D", "E", "F"], ["G", "H", "I"]]
        dictionary = ["aqu", "aq", "qu"]  # "aq"/"qu" filtered out (too short)
        expected = ["aqu"]
        self.check(grid, dictionary, expected)


if __name__ == "__main__":
    unittest.main()