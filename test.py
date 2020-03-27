import os
import time
from pip._internal.utils.misc import get_installed_distributions

for package in get_installed_distributions():
     print (package, time.ctime(os.path.getctime(package.location)))