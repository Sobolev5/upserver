import os
import sys
from django.core.wsgi import get_wsgi_application


path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, "%s" % path)
sys.path.insert(0, "%s/main" % path)
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
application = get_wsgi_application()
module_name = sys.argv[1]


exec("import %s" % module_name)
exec("{}.{}".format(module_name, " ".join(sys.argv[2:])))
