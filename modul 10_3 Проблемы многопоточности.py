# Задача "Банковские операции"
# Цель: освоить блокировки, используя объекты класса Lock и его методы
# Для генерации случайного целого числа используйте randint из random.
# Для ожидания используйте функцию sleep из модуля time.
# Особо важно соблюсти верную блокировку:
# в take замок закрывается, в deposit открывается.

import threading
from random import randint
from time import sleep
from threading import Lock


class Bank:

	def __init__(self):
		self.balance = 0
		self.lock = Lock()

	def deposit(self):
		for i in range(100):
			if self.balance >= 500 and self.lock.locked():
				self.lock.release()
			count = randint(50, 500)
			self.balance += count
			print(f'Пополнение: {count}. Баланс: {self.balance}')
			sleep(0.001)

	def take(self):
		for i in range(100):
			count = randint(50, 500)
			print(f'Запрос на {count}.')
			if count <= self.balance:
				self.balance -= count
				print(f'Снятие: {count}. Баланс: {self.balance}')
			if count > self.balance:
				print(f'Запрос отклонён, недостаточно средств')
				self.lock.acquire()


bk = Bank()
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f"Итоговый баланс: {bk.balance}")
