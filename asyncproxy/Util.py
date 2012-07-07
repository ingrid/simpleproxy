import select
from pprint import pformat

KQ_EVS = dict((getattr(select, att), att) for att in dir(select) if att.startswith('KQ_EV_'))
KQ_FILTERS = dict((getattr(select, att), att) for att in dir(select) if att.startswith('KQ_FILTER_'))
KQ_NOTE_NUMS = dict((att, getattr(select, att)) for att in dir(select) if att.startswith('KQ_NOTE_'))

KQ_NOTE_MAP = {
	'KQ_FILTER_READ' : [
		'KQ_NOTE_LOWAT',
		],
	'KQ_FILTER_WRITE' : [
		'KQ_NOTE_LOWAT',
		],
	'KQ_FILTER_VNODE' : [
		'KQ_NOTE_DELETE',
		'KQ_NOTE_WRITE',
		'KQ_NOTE_EXTEND',
		'KQ_NOTE_ATTRIB',
		'KQ_NOTE_LINK',
		'KQ_NOTE_RENAME',
		'KQ_NOTE_REVOKE',
	],
	'KQ_FILTER_PROC' : [
		'KQ_NOTE_EXIT',
		'KQ_NOTE_FORK',
		'KQ_NOTE_EXEC',
		'KQ_NOTE_PCTRLMASK',
		'KQ_NOTE_PDATAMASK',
		'KQ_NOTE_TRACK',
		'KQ_NOTE_CHILD',
		'KQ_NOTE_TRACKERR',
	],
}
#	'KQ_FILTER_NETDEV' : [
#		'KQ_NOTE_LINKUP',
#		'KQ_NOTE_LINKDOWN',
#		'KQ_NOTE_LINKINV',
#	],
#}
for filter in KQ_NOTE_MAP:
	d = {}
	for note in KQ_NOTE_MAP[filter]:
		num = KQ_NOTE_NUMS[note]
		d[num] = note
	KQ_NOTE_MAP[filter] = d

class EventWrapper(object):
	def __init__(self, event):
		self.event = event
		self.ident = event.ident
		self.filter = KQ_FILTERS.get(event.filter, '?')
		self.flags = []
		for value in KQ_EVS:
			if value & event.flags:
				self.flags.append(KQ_EVS[value])
		self.fflags = []
		for value, fflag in KQ_NOTE_MAP[self.filter].iteritems():
			if value & event.fflags:
				self.fflags.append(fflag)
	def __str__(self):
		return pformat(dict([(att, getattr(self, att)) for att in 'event', 'ident', 'filter', 'flags', 'fflags']))
