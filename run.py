import sys, os

sys.path.append('backend/') # указываем директорию с проектом

from backend import app as application # когда Flask стартует, он ищет application. Если не указать 'as application', сайт не заработает

application.run(debug=True)
