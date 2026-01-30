# Installation: Docker, Podman, nerdctl in Lima

## Docker
```sh
# Start a Docker-enabled Lima VM using the template
limactl start template://docker

# Docker is pre-installed in this template. Use inside the VM:
lima docker ps
```

## Podman
```sh
# Start a Podman-enabled Lima VM using the template
limactl start template://podman

# Podman is pre-installed in this template. Use inside the VM:
lima podman ps
```

## nerdctl
```sh
# nerdctl is included in most Lima templates (including default, docker, and podman)
# Use inside the VM:
lima nerdctl ps
```

## Custom Installation (Advanced)
If you use a custom Lima template or want to install a container engine manually:

```sh
# Open a shell in your VM
limactl shell <vm-name>

# Example: Install Docker (Ubuntu)
sudo apt-get update && sudo apt-get install -y docker.io

# Example: Install Podman (Ubuntu)
sudo apt-get update && sudo apt-get install -y podman

# Example: Install nerdctl (see https://github.com/containerd/nerdctl)
# Download and extract the latest release from GitHub
```
# Lima CLI Cheatsheet

## General VM Management
```sh
# List all VMs
limactl list

# Start a VM (by name or template)
limactl start <vm-name>
limactl start template://docker

# Stop a VM
limactl stop <vm-name>

# Delete a VM (removes all data!)
limactl delete <vm-name>

# Show VM info
limactl info <vm-name>

# Open a shell in the VM
limactl shell <vm-name>

# Run a command in the VM
limactl shell <vm-name> <command>

# List available templates
limactl list-templates
```

## Container Engines (Docker, nerdctl, Podman)
```sh
# Run Docker/nerdctl/Podman commands inside the VM
lima docker ps
lima nerdctl run hello-world
lima podman ps

# Export Docker/Podman socket to host
export DOCKER_HOST=$(limactl list <vm-name> --format 'unix://{{.Dir}}/sock/docker.sock')
export CONTAINER_HOST=$(limactl list <vm-name> --format 'unix://{{.Dir}}/sock/podman.sock')

# Use Docker/Podman CLI on host
docker ps
podman --remote ps
```

## Kubernetes
```sh
# Start a Kubernetes VM
limactl start template://k8s

# Export kubeconfig for kubectl
export KUBECONFIG=$(limactl list k8s --format 'unix://{{.Dir}}/copied-from-guest/kubeconfig.yaml')

# Use kubectl
kubectl get nodes
kubectl get pods -A
```

## File Sharing & Mounts
```sh
# By default, your home directory is mounted in the VM at /Users/<yourname>
# To add more mounts, edit the VM's YAML config before starting
```

## Networking & Port Forwarding
```sh
# Ports published in the VM are forwarded to your macOS host
lima docker run -d -p 8080:80 nginx
# Access http://localhost:8080 on your Mac
```

## Troubleshooting
```sh
# View VM logs
limactl log <vm-name>

# Restart Lima daemon
limactl daemon
```
## Using Kubernetes in Lima

Lima supports running Kubernetes clusters using several engines:
- kubeadm (default)
- k3s
- k0s
- RKE2
- Usernetes

### Single-node Kubernetes (kubeadm, k3s, k0s, RKE2, Usernetes)

```sh
# Start a single-node Kubernetes VM
limactl start template://k8s

# Export kubeconfig for kubectl
export KUBECONFIG=$(limactl list k8s --format 'unix://{{.Dir}}/copied-from-guest/kubeconfig.yaml')

# Create a deployment and service
kubectl create deployment nginx --image=nginx:alpine
kubectl create service nodeport nginx --node-port=31080 --tcp=80:80
```

To customize the kubeadm configuration, edit `templates/k8s.yaml` before starting the VM.

See also: [Kubeadm Reference](https://kubernetes.io/docs/reference/setup-tools/kubeadm/)

### Multi-node Kubernetes Cluster

A multi-node cluster can be created by launching multiple VMs on the same user network:

```sh
# Start the first (control-plane) node
limactl start --name k8s-0 --network lima:user-v2 template:k8s

# Get the join command from the control-plane node
limactl shell k8s-0 sudo kubeadm token create --print-join-command
# (Copy the join command printed here)

# Start the second (worker) node
limactl start --name k8s-1 --network lima:user-v2 template:k8s

# Reset and clean up the worker node (if needed)
limactl shell k8s-1 sudo bash -euxc "kubeadm reset --force ; ip link delete cni0 ; ip link delete flannel.1 ; rm -rf /var/lib/cni /etc/cni"

# Join the worker node to the cluster
limactl shell k8s-1 sudo <JOIN_COMMAND_FROM_ABOVE>
```

The following templates support multi-node mode:
- k8s (since Lima v2.0)
- k3s (since Lima v2.1)

See the Lima documentation for more advanced Kubernetes scenarios.
## Using Podman in Lima

### Rootless & Rootful
Lima supports both rootless and rootful Podman containers.

### To use podman command in the VM:

```sh
limactl start template://podman
limactl shell podman podman run -d --name nginx -p 127.0.0.1:8080:80 docker.io/library/nginx:alpine
```

### To use podman command on the host:

```sh
export CONTAINER_HOST=$(limactl list podman --format 'unix://{{.Dir}}/sock/podman.sock')
podman --remote run -d --name nginx -p 127.0.0.1:8080:80 docker.io/library/nginx:alpine
```

### To use docker command on the host (with Podman socket):

```sh
export DOCKER_HOST=$(limactl list podman --format 'unix://{{.Dir}}/sock/podman.sock')
docker run -d --name nginx -p 127.0.0.1:8080:80 docker.io/library/nginx:alpine
```
# Lima (limactl) Command Examples

Lima (limactl) lets you run Linux virtual machines on macOS, which is useful for running container tools like Docker or nerdctl in a Linux environment.


## Basic Kubernetes VM Management with Lima

```sh
# List all Lima VMs (including Kubernetes VMs)
limactl list

# Start a Kubernetes VM (using the k8s template)
limactl start template://k8s

# Stop a Kubernetes VM
limactl stop k8s

# Delete a Kubernetes VM (removes all data!)
limactl delete k8s

# Show VM status and info
limactl info k8s

# Open a shell in the Kubernetes VM
limactl shell k8s

# Run a command in the Kubernetes VM
limactl shell k8s uname -a

# Export kubeconfig for kubectl access
export KUBECONFIG=$(limactl list k8s --format 'unix://{{.Dir}}/copied-from-guest/kubeconfig.yaml')

# Check cluster nodes
kubectl get nodes

# Check all pods in all namespaces
kubectl get pods -A
```

## Creating a New Lima VM

```sh
# Create a new VM with Docker support
limactl start --name=mydocker-template template://docker

# Or interactively
limactl start
```

## File Sharing

- By default, your home directory is mounted in the VM at `/Users/<yourname>`.
- You can configure additional mounts in your Lima YAML config.

## Using Docker or nerdctl in Lima

```sh
# Run Docker commands inside the Lima VM
lima docker ps
lima docker run hello-world

# Or use nerdctl (a Docker-compatible CLI)
lima nerdctl run -d -p 8080:80 nginx
```

## Exporting Docker Socket to Host

You can use Docker on your macOS host by exporting the Docker socket from Lima:

```sh
# Start a Docker-enabled Lima VM (if not already running)
limactl start template://docker

# Export the Docker socket for host usage
export DOCKER_HOST=$(limactl list docker --format 'unix://{{.Dir}}/sock/docker.sock')

# Now you can use the docker CLI on your host:
docke ps
docke run hello-world
```

## Docker Compose in Lima

```sh
# Use docker compose inside the Lima VM
lima docker compose up -d

# Or, with the exported socket, on your host:
docke compose up -d
```

## Port Forwarding

Lima automatically forwards ports from the VM to your macOS host. For example:

```sh
lima docker run -d --name nginx -p 127.0.0.1:8080:80 nginx:alpine
# Access http://localhost:8080 on your Mac
```

## Persistent Volumes

```sh
# Create a persistent volume
lima docker volume create mydata

# Use it in a container
lima docker run -d -v mydata:/data busybox tail -f /dev/null
```

## Troubleshooting

- If you see permission errors, check your Lima VM's mounts and user permissions.
- For network issues, ensure the VM is running and ports are forwarded.
- For more, see the [Lima FAQ](https://lima-vm.io/docs/faq/).

## More Examples
- [Lima Container Examples](https://lima-vm.io/docs/examples/containers/)
- [Lima Docker Example](https://lima-vm.io/docs/examples/containers/docker/)

## Helpful Links
- [Lima Documentation](https://github.com/lima-vm/lima)
- [Lima Getting Started](https://github.com/lima-vm/lima/blob/master/docs/getting-started.md)

---

## Example: Using a Custom YAML Config File

You can create a Lima VM with a custom configuration by writing a YAML file (e.g., `myvm.yaml`).

Example `myvm.yaml`:
```yaml
images:
	- location: "https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img"
		arch: "x86_64"
mounts:
	- location: "/Users/yourname/projects"
		writable: true
containerd:
	system: true
	user: false
provision:
	- mode: system
		script: |
			apt-get update && apt-get install -y htop
```

To start a VM with this config:
```sh
limactl start ./myvm.yaml
```

For more advanced usage, see the Lima docs or your VM's YAML config file.
