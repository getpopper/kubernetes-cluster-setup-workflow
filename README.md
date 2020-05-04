# Kubernetes Cluster With Popper

A [popper](https://github.com/systemslab/popper) workflow to setup a kubernetes cluster in cloudlab.us.

## Running instructions

* Set the `geni-lib` secret variables as given [here](https://github.com/popperized/library/tree/master/geni#secrets) and the `ansible` secret
variables as given [here](https://github.com/popperized/library/tree/master/ansible#secrets).

* Change the volume binding in [`config.yml`](https://github.com/JayjeetAtGithub/kubernetes-cluster-popper/blob/master/config.yml#L4) according to your environment.

* Execute the workflow with popper.
```
$ popper run -f wf.yml -c config.yml --skip 'release nodes'
```

* Release the nodes in the cluster.
```
$ popper run -f wf.yml -c config.yml 'release nodes'
```

**NOTE**: The configuration of the cluster is described by
the following environment variables defined in `config.yml`:
* `NODES`: Specifies the size of the kubernetes cluster.
* `NODE_HARDWARE`: Specifies the compute hardware for the nodes.
* `NODE_CLUSTER`: Specifies the cloudlab cluster to use.
* `NODE_SLICE_NAME`: Specifies the name of the slice.
