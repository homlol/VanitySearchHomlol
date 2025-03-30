import requests
import json
import os
import random

def hex_to_int(hex_value):
	"""Преобразует шестнадцатеричное значение в целое число."""
	return int(hex_value, 16)

def int_to_hex(int_value):
	"""Преобразует целое число в шестнадцатеричное значение."""
	return hex(int_value)[2:]  # убираем '0x' в начале

def divide_hex(a, b, n):
	"""Делит диапазон [a, b] на n равных частей и выводит их границы."""
	a_int = hex_to_int(a)
	b_int = hex_to_int(b)
	if a_int >= b_int:
		raise ValueError("a должно быть меньше b")
	step = (b_int - a_int) // n
	ranges = []
	for i in range(n):
		start = a_int + i * step
		end = a_int + (i + 1) * step
		ranges.append((int_to_hex(int(start)), int_to_hex(int(end))))
		print(int_to_hex(int(start)), int_to_hex(int(end)))
	return ranges

def get_range_by_part(a, b, n, part_number):
	part_number-=1
	"""Возвращает начальное и конечное значение для заданной части."""
	if part_number < 0 or part_number > n:
		raise ValueError("Номер части должен быть в диапазоне от 1 до n")
	a_int = hex_to_int(a)
	b_int = hex_to_int(b)
	if a_int >= b_int:
		raise ValueError("a должно быть меньше b")
	step = (b_int - a_int) // n
	ranges = []
	start = a_int + part_number * step
	end = a_int + (part_number + 1) * step
	return int_to_hex(int(start)), int_to_hex(int(end))

def get_part_number_by_value(a, b, n, value):
	"""Возвращает номер диапазона для заданного шестнадцатеричного значения."""
	a_int = hex_to_int(a)
	b_int = hex_to_int(b)
	if a_int >= b_int:
		raise ValueError("a должно быть меньше b")
	step = (b_int - a_int) // n
	# Преобразуем значение из hex в int
	value_int = hex_to_int(value)
	if value_int < a_int or value_int >= b_int:
		raise ValueError("Значение должно быть в диапазоне от a до b")
	# Находим номер диапазона
	part_number = (value_int - a_int) // step
	return part_number + 1  # Возвращаем номер диапазона (с 1)

def takeCheckedRange():
	url = 'https://btc.homlol.ru/api/getCheckedRange'
	data = {"api_get_checked_range": True}
	response = requests.post(url, data=data)
	return response.json()

def selectRange(number_range):
	url = 'https://btc.homlol.ru/api/selectRange'
	data = {"api_select_range": True, "number_range": number_range}
	response = requests.post(url, data=data)
	return response.json()

def setRange(number_range, comment = '', mass = {}):
	url = 'https://btc.homlol.ru/api/setRange'
	data = {"api_save_select_range": True, "number_range": number_range, "comment": comment, "mass": json.dumps(mass)}
	response = requests.post(url, data=data)
	return response.json()

if __name__ == "__main__":

	# tmp's
	#main_path = "C:/bitcoin/VanitySearchHomlol/x64/Release/" # заменить на нужный путь или оставить пустыл если файл находится в одной папке вместе с VanitySearch
	main_path = ""
	name_in_file = "in.txt"
	name_out_file = "Found.txt"
	quantity = 0
	main_address = "1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ"
	a = "80000000000000000" # шестнадцатеричное значение
	b = "fffffffffffffffff"
	n = 1000000 # кол-во областей
	comment = "BITCOIN PUZZLE HoMLoL POOL bc1qdn2wng73y80phr7kul5aa24n850f5c82zwq27h" # ваш комментарий

	while True:
		quantity+=1

		os.system('cls')

		mass_checked_range = {}

		print('--------------------------------------------------------------------------')
		print('----------------------- BITCOIN PUZZLE HoMLoL POOL -----------------------')
		print('--------------------------------------------------------------------------')
		print('-- Questions/Offers: TG @homlol_official                                --')
		print('-- Group: TG @homlol_pool                                               --')
		print('-- Donate BTC: bc1qdn2wng73y80phr7kul5aa24n850f5c82zwq27h               --')
		print('--------------------------------------------------------------------------')

		print('*** Synchronization of checked range ***')
		checked_range = takeCheckedRange()
		print(f'* Total checked: {len(checked_range["result"])}')
		for i in checked_range['result']:
			mass_checked_range[i] = i

		print('*** Select random range ***')
		while True:
			page = random.randint(1, n)
			if page not in mass_checked_range:
				break

		print(f'* Range number: {page}')
		print('* Addresses for search:')
		select_range = selectRange(page)

		file_path = f'{main_path}{name_in_file}'

		with open(file_path, 'w', encoding='utf-8') as file:
			for i in select_range['addresses']:
				file.write(str(i)+"\n")
				print(f'\t - {i}')
		range_hex = get_range_by_part(a, b, n, page)
		print(f'* Range hex: {range_hex[0]}:{range_hex[1]}')

		os.system(f'{main_path}VanitySearch.exe -t 0 -gpu -gpuId 0 -i {main_path}{name_in_file} -o {main_path}{name_out_file} --keyspace {range_hex[0]}:{range_hex[1]}')

		db_mass = {}
		with open(f'{main_path}tmp_homlol_pool_found.txt', 'r') as bs: # tmp_homlol_pool_found.txt имя файла в который сохраняются адреса и приватные ключи для проверки. НЕ МЕНЯТЬ!
			for i in bs.readlines():
				addr, key = i.strip().split(',')
				db_mass[addr] = key

		print(db_mass)

		if main_address in db_mass: # если нашли основной ключ!!!!
			print(f'Address: {main_address}')
			print(f'Private key: {db_mass[main_address]}')
			print('--------------------------------------- !!! НАЙДЕНО !!! ------------------------------------------')
			break;
		else: # если нет, отправляем инфу в пул
			new_mass_for_send = {}
			for i in select_range['addresses']:
				try:
					new_mass_for_send[i] = db_mass[i]
				except:
					pass

			if not new_mass_for_send:
				print("* Error: Not data for send")
			else:
				print(setRange(page, comment, new_mass_for_send))



# Кто захочет сам компилировать версию от https://github.com/allinbit/VanitySearch/

# 1. Исправте код в файле main.cpp. 171 строка, scanf на sscanf.
# 2. Добавьте этот фрагмент кода в функцию void VanitySearch:output(){} он служит для получения результата флагов от VanitySearch в файл скрипта к пулу.

# 	// pool save to tmp file start ->

# 	string outputFile_homlol_pool;
# 	string outputFile_homlol_pool_info;
# 	string tmp_found_address;
# 	string tmp_found_private;
# 	FILE* f_pool = stdout;

# 	outputFile_homlol_pool = "tmp_homlol_pool_found.txt";

# 	f_pool = fopen(outputFile_homlol_pool.c_str(), "a");
# 	if (f_pool == NULL) {
# 		fprintf(stderr, "Cannot open %s for writing\n", outputFile_homlol_pool.c_str());
# 		f_pool = stdout;
# 	}

# 	tmp_found_address = addr.c_str();
# 	tmp_found_private = pAddrHex.c_str();

# 	outputFile_homlol_pool_info = tmp_found_address + "," + tmp_found_private + "\n";

# 	fprintf(f_pool, outputFile_homlol_pool_info.c_str());

# 	// pool save to tmp file end <-