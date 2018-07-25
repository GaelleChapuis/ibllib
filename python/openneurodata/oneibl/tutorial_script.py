## Init
from oneibl.one import ONE
myone = ONE() # need to instantiate the class to have the API.

## Load #1
dataset_types = ['cwStimOn.times', 'cwStimOn.contrastRight', 'cwStimOn.contrastLeft']
eid = 'http://localhost:8000/sessions/698361f6-b7d0-447d-a25d-42afdef7a0da'
t, cr, cl = myone.load(eid, dataset_types=dataset_types)

## Load #2
my_data = myone.load(eid, dataset_types=dataset_types, dclass_output=True)
from ibllib.misc import pprint
pprint(my_data.local_path)
pprint(my_data.dataset_type)

## Load everything
my_data = myone.load(eid)

## Load
dataset_types = ['cwStimOn.times', 'thisDataset.IveJustMadeUp', 'cwStimOn.contrastLeft']
t, empty, cl = myone.load(eid, dataset_types=dataset_types)

## List #1
myone.list(table='dataset-types', verbose=True)

## List #2
list_types , dtypes = myone.list(table=['dataset-types','users'])
pprint(list_types)
pprint(dtypes)

## Search users
sl, sd = myone.search(users=['Morgane','miles','armin'])
pprint(sl)

## Search by date
sl, sd = myone.search(users='miles', date_range=['2018-03-01', '2018-03-24'])


