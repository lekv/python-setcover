#!/usr/bin/env python
'''
File: cover.py
Author: Lars Volker <lv@lekv.de>
Description: This is an implementation of SETCOVER in python, hacked together
for a friend's PhD thesis. It computes the complete list of solutions for the
  given input set of subsets.
Copyright: 2012 Lars Volker
License: Lars Volker <lv@lekv.de> wrote this file. As long as you retain this
notice you can do whatever you want with this stuff. If we meet some day, and
you think this stuff is worth it, you can buy me a beer in return.
'''

import logging, sys
from itertools import combinations

#from profilehooks import coverage, profile

# Setup logging
#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

class Solver(object):
  """Main Solver class.
  
  To use it, pass a list of lists to the class during creation. If you omit
  the list, an internal test fixture will be used. Then call solve() to run
  the solver. Afterwards, the results can be obtained with getSolutions() and
  can be printed to the console with printSolutions()."""

  def __init__(self, subsets = None):
    """Initalize the class.

    Keyword arguments:
    subsets -- the list of subsets from which to compute the SETCOVER
    solutions."""
    # TODO: parse subsets from lists
    self.subsets = subsets

    # Development fixture
    if not self.subsets:
      self.subsets = [ [1, 2],
                       [2, 3],
                       [1, 3],
                        ]
    # All elements
    self.superset = set()
    for s in self.subsets:
      self.superset = self.superset.union(s)

    # List of all solutions
    self.solutions = []

    # Best bound so far. Combining all subsets yields a trivial bound.
    self.bound = len(self.subsets)

  #@profile
  def isSolution(self, indices):
    """Check, if the subsets indicated by indices form a solution."""
    # TODO: To speed things up, we could copy self.superset and then remove
    # subsets from it, until it is empty
    # Initialize an empty set
    merged = set()
    subsets = ((self.subsets[i] for i in indices))
    # Add all subsets to the temporary set
    for s in subsets:
      merged = merged.union(s)
    # Compare the temporary set with the target
    return merged == self.superset


  def solve(self):
    """Main solving routine.
    
    First it scans combinations for the currently lowest bound and breaks on
    the first found solution and decreases the bound. This is done until the
    final solution length is discovered. In an exhaustive search, it then
    finds all solutions of the final length."""

    # Indicates the end of the exploration phase, when no solution for the
    # current bound could be found
    endOfSearch = False
    while not endOfSearch:
      logging.debug("checking bound: %s" % self.bound)
      for indices in combinations(range(len(self.subsets)), self.bound):
        # Temptatively set endOfSearch. It will get unset if a solution is
        # found
        endOfSearch = True
        # Check, if we found a solution
        if self.isSolution(indices):
          # We found a solution this time, so we will have to check for one
          # lower round
          endOfSearch = False
          self.bound = len(indices)
          logging.debug("found solution %s, decreasing bound" % repr(indices))
          self.bound -= 1
          break;
    # Update bound, as it now contains the smallest count, where no solution
    # was found
    self.bound += 1
    logging.info("Computed length of shortest solution: %s" % self.bound)

    # Now perform an exhaustive search for solutions of length self.bound
    for indices in combinations(range(len(self.subsets)), self.bound):
      # Check, if we found a solution
      if self.isSolution(indices):
        # add the solution
        logging.debug("Found solution: %s" % repr(indices))
        self.solutions.append(indices)

  def getSolutions(self):
    """Return a list with all solutions that were found."""
    return self.solutions

  def printSolutions(self):
    """Print all solutions found."""
    print("Solutions:")
    for s in self.getSolutions():
      # Build output string
      out = ""
      for i in s:
        out += str(i+1) + " "
      print(out)

def checkOldFile(path):
  """Check, whether an old file format could have been specified.
  
  Ealier versions used to specify the number of vertices and the number of
  subsets on the first two lines of the file. Therefore we issue a warning,
  if the first two lines contain only one integer each."""
  with file(path) as f:
    # Check first two lines
    for i in range(2):
      # Get number of values
      if len(f.readline().split()) == 1:
        return True
  return False

def main():
  """Method to run the solver as a CLI tool."""
  # Check for required arguments and exit with usage information
  if len(sys.argv) < 2:
    print("Usage: %s INPUTFILE" % sys.argv[0])
    sys.exit(1)
  # Get path of the input file
  path = sys.argv[1]

  # If the user specifies an old format file, it will be automatically
  # detected. However, the user has the chance to force a new format file
  # behaviour.
  oldFile = checkOldFile(path)

  # Parse --new-file option
  forceNewFile = False
  if len(sys.argv) > 2:
    forceNewFile = sys.argv[2] == "--new-file"

  # Issue a warning if the user does not decide to override.
  if oldFile and not forceNewFile:
    logging.warn("Old file format detected. Please check the input file. If\
        you want single vertex subsets on the first two lines, then run\
        with --new-file.")

  # The parsed subsets
  subsets = []

  # Load subsets from the specified file
  logging.info("loading file %s" % path)
  with file(path) as f:
    if oldFile and not forceNewFile:
      # Old files contain two header lines
      logging.info("Removing header lines from old format file.")
      maxID = f.readline().strip()
      noSets = f.readline().strip()
    for line in f.readlines():
      subsets.append(map(int, line.split()))

  # Initialize a Solver with the subsets loaded from the input file
  solver = Solver(subsets)
  # Run the solver
  solver.solve()
  # Output the results
  solver.printSolutions()

if __name__ == '__main__':
  main()

# vim: textwidth=80 shiftwidth=2 expandtab autoindent tabstop=2
