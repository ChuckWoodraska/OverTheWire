from httpimport import remote_repo
import httpimport

httpimport.INSECURE = True

with remote_repo(['hello', 'neat'], base_url='http://127.0.0.1:5002'):
	from hello import hi
	import neat
neat.Neat().print_neat()
print(dir(hi))
hi.HelloWorld().print_hello()

import_list = ['hello', 'neat']
obj_dict = {}
for item in import_list:
	obj_dict[item] = httpimport.load(item, 'http://127.0.0.1:5002')
obj_dict['neat'].Neat().print_neat()
print(dir(obj_dict['hello'].hi))
obj_dict['hello'].hi.HelloWorld().print_hello()
