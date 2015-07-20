# coding=UTF-8
__author__ = 'Termvsrobo'
__doc__ = """
sendSMS отправляет СМС сообщения посредством USB-модема.
"""

import serial
import time
import math
import random


starttime = time.time()


# u'Функция убирает знак "+" из номера телефона, добавляет "F" в конце, если длина номера нечетная,
# u'и попарно меняет местами цифры в номере телефона. Возвращает полученный результат
def convertnumberphone(number):
	number = list(number)

	# Удаляем знак "+", если он есть в номере
	if '+' in number:
		del number[number.index('+')]

	# Если длина строки нечетная, то в конце добавляем букву "F"
	if len(number) % 2 != 0:
		number.append('F')
	# Переставляем попарно цифры в номере
	for i in range(0, len(number) - 1, 2):
		number[i], number[i + 1] = number[i + 1], number[i]

	# Объединяем все в строку
	number = ''.join(number)

	# Возвращаем итоговый результат
	return number


# Функция конвертирования текста в формат PDU
def convertmessagetext(message):
	result = ''
	for symbol in message:
		s = '%X' % ord(symbol)
		s = s.zfill(4)
		result += s
	return result


# Формула отправляемого сообщения в формате PDU: SMS = SCA + TPDU
# где SCA - номер телефона SMS - центра, через который отправляется SMS
# TPDU = содержит номер получателя, само сообщение (закодированное в UCS2) и несколько служебных полей

# 07 - размер байта = 91 (1 байт) + 79232909090 (6 байт), 91 - тип номера международного
# формата, 79232909090 - номер СМС центра Мегафон
SCA = '07' + '91' + convertnumberphone('+79232909090')


def send_sms(number, mes):
	# Конвертируем в юникод
	mes = mes.decode("utf-8")

	tp_da = '0B' + '91' + convertnumberphone(number)

	tp_pid = '00'  # идентификатор протокола
	tp_dcs = '08'  # Схема кодирования данных. Указывает, в каком формате представлено сообщение.
	tp_vp = '00'  # время действия сообщения (если сообщение не будет получено абонентом в течение этого времени,
	# sms-центр его удалит)

	ser = serial.Serial('COM4', 128000)

	ser.write('AT+CMGF=0\r')
	time.sleep(0.1)
	u = ser.read(640)
	print(u)

	if len(mes) <= 67:
		kol_sms = 1 # Количество смс для отправки
		# TPDU = pdu_type + tp_mr + tp_da + tp_pid + tp_dcs + tp_vp + tp_udl + tp_ud
		pdu_type = '11'  # b00010001 Поле флагов типа сообщения
		tp_mr = '00'

		tp_udl = '%X' % (2 * len(mes))  # длина сообщения
		tp_udl = tp_udl.zfill(2)  # добавляем нолик в начале, чтобы было двузначное число. Такие требования.
		tp_ud = convertmessagetext(mes)  # непосредственно текст sms-сообщения, закодированный согласно полю TP-DCS

		tpdu = pdu_type + tp_mr + tp_da + tp_pid + tp_dcs + tp_vp + tp_udl + tp_ud

		sms = SCA + tpdu

		lentpdu = str((len(tpdu)) / 2)

		ser.write('AT+CMGS=' + lentpdu + '\r')
		time.sleep(1.5)
		r = ser.read(640)
		print(r)
		time.sleep(1.5)
		ser.write(sms + '\x1a')
		time.sleep(1.5)
		e = ser.read(640)
		print(e)

		return kol_sms # Возвращаем количество смс для отправки
	else:
		kol_sms = float(len(mes))/67.0 # Количество смс для отправки
		kol_sms = int(math.ceil(kol_sms)) # Округляем до ближайшего большего целого

		pdu_type = '41'  # b01000001 Поле флагов типа сообщения

		rand = random.randint(0, 255)
		rand = '%X' % rand
		rand = rand.zfill(2)
		for i in range(0, kol_sms, 1):
			tp_mr = str(i).zfill(2)

			tp_udl = '%X' % (2 * len(mes[i*67:67*(i+1)]) + 6)  # длина сообщения
			tp_udl = tp_udl.zfill(2)  # добавляем нолик в начале, чтобы было двузначное число. Такие требования.

			tp_sms = '%X' % kol_sms
			tp_sms = tp_sms.zfill(2)

			tp_i = '%X' % (i+1)
			tp_i = tp_i.zfill(2)

			tp_udh = '05' + '00' + '03' + rand + tp_sms + tp_i

			tp_ud = convertmessagetext(mes[i*67:67*(i+1)])  # непосредственно текст sms-сообщения, закодированный согласно полю TP-DCS

			tpdu = pdu_type + tp_mr + tp_da + tp_pid + tp_dcs + tp_udl + tp_udh + tp_ud

			sms = SCA + tpdu

			lentpdu = str((len(tpdu)) / 2)


			ser.write('AT+CMGS=' + lentpdu + '\r')
			time.sleep(1.6)
			r = ser.read(640)
			print(r)
			time.sleep(1.6)
			ser.write(sms + '\x1a')
			time.sleep(1.6)
			e = ser.read(640)
			print(e)

		return kol_sms # Возвращаем количество смс для отправки


if __name__ == '__main__':
	o = send_sms('+79061980010', 'Это тестовое сообщение для проверки получения клиентом Билайна сообщений от компании Антонов двор. Пожалуйста, не отвечайте на это сообщение. Копия5')

	executetime = time.time() - starttime
	print('Время выполнения = %s секунд' % executetime)
