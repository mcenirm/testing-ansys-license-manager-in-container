set -euo pipefail

cd /AnsysLicenseManager/linx64/

./INSTALL -silent -lm

touch /run-install.completed
