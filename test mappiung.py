import hyperspy.api as hs
s = hs.load("EDS Data.rpl")
s.axes_manager.gui() 