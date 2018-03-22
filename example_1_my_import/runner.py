from example_1_my_import import memoryimporter

neat = memoryimporter.load('neat', 'http://127.0.0.1:5002')
neat.Neat().print_neat()
