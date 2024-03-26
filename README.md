# UUCMigratiton: User-Unaware Container Live Migration
# Getting Started
## Dependencies

1. golang >= 1.19
2. protobuf 
3. protobuf-python
4. protobuf-c
5. protobuf-c-devel
6. protobuf-compiler
7. protobuf-devel
8. Python 3.8.8
4. numpy
5. pandas
6. sklearn
9. pytorch 2.0.1

## Installation

```shell

git clone https://github.com/CycleOfStrife/UUCMigration.git
cd criu-3.16.1
make && make install
cd runc 
make && make install
cd Podman
make && make install
```
## Run the UUCMigratiton System


```shell
#linux01
podman run -itd --name mybox docker.io/busybox
podman conatienr checkpoint --live-migration --predict-mode="SSPD" --dirty-file="test.csv" --ip=<linux02IP> --path="/migration" mybox

```
#linux02
```
mkdir /migration
cd /migration
podman container restore -i <the last file> mybox

```


