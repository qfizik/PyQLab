"""
Measurement filters
"""

from traits.api import HasTraits, Int, Float, List, Str, Dict, Bool
import enaml

class MeasFilter(HasTraits):
	name = Str
	channel = Int(1)
	enabled = Bool(True)

	def get_stack_view(self):
		with enaml.imports():
			from MeasFiltersViews import FilterStackView
		return FilterStackView(myFilter=self)

class DigitalHomodyne(MeasFilter):
	boxCarStart = Int(0, desc='The start index of the integration window in pts.')
	boxCarStop = Int(0, desc='The stop index of the integration window in pts.')
	IFfreq = Float(10e6, desc='The I.F. frequency for digital demodulation.')
	samplingRate = Float(250e6, desc='The sampling rate of the digitizer.')


class Correlator(MeasFilter):
	filters = List(MeasFilter)

class MeasFilterLibrary(HasTraits):
	filterDict = Dict(Str, MeasFilter)
	libFile = Str('MeasFilterLibrary.json', transient=True)
	filterList = List([DigitalHomodyne, Correlator], transient=True)

	def write_to_file(self):
		#Move import here to avoid circular import
		import JSONHelpers
		with open(self.libFile,'w') as FID:
			json.dump(self, FID, cls=JSONHelpers.QLabEncoder, indent=2, sort_keys=True)

	def load_from_file(self):
		pass

if __name__ == "__main__":

	#Work around annoying problem with multiple class definitions 
	from MeasFilters import DigitalHomodyne, MeasFilterLibrary

	testFilter1 = DigitalHomodyne(name='M1', boxCarStart=100, boxCarStop=500, IFfreq=10e6, samplingRate=250e6, channel=1)
	testFilter2 = DigitalHomodyne(name='M2', boxCarStart=150, boxCarStop=600, IFfreq=39.2e6, samplingRate=250e6, channel=2)

	testLib = MeasFilterLibrary()
	testLib.filterDict.update({'M1':testFilter1, 'M2':testFilter2})

	from enaml.stdlib.sessions import show_simple_view
	with enaml.imports():
		from MeasFiltersViews import MeasFilterManagerWindow
	session = show_simple_view(MeasFilterManagerWindow(filterLib=testLib))