# Kubernetes restart

A kubernetes pod restart loop is usually memory pressure: the kubelet
kills the pod, the controller starts it again, and it dies again. Check
`kubectl describe pod` for the OOMKilled reason and raise the limit.
