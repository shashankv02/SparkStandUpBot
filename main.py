import bot
import backend
from multiprocessing import Process


#backend_process = Process(target=backend.start, args=bot.cq)
#backend_process.start()
if __name__ == "__main__":
    backend_process = Process(target=backend.start, args=(bot.incoming_q, bot.outgoing_q))
    backend_process.start()
    bot.start()

#bot.app.run()



