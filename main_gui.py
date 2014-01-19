#Boa:Frame:compare_data_gui_main

import wx
import wx.lib.stattext
import savReaderWriter as spss

def create(parent):
    return compare_data_gui_main(parent)

[wxID_COMPARE_DATA_GUI_MAIN, wxID_COMPARE_DATA_GUI_MAINBUTTON1, 
 wxID_COMPARE_DATA_GUI_MAINCOLUMNS, wxID_COMPARE_DATA_GUI_MAINFILENAME, 
 wxID_COMPARE_DATA_GUI_MAINGENSTATICTEXT1, 
 wxID_COMPARE_DATA_GUI_MAINGENSTATICTEXT2, 
 wxID_COMPARE_DATA_GUI_MAINSTATICTEXT1, wxID_COMPARE_DATA_GUI_MAINSTATICTEXT2, 
 wxID_COMPARE_DATA_GUI_MAINSTATICTEXT3, wxID_COMPARE_DATA_GUI_MAINWELCOME, 
] = [wx.NewId() for _init_ctrls in range(10)]

class compare_data_gui_main(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_COMPARE_DATA_GUI_MAIN,
              name=u'compare_data_gui_main', parent=prnt, pos=wx.Point(306, 27),
              size=wx.Size(1019, 559), style=wx.DEFAULT_FRAME_STYLE,
              title=u'Compare SPSS Data')
        self.SetClientSize(wx.Size(1019, 559))

        self.Welcome = wx.StaticText(id=wxID_COMPARE_DATA_GUI_MAINWELCOME,
              label=u'Welcome to Compare Data!  We will compare data entered by two different "coders" that we hope is the same, but may have disagreements.',
              name=u'Welcome', parent=self, pos=wx.Point(16, 8),
              size=wx.Size(793, 64), style=0)
        self.Welcome.SetToolTipString(u'staticText1')

        self.staticText1 = wx.StaticText(id=wxID_COMPARE_DATA_GUI_MAINSTATICTEXT1,
              label=u'We assume that column zero is an ID field that will be the same for both coders, but different for every record.',
              name='staticText1', parent=self, pos=wx.Point(16, 64),
              size=wx.Size(718, 17), style=0)

        self.columns = wx.TextCtrl(id=wxID_COMPARE_DATA_GUI_MAINCOLUMNS,
              name=u'columns', parent=self, pos=wx.Point(16, 208),
              size=wx.Size(136, 32), style=0, value=u'')

        self.staticText2 = wx.StaticText(id=wxID_COMPARE_DATA_GUI_MAINSTATICTEXT2,
              label=u'Please enter a comma separated list of columns to check for agreement',
              name='staticText2', parent=self, pos=wx.Point(16, 184),
              size=wx.Size(472, 17), style=0)

        self.staticText3 = wx.StaticText(id=wxID_COMPARE_DATA_GUI_MAINSTATICTEXT3,
              label=u"Please enter the filename of an spss file to check.  This should be in the same path as the application you're running or should be given with the full path.",
              name='staticText3', parent=self, pos=wx.Point(16, 88),
              size=wx.Size(784, 72), style=0)

        self.filename = wx.TextCtrl(id=wxID_COMPARE_DATA_GUI_MAINFILENAME,
              name=u'filename', parent=self, pos=wx.Point(16, 128),
              size=wx.Size(272, 27), style=0, value=u'')

        self.button1 = wx.Button(id=wxID_COMPARE_DATA_GUI_MAINBUTTON1,
              label=u'Evaluate it, Yo!', name='button1', parent=self,
              pos=wx.Point(848, 512), size=wx.Size(160, 40), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_COMPARE_DATA_GUI_MAINBUTTON1)

        self.genStaticText1 = wx.lib.stattext.GenStaticText(ID=wxID_COMPARE_DATA_GUI_MAINGENSTATICTEXT1,
              label=u'', name='genStaticText1', parent=self, pos=wx.Point(712,
              352), size=wx.Size(200, 120), style=0)
        self.genStaticText1.SetFont(wx.Font(76, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Sans'))

        self.genStaticText2 = wx.lib.stattext.GenStaticText(ID=wxID_COMPARE_DATA_GUI_MAINGENSTATICTEXT2,
              label=u'', name='genStaticText2', parent=self, pos=wx.Point(808,
              464), size=wx.Size(200, 23), style=0)
        self.genStaticText2.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Sans'))

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnButton1Button(self, event):
        filename = self.filename.Value
        columns = self.columns.Value.split(',')
        agreement = evaluate(filename, columns)
        self.genStaticText1.SetLabel("%.2f" % agreement)
        self.genStaticText2.SetLabel("Percent Agreement")
        event.Skip()


   

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

def evaluate(filename, columns):
    record_list = []
    with spss.SavReader(filename) as f:
        #header = next(f)
        for line in f:
            record_list.append(line)
    coder1 = []
    coder2 = []
    for column_num in columns:
        records_per_coder, new_coder1, new_coder2 = \
            column_run(record_list, int(column_num))
        coder1.extend(new_coder1)
        coder2.extend(new_coder2)
        
    agreement = 0
    for i in range(len(coder1)):
        #text.append("%s   %s          %s " % (i, coder1[i], coder2[i]))
        if coder1[i] == coder2[i]:
            agreement += 1
        
    percent_agreement = (float(agreement)/float(len(coder1)))*100
    return percent_agreement
