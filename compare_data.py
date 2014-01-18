#/usr/bin/python
"""Python stand alone script to compare data entered by two different people"""

import savReaderWriter as spss
import argparse
import sys

__author__ = "mt@trustdarkness.com (Mike Thompson)"

#CONSTANTS used throughout the program
TITLE = "SPSS Compare Data"
DEFAULT_MODE = "gui"
try:
  import easygui as eg
except ImportError:
  print "python-easygui required for graphical mode, running in console mode"
  DEFAULT_MODE = "console"

def column_run(record_list, test):
  """Takes a record list and a column number and returns two separate lists, 
  one for each coder, with the data run for the given column.

  Args:
    record_list: a list of lists, where each list in the parent list is one
      spss "record" or basically a line in the spss file.
    test:  a column number to test (TODO: rename this?)

  Returns:
    tuple like (records_per_coder (int), coder1 (list), coder2 (list))
  """
  records_per_coder = len(record_list)/2
  #current_record = record_list[0][0]
  #print "Current record: %s" % current_record
  # we assume there will only ever be 2 coders
  coder1 = []
  coder2 = []
  for i in range(0, records_per_coder):
    coder1.append(665)
    coder2.append(665)

  for record in record_list:
    index = int(record[0]) - 1
    # print "Processing record %d" % index
    if coder1[index] == 665:
      #print "record %d coder 2 = %d" % (index, record[test])
      if record[test]:
        coder1[index] = record[test]
      else:
        coder1[index] = 666
    else:
      #print "record %d coder 1 = %d" % (index, record[test])
      if record[test]:
        coder2[index] = record[test]
      else: 
        coder2[index] = 666
 
  return (records_per_coder, coder1, coder2)

def main():
  """
  Our main method, parses command line arguments and runs based on the user's
  input
  """
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument("-g", "--gui", action="store_true", default=None,
    help="Run in Graphical Mode (if supported)", dest="gui")
  parser.add_argument("-t", "--test", action="store_true", default=None,
    help="Run in Text Mode", dest="text")

  args = parser.parse_args()
  if args.gui:
    gui()
  elif args.text:
    cui()
  else: 
    if DEFAULT_MODE == 'gui':
      gui()
    else: 
      cui()

def gui():
  """Method to run the code in gui mode"""
  filename = eg.fileopenbox(msg="Please choose an spss .sav file", title=TITLE)
  test = int(eg.enterbox(msg ="\n".join([
    "I'm assuming column 0 is an ID that corresponds to a casefile", 
    "such that there will be two records each with that ID, one for ",
    "each data coder.",
    "",
    "Please enter another column number, starting with 0, to score:"
  ]), title=TITLE))
  record_list = []
  # first we'll read in every record and add them all to the list
  with spss.SavReader(filename) as f:
    #header = next(f)
    for line in f:
      record_list.append(line)
  tf = eg.boolbox(msg="\n".join([
    "I found %d records.  If that's not what you" % len(record_list), 
    "expected, please try again or contact the developer",
    "Continue?"]), title=TITLE, choices=("Yes", "No"))
  if not tf:
    sys.exit(0)
  records_per_coder, coder1, coder2 = column_run(record_list, test)
  #text = ["The data looks like: ", "#  Coder 1:  Coder 2: "]
  text = []
  agreement = 0
  for i in range(records_per_coder):
    #text.append("%s   %s          %s " % (i, coder1[i], coder2[i]))
    if coder1[i] == coder2[i]:
      agreement += 1 
  text.append("")
  text.append("Would you like to add another column?")
  tf = eg.boolbox(msg="\n".join(text), title=TITLE, choices=("Yes", "No"))
  while tf:
    column_num = int(eg.enterbox(msg="Please enter a column number: ", 
      title=TITLE))
    records_per_coder, new_coder1, new_coder2 = \
      column_run(record_list, column_num)
    coder1.extend(new_coder1)
    coder2.extend(new_coder2)
    tf = eg.boolbox(msg="Would you like to add another column?",
      title=TITLE, choices=("Yes", "No"))
  #text = ["The data looks like: ", "#  Coder 1:  Coder 2: "]
  text = []
  agreement = 0
  for i in range(len(coder1)):
    #text.append("%s   %s          %s " % (i, coder1[i], coder2[i]))
    if coder1[i] == coder2[i]:
      agreement += 1 
  text.append("")
  percent_agreement = (float(agreement)/float(len(coder1)))*100
  text.append("There was %f %% agreement between the two coders" % \
    percent_agreement)
  text.append("Thanks for playing!")
  eg.boolbox(msg="\n".join(text), title=TITLE, choices=("Exit", "Exit"))
  sys.exit(0)


def cui(): 
  """Run to program in text mode"""
  filename = raw_input("Please enter a filename: ")
  print "--"
  print "I'm assuming column 0 is an ID that corresponds to a casefile"
  print "such that there will be two records each with that ID, one for "
  print "each data coder."
  test = int(raw_input("Please give me a column number to score: "))
  record_list = []
  # first we'll read in every record and add them all to the list
  with spss.SavReader(filename) as f:
    #header = next(f)
    for line in f:
      record_list.append(line)

  print "I found %d records.  If that's not what you" % len(record_list)
  print "expected, please try again or contact the developer"
  yn = raw_input("Continue? (Y/n): ")
  if yn.upper() == "N":
    sys.exit(0)

  records_per_coder, coder1, coder2 = column_run(record_list, test)
  print "The data looks like: "
  print "#  Coder 1:  Coder 2: "
  agreement = 0
  for i in range(records_per_coder):
    print "%s   %s       %s " % (i, coder1[i], coder2[i])
    if coder1[i] == coder2[i]:
      agreement += 1

  yn = raw_input("Would you like to add another column? (y/N) ")
  while (yn.lower() == "y"):
    column_num = int(raw_input("Please enter a column number: "))
    records_per_coder, new_coder1, new_coder2 = \
      column_run(record_list, column_num)
    coder1.extend(new_coder1)
    coder2.extend(new_coder2)
    yn = raw_input("Would you like to add another column? (y/N) ")
  print "The data looks like: "
  print "#  Coder 1:  Coder 2: "
  agreement = 0
  for i in range(len(coder1)):
    print "%s   %s       %s " % (i, coder1[i], coder2[i])
    if coder1[i] == coder2[i]:
      agreement += 1

  percent_agreement = (float(agreement)/float(len(coder1)))*100
  print " "
  print "There was %f %% agreement between the two coders" % percent_agreement
  print "Thanks for playing!"

if __name__ == "__main__":
  main()
