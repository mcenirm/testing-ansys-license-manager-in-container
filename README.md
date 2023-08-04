# testing-ansys-license-manager-in-container

1. Download `AnsysLicenseManager.tgz` for 64-bit Linux
2. Extract `AnsysLicenseManager.tgz` so that `AnsysLicenseManager/linx64/INSTALL` exists
3. Start compose services (`podman-compose up` or `docker compose up`)
4. Review output from INSTALL command


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
