import sys, os, bottle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import index # Основной файл

application = bottle.default_app()
