#/usr/bin/python
import savReaderWriter as spss

def main():
  filename = raw_input("Please enter a filename: ")
  print "--"
  print "I'm assuming column 0 is a unique ID that corresponds to a casefile"
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
  if yn.upper == "N":
    sys.exit(0)
  records_per_coder = len(record_list)/2
  current_record = record_list[0][0]
  print "Current record: %s" % current_record
  print "There will be %d records per coder" % records_per_coder
  # we assume there will only ever be 2 coders
  coder1 = []
  coder2 = []
  for i in range(records_per_coder):
    coder1.append(None)
    coder2.append(None)

  for record in record_list:
    index = int(record[0]) - 1
    # print "Processing record %d" % index
    if coder1[index] == None:
      # print "record %d coder 2 = %d" % (index, record[test])
      coder1[index] = record[test]
    else:
      # print "record %d coder 1 = %d" % (index, record[test])
      coder2[index] = record[test]

  print "The data looks like: "
  print "#  Coder 1:  Coder 2: "
  agreement = 0
  for i in range(records_per_coder):
    print "%d   %d       %d " % (i, coder1[i], coder2[i])
    if coder1[i] == coder2[i]:
      agreement += 1

  percent_agreement = float(agreement)/float(records_per_coder)
  print " "
  print "There was %f agreement between the two coders" % percent_agreement
  print "Thanks for playing!"

if __name__ == "__main__":
  main()
