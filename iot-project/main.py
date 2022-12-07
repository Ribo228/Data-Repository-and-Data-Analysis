from app import app
from apireads import *
from apiwrites import *
from apihelpers import *

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9000)