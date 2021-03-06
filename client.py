#Entry point for client

import sys
from twisted.internet import reactor
from twisted.python import log
from client.player import *
from client.creep import *
from client.environment import Environment
from client.ui import *
sys.path.append('data')

def main():
	host = 'localhost'
	port = 1338
	multi = False
	resolution = [800,800]

	if multi:
		print 'Client - Multi Player port:', port
		run(host,port)
	else:
		print 'Client - Single Player'
		environment = Environment(100, reactor)
		environment.start()
		window = Window(environment, resolution)
		player = Player([200,200],[200,200], environment.seconds, resolution)
		#creep = Creep([200,200],[200,200], environment.seconds, resolution)
		window.client = player
		window.submitTo(PlayerController(player))
		window.go()
		reactor.run()
		
def run(host, port, res):
	log.startLogging(sys.stdout)
	client = UI()
	a = client.start(host,port)
	a.addErrback(log.err, "Server Error")
	a.addCallback(lambda ignored: reactor.stop())
	client.reactor.run()
	pygame.quit()
	sys.exit()

if __name__ == '__main__':
    main()
