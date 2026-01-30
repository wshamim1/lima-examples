# Lima Example: Apache HTTP Server

This example shows how to use Lima to run an Apache HTTP server in a Linux VM on macOS, with port forwarding to your host.

## Files
- `apache.yaml` — Lima config file to provision Apache in the VM

## Usage

1. Start the VM with the config:
   ```sh
   limactl start ./apache.yaml
   ```
2. Once started, open your browser and go to [http://localhost:8088](http://localhost:8088)
   - You should see the Apache default page served from the VM.
3. To access the VM shell:
   ```sh
   limactl shell apache
   ```

## How it works
- The VM is provisioned with Ubuntu and Apache installed automatically.
- Port 80 in the VM is forwarded to port 8088 on your Mac.
- The Apache service is enabled and started on boot.

## Customization
- Edit `apache.yaml` to change the port, add mounts, or install more packages.

---
For more Lima examples, see the main project README or [Lima documentation](https://lima-vm.io/docs/).
