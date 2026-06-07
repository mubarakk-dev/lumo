# Virtual Machines

A virtual machine, or VM, is a software-based computer that runs its own operating system on top of a host machine.

## How VMs Work

A hypervisor creates and manages virtual hardware such as CPU, memory, disk, and network devices.

Each VM usually includes:

- a full guest operating system
- virtual hardware
- installed applications
- its own isolated environment

## Docker Compared With VMs

Docker containers share the host operating system kernel.

Virtual machines run a full guest operating system.

## Key Difference

- VM = heavier isolation with a full operating system
- Container = lighter isolation for running application processes

## When VMs Are Useful

VMs are useful when you need a separate operating system, stronger isolation, or infrastructure that behaves like a complete machine.
