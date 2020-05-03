import os

from geni.aggregate import cloudlab
from geni import util


ctx = util.loadContext("/geni-context.json",
                       key_passphrase=os.environ['GENI_KEY_PASSPHRASE'])

print("Available slices: {}".format(ctx.cf.listSlices(ctx).keys()))

if util.sliceExists(ctx, 'kube-cluster'):
    print('Slice exists.')
    print('Removing all existing slivers (errors are ignored)')
    util.deleteSliverExists(cloudlab.Utah, ctx, 'kube-cluster')
else:
    print("Slice does not exist.")