class Boggle:
    def __init__(self, grid, dictionary):
        self.grid = None
        self.dictionary = None
        self.solution = []
        self._rows = 0
        self._cols = 0
        self._trie = None
        self.setGrid(grid)
        self.setDictionary(dictionary)
 
    def setGrid(self, grid):
        """
        Method that validates and stores the grid.
        These are the requirements:
          - grid is a non-empty list
          - every row is a non-empty list
          - every row has the same length
          - every cell is a non-empty string
        On failure, self.grid is set to None.
        """
        # Rejects anything that isnt a non empty list
        if not isinstance(grid, list) or len(grid) == 0:
            self.grid = None
            self._rows = 0
            self._cols = 0
            return
 
        row_len = None
        for row in grid:
          # Each row must be a non empty list
            if not isinstance(row, list) or len(row) == 0:
                self.grid = None
                self._rows = 0
                self._cols = 0
                return
            if row_len is None:
                row_len = len(row) # first row sets the expected width
            elif len(row) != row_len:
              # every row after the first much match that width, else its not rectangular
                self.grid = None
                self._rows = 0
                self._cols = 0
                return
            for cell in row:
              # every tile must be a real non empty string
                if not isinstance(cell, str) or len(cell) == 0:
                    self.grid = None
                    self._rows = 0
                    self._cols = 0
                    return
 
        # grid passes all checks and is stored
        self.grid = grid
        self._rows = len(grid)
        self._cols = row_len
 
    def setDictionary(self, dictionary):
        """
        Method that validates and stores the dictionary.
        Requirements:
          - dictionary is a non-empty list
          - every entry is a non-empty string
        Words are set to lowercase and words shorter than 3
        letters are dropped because they can never be valid words.
        On failure, self.dictionary is set to None.
        """
        # reject anything that isnt a non empty list
        if not isinstance(dictionary, list) or len(dictionary) == 0:
            self.dictionary = None
            return
 
        normalized = []
        for word in dictionary:
          # every word must be a real non empty string
            if not isinstance(word, str) or len(word) == 0:
                self.dictionary = None
                return
            lowered = word.lower() # make words lowercase so grid is case insensitive
            if len(lowered) >= 3:
              # dont count words shorter than 3 letters
                normalized.append(lowered)
 
        self.dictionary = normalized
 
    
    def _buildTrie(self):
        """
        Builds a nested-dict trie from self.dictionary for fast prefix
        pruning during the search. '$' marks the end of a valid word.
        """
        trie = {}
        for word in self.dictionary:
            node = trie
            for ch in word:
                if ch not in node:
                    node[ch] = {} # create a branch for this letter if it doesnt exist yet
                node = node[ch]
            node['$'] = True # mark node, signifying end of a complete word
        return trie
 
    def _isValid(self):
        return self.grid is not None and self.dictionary is not None and len(self.dictionary) > 0
 
    def _neighbors(self, r, c):
      # Yeilds all surrounding cells but skips any off grid
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self._rows and 0 <= nc < self._cols:
                    yield nr, nc
 
    def _dfs(self, r, c, node, visited, current_word, found):
        tile = self.grid[r][c].lower()
        # Walk the trie one character at a time for this tile's letters.
        # If at any point there's no matching branch, this path can
        # never lead to a dictionary word, so prune immediately.
        cursor = node
        for ch in tile:
            if ch not in cursor:
                return
            cursor = cursor[ch]
 
        new_word = current_word + tile
        visited.add((r, c))
 
        if '$' in cursor and len(new_word) >= 3:
            found.add(new_word)
 
        for nr, nc in self._neighbors(r, c):
            if (nr, nc) not in visited:
                self._dfs(nr, nc, cursor, visited, new_word, found)
 
        visited.remove((r, c))
 
    def getSolution(self):
        """
        Returns a list of found words, or an empty list if no words
        were found or the grid/dictionary are invalid.
        """
        self.solution = []
 
        if not self._isValid():
            return self.solution
 
        self._trie = self._buildTrie()
        found = set()
        visited = set()
 
        for r in range(self._rows):
            for c in range(self._cols):
                self._dfs(r, c, self._trie, visited, "", found)
 
        self.solution = sorted(found)
        return self.solution


def main():
    grid = [["T", "W", "Y", "R"], ["E", "N", "P", "H"], ["G", "Z", "Qu", "R"], ["O", "N", "T", "A"]]
    dictionary = ["art", "ego", "gent", "get", "net", "new", "newt", "prat", "pry", "qua", "quart", "quartz", "rat", "tar", "tarp", "ten", "went", "wet", "arty", "rhr", "not", "quar"]
    mygame = Boggle(grid, dictionary)
    print(mygame.getSolution())


if __name__ == "__main__":
    main()
