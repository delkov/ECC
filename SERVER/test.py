with open("test.txt",'r', encoding='utf-8') as txt:	
	all_strings=txt.readlines()

	if all_strings[0]=='\n':
		print(all_strings)