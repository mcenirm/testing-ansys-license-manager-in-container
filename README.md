# testing-ansys-license-manager-in-container


## General preparation

1. Download `AnsysLicenseManager.tgz` for 64-bit Linux
2. Extract `AnsysLicenseManager.tgz` so that `AnsysLicenseManager/linx64/INSTALL` exists


## RPM tests

### Build RPM

1. Build RPM

   ```shell
   podman-compose -f rpmbuild-compose.yaml down -v ; podman-compose -f rpmbuild-compose.yaml up
   ```

2. Review RPM

   ```shell
   rpm -qp builtrpms/RPMS/x86_64/ansyslmd-2023.2-1.el9.x86_64.rpm -lv
   ```

3. TODO


### Test RPM under systemd

1. Build test image, with RPM installed

   ```shell
   podman-compose -f rpmtest-compose.yaml build
   ```

2. Start test container

   ```shell
   podman-compose -f rpmtest-compose.yaml up -d
   ```

3. Inspect test container

   ```shell
   podman-compose -f rpmtest-compose.yaml exec rpmtest systemctl status
   podman-compose -f rpmtest-compose.yaml exec rpmtest /usr/ansys_inc/shared_files/licensing/linx64/lmutil lmstat
   ```

4. TODO


## Original test

1. Start compose services (`podman-compose -f test-compose.yaml up` or `docker compose -f test-compose.yaml up`)
2. Review output for any errors
3. Review outputs saved to `scratch/`

Expected (successful?) ending of `/ansys_inc/install.log`:

```
Installation Complete: Ddd Mmm DD HH:MM:SS YYYY
<---------------------------------------<<<
```

Ending of `/ansys_inc/install_licconfig.log`:

```
YYYY/MM/DD HH:MM:SS  *** DETERMINING IF THE FLEXNET DONGLE DRIVER MANUAL STEPS ARE RELEVANT...
YYYY/MM/DD HH:MM:SS  No license files were found. Therefore, the FlexNet dongle driver manual steps are not required.


YYYY/MM/DD HH:MM:SS  *** Exiting the configuration with exit code 0 ***


@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
```

List changed/added/deleted files in the test container's file system:

```shell
podman diff ${PWD##*/}_test_1
```

Inspect the installation volumes with 

```shell
podman run --rm -it -v $PWD/scratch:/scratch:rw,Z -v ${PWD##*/}_ansys_inc:/ansys_inc ${PWD##*/}_test bash
```


# notes

## missing library

`/ansys_inc/install.err` shows:

```
/ansys_inc/shared_files/licensing/tools/bin/linx64/ansyslm_config: error while loading shared libraries: libSM.so.6: cannot open shared object file: No such file or directory
```

Find package that provides the missing library:

```shell
MISSINGLIBRARY=libSM.so.6
podman run --rm -it localhost/${PWD##*/}_test:latest dnf -q provides $MISSINGLIBRARY'()(64bit)'
```

Matching packages:

```
libSM-1.2.3-10.el9.x86_64 : X.Org X11 SM runtime library
Repo        : rhel-9-for-x86_64-appstream-rpms
Matched from:
Provide    : libSM.so.6()(64bit)

libSM-1.2.3-10.el9.x86_64 : X.Org X11 SM runtime library
Repo        : ubi-9-appstream-rpms
Matched from:
Provide    : libSM.so.6()(64bit)

```

Append package (eg, `libSM-1.2.3-10.el9.x86_64`) to `dnf install` list in [`test-image/Containerfile`](test-image/Containerfile):

```patch
--- a/test-image/Containerfile
+++ b/test-image/Containerfile
@@ -3,4 +3,5 @@ RUN dnf makecache
 RUN dnf install -q -y \
     procps-ng-3.3.17-11.el9.x86_64 \
     freetype-2.10.4-9.el9.x86_64 \
+    libSM-1.2.3-10.el9.x86_64 \
  && dnf clean all
```

Rerun `podman-compose build`.

Clean old volume(s) with `podman-compose down -v`.
