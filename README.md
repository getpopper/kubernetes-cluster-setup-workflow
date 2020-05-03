# Kubernetes Cluster With Popper

A [popper](https://github.com/systemslab/popper) workflow to setup a 3 node kubernetes cluster in cloudlab.us.

## Running instructions

* Set the `geni-lib` secret variables as given [here](https://github.com/popperized/library/tree/master/geni#secrets) and the `ansible` secret
variables as given [here](https://github.com/popperized/library/tree/master/ansible#secrets).

* Change the volume binding in `config.yml` according to your environment.

* Execute the workflow with popper.
```
$ popper run -f wf.yml -c config.yml --skip 'release nodes'
```

* Release the nodes in the cluster.
```
$ popper run -f wf.yml -c config.yml 'release nodes'
```
