# Lima Example: Python VM

This example shows how to use Lima to run a Linux VM with Python pre-installed, so you can run and test Python code in an isolated environment on macOS.

## Files
- `python.yaml` — Lima config file to provision Python in the VM

## Usage

1. Start the VM with the config:
   ```sh
   limactl start ./python.yaml
   ```
2. Open a shell in the VM:
   ```sh
   limactl shell python
   ```
3. Run Python code interactively or execute scripts:
   ```sh
   python3
   # or
   python3 myscript.py
   ```

## How it works
- The VM is provisioned with Ubuntu and Python 3 (plus pip) installed automatically.
- Your `/Users` directory is mounted writable, so you can edit code on your Mac and run it in the VM.

## Customization
- Edit `python.yaml` to add more packages or change mounts.
- Use `pip3` to install additional Python libraries as needed.

---
For more Lima examples, see the main project README or [Lima documentation](https://lima-vm.io/docs/).
