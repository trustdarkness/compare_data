#Boa:Frame:compare_data_gui_main

import wx
import wx.lib.filebrowsebutton
import wx.lib.stattext
import savReaderWriter as spss

def create(parent):
    return compare_data_gui_main(parent)

[wxID_COMPARE_DATA_GUI_MAIN, wxID_COMPARE_DATA_GUI_MAINBUTTON1, 
 wxID_COMPARE_DATA_GUI_MAINCOLUMNS, wxID_COMPARE_DATA_GUI_MAINGENSTATICTEXT1, 
 wxID_COMPARE_DATA_GUI_MAINGENSTATICTEXT2, wxID_COMPARE_DATA_GUI_MAINPATH, 
 wxID_COMPARE_DATA_GUI_MAINSTATICTEXT1, wxID_COMPARE_DATA_GUI_MAINSTATICTEXT2, 
 wxID_COMPARE_DATA_GUI_MAINSTATICTEXT3, wxID_COMPARE_DATA_GUI_MAINWELCOME, 
] = [wx.NewId() for _init_ctrls in range(10)]

class compare_data_gui_main(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_COMPARE_DATA_GUI_MAIN,
              name=u'compare_data_gui_main', parent=prnt, pos=wx.Point(307, 29),
              size=wx.Size(877, 485),
              style=wx.TAB_TRAVERSAL | wx.SYSTEM_MENU | wx.DEFAULT_FRAME_STYLE,
              title=u'Compare SPSS Data')
        self.SetClientSize(wx.Size(877, 485))
        self.SetBackgroundStyle(wx.BG_STYLE_COLOUR)
        self.SetThemeEnabled(True)
        self.SetStatusBarPane(1)
        self.SetHelpText(u'')
        self.SetBackgroundColour(wx.Colour(200, 200, 200))

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
        self.columns.SetThemeEnabled(True)

        self.staticText2 = wx.StaticText(id=wxID_COMPARE_DATA_GUI_MAINSTATICTEXT2,
              label=u'Please enter a comma separated list of columns to check for agreement:',
              name='staticText2', parent=self, pos=wx.Point(16, 192),
              size=wx.Size(476, 17), style=0)

        self.staticText3 = wx.StaticText(id=wxID_COMPARE_DATA_GUI_MAINSTATICTEXT3,
              label=u'Please choose an spss file to check:', name='staticText3',
              parent=self, pos=wx.Point(16, 104), size=wx.Size(300, 20),
              style=0)

        self.button1 = wx.Button(id=wxID_COMPARE_DATA_GUI_MAINBUTTON1,
              label=u'Evaluate it, Yo!', name='button1', parent=self,
              pos=wx.Point(698, 424), size=wx.Size(168, 40), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_COMPARE_DATA_GUI_MAINBUTTON1)

        self.genStaticText1 = wx.lib.stattext.GenStaticText(ID=wxID_COMPARE_DATA_GUI_MAINGENSTATICTEXT1,
              label=u'', name='genStaticText1', parent=self, pos=wx.Point(555,
            287), size=wx.Size(200, 120), style=0)
        self.genStaticText1.SetFont(wx.Font(76, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Sans'))
        self.genStaticText1.SetBackgroundStyle(wx.BG_STYLE_COLOUR)
        self.genStaticText1.SetBackgroundColour(wx.Colour(200, 200, 200))

        self.genStaticText2 = wx.lib.stattext.GenStaticText(ID=wxID_COMPARE_DATA_GUI_MAINGENSTATICTEXT2,
              label=u'', name='genStaticText2', parent=self, pos=wx.Point(650,
              392), size=wx.Size(200, 23), style=0)
        self.genStaticText2.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Sans'))
        self.genStaticText2.SetBackgroundColour(wx.Colour(200, 200, 200))

        self.path = wx.lib.filebrowsebutton.FileBrowseButton(buttonText=u'Browse',
              dialogTitle=u'Select a file', fileMask='*.*', fileMode=1,
              id=wxID_COMPARE_DATA_GUI_MAINPATH, initialValue='',
              labelText='Select a file:', parent=self, pos=wx.Point(16, 128),
              size=wx.Size(448, 56), startDirectory='.', style=wx.THICK_FRAME,
              toolTip='Type File name or browse to select')
        self.path.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.path.SetToolTipString(u'path')
        self.path.SetValue(u'')
        self.path.SetLabel(u'Select a file:')
        self.path.SetThemeEnabled(True)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnButton1Button(self, event):
        filename = self.path.GetValue()
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
