import re
import os
from os import path
import msvcrt
import glob


class Ports:
	def __init__(self):
		self.po_name = ""
		self.po_direction = ""
		self.po_nbits = 1
		self.po_tag = ""

class Parameters:
	def __init__ (self):
		self.pa_name = ""
		self.pa_value = 0

class Connections:
	def __init__ (self):
		self.from_port = ""
		self.to_port = ""
		self.to_module = ""

class Module:
	def __init__(self):
		self.nParameters = -1
		self.nPorts = -1
		self.nConnections = -1
		self.Name = ""
		self.nInstance = 0
		self.Master = None
		self.Ports = []
		self.Parameters = []
		self.Connections = []

class Connect:
	def __init__ (self):
		self.from_module = ""
		self.from_port = ""
		self.to_port = ""
		self.to_module = ""
		self.signal_name = ""
		self.from_nInstance = 0
		self.to_nInstance = 0
		self.nBits = 1

class Exterior_Connection:
	def __init__ (self):
		self.in_out_name=""
		self.to_port = 0
		self.from_module = 0

# Reads a file and stores the relevant data in Modules
def read(Modules):
	path = 'XML'

	for filename in glob.glob(os.path.join(path, '*.txt')):
		with open(filename, 'r') as f: # open in readonly mode
	
			lines = f.readlines()

			# Temporary data storage
			port_names = []
			port_directions = []
			param_names = []
			param_values = []
			port_connections = []
			port_widths = []
			port_tags = []
			i = 0
			prova = False
			#Data acquisition
			while i < len(lines):
				line = lines[i]
				if "<ipxact:moduleName>" in line:
					Modules.append(Module())

					p = re.compile("<ipxact:moduleName>(.*)</ipxact:moduleName>")
					name = p.search(line)
					Modules[-1].Name = name.group(1)

					while "</ipxact:componentInstantiation>" not in line:
						
						if "<ipxact:moduleParameter " in line:

							Modules[-1].nParameters += 1
							Modules[-1].Parameters.append(Parameters())
							while "</ipxact:moduleParameter>" not in line:
								i += 1
								line = lines[i]
								if "<ipxact:moduleParameter " in line:
									Modules[-1].nParameters += 1
									Modules[-1].Parameters.append(Parameters())
								if "<ipxact:name>" in line:
									p = re.compile("<ipxact:name>(.*)</ipxact:name>")
									param_names.append(p.search(line))
									Modules[-1].Parameters[Modules[-1].nParameters].pa_name = param_names[-1].group(1)						
								if "<ipxact:value>" in line:
									p = re.compile("<ipxact:value>(.*)</ipxact:value>")
									param_values.append(p.search(line))
									Modules[-1].Parameters[Modules[-1].nParameters].pa_value = int(param_values[-1].group(1))
						if "<ipxact:classType>" in line:     														#Invented parameter from the IP-XACT protocol
							p = re.compile("<ipxact:classType>(.*)</ipxact:classType>")
							classType = p.search(line)
							if classType.group(1) == "Master" or classType.group(1) == "master":
								Modules[-1].Master = True
							elif classType.group(1) == "Slave" or classType.group(1) == "slave":
								Modules[-1].Master = False
									
						i += 1
						line = lines[i]

								
				if "<ipxact:port>" in line:

					Modules[-1].nPorts += 1
					Modules[-1].Ports.append(Ports())

					while "</ipxact:ports>" not in line:
						i += 1
						line = lines[i]

						if "<ipxact:port>" in line:
							Modules[-1].nPorts += 1
							Modules[-1].Ports.append(Ports())
						if "<ipxact:name>" in line:
							p = re.compile("<ipxact:name>(.*)</ipxact:name>")
							port_names.append(p.search(line))
							Modules[-1].Ports[Modules[-1].nPorts].po_name = port_names[-1].group(1)

						if "<ipxact:direction>" in line:
							p = re.compile("<ipxact:direction>(.*)</ipxact:direction>")
							port_directions.append(p.search(line))
							Modules[-1].Ports[Modules[-1].nPorts].po_direction = port_directions[-1].group(1)

						if "<ipxact:width>" in line:
							p = re.compile("<ipxact:width>(.*)</ipxact:width>")
							port_widths.append(p.search(line))
							Modules[-1].Ports[Modules[-1].nPorts].po_nbits = port_widths[-1].group(1)

						if "<ipxact:tag>" in line:
							p = re.compile("<ipxact:tag>(.*)</ipxact:tag>")
							port_tags.append(p.search(line))
							Modules[-1].Ports[Modules[-1].nPorts].po_tag = port_tags[-1].group(1)



				i += 1	
			f.close()


def read_connections(file_name, Modules):
	f = open(os.path.join("Connections", file_name + ".txt"), 'r')
	lines = f.readlines()
	i = 0

	while i < len(lines):
		line = lines[i]

		if "<ipxact:adHocConnection>" in line:
			while "</ipxact:adHocConnections>" not in line:
				i += 1
				line = lines[i]

				if "<ipxact:internalPortReference " in line:
					p = re.compile('<ipxact:internalPortReference componentRef="u_(.*)" ')
					module1 = p.search(line)
					p = re.compile(' portRef="(.*)"/>')
					port_name1 = p.search(line)

					print(module1.group(1))
					print(port_name1.group(1))

					module_index1 = 0
					for module in Modules:
						if module.Name == module1.group(1):
							module.nConnections += 1
							module.Connections.append(Connections())
							port_index1 = 0
							for port in module.Ports:
								if port.po_name == port_name1.group(1):
									break
								port_index1 += 1
							break
						module_index1 += 1

					i += 1
					line = lines[i]
					if "<ipxact:internalPortReference " in line:	
						p = re.compile('<ipxact:internalPortReference componentRef="u_(.*)" ')
						module2 = p.search(line)
						p = re.compile(' portRef="(.*)"/>')
						port_name2 = p.search(line)

						module_index2 = 0
						for module in Modules:
							if module.Name == module2.group(1):
								module.nConnections += 1
								module.Connections.append(Connections())
								port_index2 = 0
								for port in module.Ports:
									if port.po_name == port_name2.group(1):
										break
									port_index2 += 1
								break
							module_index2 += 1


						print(port_index1)
						print(module_index1)
						print(port_index2)
						print(module_index2)
						#Save the data
						Modules[module_index1].Connections[-1].from_port = port_index1
						Modules[module_index1].Connections[-1].to_module = module_index2
						Modules[module_index1].Connections[-1].to_port = port_index2
						Modules[module_index2].Connections[-1].from_port = port_index2
						Modules[module_index2].Connections[-1].to_module = module_index1
						Modules[module_index2].Connections[-1].to_port = port_index1

		i += 1

	f.close()
	




def print_all(Modules):
	#Imprimir por pantalla
	for module in Modules:
		print ("Name: %s " %(module.Name))
		print ("Number of Instance: %s " %(module.nInstance))
		print ("Master: %s " %(module.Master))
		for param in module.Parameters:
			print("Parameter name: %s " %(param.pa_name))
			print("Parameter value: %s " %(param.pa_value))
		for port in module.Ports:
			print("Port name: %s " %(port.po_name))
			print("Port direction: %s " %(port.po_direction))
			print("Port bits: %s " %(port.po_nbits))
			print("Port tag: %s " %(port.po_tag))
		print()

def print_modules(Modules):
	i = 0
	print("n.  Name  nInstance")
	for module in Modules:
		i += 1
		print("%s. %s %s" % (i, module.Name, module.nInstance))

def print_connections(Modules):
	for module in Modules:
		print ("From module: "+module.Name)
		for connection in module.Connections:
			print("		With port: "+module.Ports[connection.from_port].po_name)
			print("			To module: "+Modules[connection.to_module].Name)
			print("			With port: "+Modules[connection.to_module].Ports[connection.to_port].po_name)
		print()

def print_exterior_connections(connections):
	for connection in connections:
		print(connection.in_out_name)
		print(connection.to_module)
		print(connection.to_port)

def print_interconnections(interconnections):
	for connection in interconnections:
		print(connection.from_module)
		print(connection.from_port)
		print(connection.to_module)
		print(connection.to_port)

def print_ports(module):
	i = 0
	for port in module.Ports:
		i += 1
		print("%s. %s" % (i, port.po_name))

'''
		Modules_extended[-1].Name = Modules_extended[-1].Name + "_" + str(ninstances[-1] - 1)
		for param in Modules_extended[-1].Parameters:
			param.pa_name = param.pa_name + "_" + str(ninstances[-1] - 1)
		for port in Modules_extended[-1].Ports:
			port.po_name = port.po_name + "_" + str(ninstances[-1] - 1)
'''

def copy_module(module, Modules_extended):
	Modules_extended.append(Module())
	Modules_extended[-1].Name = module.Name
	Modules_extended[-1].Master = module.Master
	Modules_extended[-1].nInstance = module.nInstance
	for param in module.Parameters:
		Modules_extended[-1].Parameters.append(Parameters())
		Modules_extended[-1].Parameters[-1].pa_name = param.pa_name
		Modules_extended[-1].Parameters[-1].pa_value = param.pa_value
	for port in module.Ports:
		Modules_extended[-1].Ports.append(Ports())
		Modules_extended[-1].Ports[-1].po_name = port.po_name
		Modules_extended[-1].Ports[-1].po_direction = port.po_direction
		Modules_extended[-1].Ports[-1].po_nbits = port.po_nbits
		Modules_extended[-1].Ports[-1].po_tag = port.po_tag
	for connection in module.Connections:
		Modules_extended[-1].Connections.append(Connections())
		Modules_extended[-1].Connections[-1].from_port = connection.from_port
		Modules_extended[-1].Connections[-1].to_module = connection.to_module
		Modules_extended[-1].Connections[-1].to_port = connection.to_port

'''
>>> str1 = "mystring"
>>> list1 = list(str1)
>>> list1[5] = 'u'
>>> str1 = ''.join(list1)
>>> print(str1)
'''

def create_instance(Modules, num_module, ninstances, Modules_extended):
	for i in range(ninstances - 1):
		copy_module(Modules[num_module], Modules_extended)
		Modules_extended[-1].nInstance += (i + 1)
		for port in Modules_extended[-1].Ports:
			if port.po_tag:
				list1 = list(port.po_tag)
				list1[-1] = str(Modules_extended[-1].nInstance)
				port.po_tag = ''.join(list1)
			
			#port.po_tag[-1] = Modules_extended[-1].nInstance
		

def delete_connection(Modules, module, index):
	to_module = int(module.Connections[index].to_module)
	from_port = int(module.Connections[index].from_port)
	to_port = int(module.Connections[index].to_port)

	for modulex in Modules:
		if modulex.Name == Modules[to_module].Name:
			i = 0
			for connection in modulex.Connections:
				if connection.from_port == to_port and connection.to_port == from_port:
					modulex.Connections.pop(i)
					print("trobat")
					break
				i += 1

	#module.Connections.pop(index)

def write_param(module, f):
	i = 0
	if module.Parameters:   #If there is some parameter to write
		f.write("#(\n")
		for param in module.Parameters:
			if i+1 == len (module.Parameters):
				f.write("	.%s (%s)\n" %(param.pa_name, param.pa_value))
				break
			f.write("	.%s (%s),\n" %(param.pa_name, param.pa_value))
			i+=1
		f.write("	)\n")

def delete_doubled_interconnections(interconnections):
	i = 0
	index = 0
	for connection in interconnections:
		i+=1
		index = i
		for connection2 in interconnections[i:]:
			if connection.from_module == connection2.to_module and connection.from_port == connection2.to_port:
				if connection.to_module == connection2.from_module and connection.to_port == connection2.from_port:
					interconnections.pop(index)
					break
			index += 1






#interconnections is the list that stores the connections
def copy_interconnections(Modules, module, interconnections):
	
	for connection in module.Connections:
		interconnections.append(Connect())
		interconnections[-1].from_module = module.Name
		interconnections[-1].from_port = module.Ports[connection.from_port].po_name
		interconnections[-1].to_module = Modules[connection.to_module].Name
		interconnections[-1].to_port = Modules[connection.to_module].Ports[connection.to_port].po_name
		interconnections[-1].nBits = module.Ports[connection.from_port].po_nbits
		interconnections[-1].from_nInstance = module.nInstance
		interconnections[-1].to_nInstance = Modules[connection.to_module].nInstance


def find_signal_name(Modules, module, connection, interconnections):
	for interconnection in interconnections:
		if module.Name == interconnection.from_module:
			if module.Ports[connection.from_port].po_name == interconnection.from_port and Modules[connection.to_module].Name == interconnection.to_module:
				if Modules[connection.to_module].Ports[connection.to_port].po_name == interconnection.to_port:
					return interconnection.signal_name
		elif module.Name == interconnection.to_module:
			if module.Ports[connection.from_port].po_name == interconnection.to_port and Modules[connection.to_module].Name == interconnection.from_module:
				if Modules[connection.to_module].Ports[connection.to_port].po_name == interconnection.from_port:
					return interconnection.signal_name

	return ("")

def connect_them(module1, module2, module1index, module2index, port1index, port2index):
	module1.Connections.append(Connections())
	module1.Connections[-1].to_module = module2index
	module1.Connections[-1].to_port = port2index
	module1.Connections[-1].from_port = port1index

	module2.Connections.append(Connections())
	module2.Connections[-1].to_module = module1index
	module2.Connections[-1].to_port = port1index
	module2.Connections[-1].from_port = port2index

def make_manual_connection(Modules):
	print("Select a module: ")
	print_modules(Modules)
	module1index = int(input()) - 1
	print("Select a port: ")
	i = 1
	for port in Modules[module1index].Ports:
		print( "%s. %s" %(i, port.po_name))
		i+=1
	port1index = int(input()) - 1

	print("Select a module: ")
	print_modules(Modules)
	module2index = int(input()) - 1
	print("Select a port: ")
	i = 1
	for port in Modules[module2index].Ports:
		print( "%s. %s" %(i, port.po_name))
		i+=1
	port2index = int(input()) - 1

	connect_them(Modules[module1index], Modules[module2index], module1index, module2index, port1index, port2index)


def connect_toto_crossbar(Modules):
	found = False
	module1index = 0
	module2index = 0
	port1index = 0
	port2index = 0

	for module in Modules:
		if module.Name == "Crossbar" or module.Name == "crossbar":
			found = True
			crossbar = module
			break
		module2index += 1
	

	if found:
		for module in Modules:
			if module.Master is not None:
				for port in module.Ports:
					for c_port in crossbar.Ports:
						if port.po_tag and c_port.po_tag:
							if port.po_tag == c_port.po_tag:
								connect_them(module, crossbar, module1index, module2index, port1index, port2index)
						port2index += 1
					port2index = 0
					port1index += 1
			port1index = 0
			module1index += 1

	else:
		print("Crossbar not found, try naming it crossbar or crossbar.")

'''
for port in module.Ports:
					j = 0

					if module.Master == True:
						nMasters += 1
						master_name = port.po_name + "_m_"
						for c_port in crossbar.Ports:
							if master_name in c_port.po_name:
								m_portsIndex.append(i)
								c_portsIndex.append(j)
							j += 1
'''


def write_Verilog(Modules, Modules_extended):
	print("Name for the new module: ")
	new_name = input()
	inputs_names = []
	outputs_names = []

	########Header
	try:
		if not os.path.exists("IPs"):
			os.mkdir("IPs")
	except:
		print("Failed to create a directory.")
	f = open(os.path.join("IPs", new_name + ".txt"), "w")
	f.write("`timescale 10ns / 10ns\n\n")
	f.write("module %s( \n"%(new_name))


	if not Modules_extended:
		for module in Modules:
			copy_module(module, Modules_extended)

	exterior_connection = []
	#####INputs and OUTputs
	print("Does the module have any inputs? (yes/no)")
	answer = input()
	while answer == "yes":
		print("Name for the input: ")
		input_name = input()
		inputs_names.append(input_name)
		print("Number of bits? ")
		input_bits = int(input())
		if input_bits>1:
			f.write("input [%s:0] %s"%(input_bits - 1, input_name))
		else:
			f.write("input %s"%(input_name))

		print("Is this input connected to a port of a module? (yes/no)")
		answer = input()
		while answer == "yes":
			#Store the connection to be made.
			exterior_connection.append(Exterior_Connection())
			exterior_connection[-1].in_out_name = inputs_names[-1]
			print("Which module? ")
			print_modules(Modules_extended)
			index = int(input()) - 1
			exterior_connection[-1].to_module = index
			print("Which port? ")
			print_ports(Modules_extended[index])
			index = int(input()) - 1
			exterior_connection[-1].to_port = index
			print_exterior_connections(exterior_connection)
			print("Is it connected to other modules as well? (yes/no)")
			answer = input()

		print("Another input? (yes/no)")
		answer = input()
		if answer == "yes":
			f.write(",\n")
		

	print("Does the module have any outputs? (yes/no)")
	answer = input()
	if answer == "yes":
		f.write(",\n")
	else:
		f.write("\n")

	while answer == "yes":
		print("Name for the output: ")
		output_name = input()
		outputs_names.append(output_name)

		print("Number of bits? ")
		input_bits = int(input())

		if input_bits > 1:
			f.write("output [%s:0] %s"%(input_bits - 1, output_name))
		else:
			f.write("output %s"%(output_name))

		print("Is this input connected to a port of a module? (yes/no)")
		answer = input()
		while answer == "yes":
			#Store the connection to be made.
			exterior_connection.append(Exterior_Connection())
			exterior_connection[-1].in_out_name = outputs_names[-1]
			print("Which module? ")
			print_modules(Modules_extended)
			index = int(input()) - 1
			exterior_connection[-1].to_module = index
			print("Which port? ")
			print_ports(Modules_extended[index])
			index = int(input()) - 1
			exterior_connection[-1].to_port = index
			print_exterior_connections(exterior_connection)
			print("Is it connected to other modules as well? (yes/no)")
			answer = input()

		print("Another output? (yes/no)")
		answer = input()
		if answer == "yes":
			f.write(",\n")
		
	f.write("\n);\n\n")

	
		

	print("Do you wish to modify the value of a parameter? (yes/no)")
	answer = input()
	while answer == "yes":
		print("Possible modules: ") 
		print_modules(Modules_extended)

		module_index = int(input("Enter the number of the module you want to edit: ")) - 1

		print("Enter the number of the parameter you wish to modify:")
		print()
		print("n.  Name   Value")
		i = 0
		for param in Modules_extended[module_index].Parameters:
			i += 1
			print("%s.  %s  %s" %(i, param.pa_name, param.pa_value))
		param_index = int(input()) - 1
		new_value = int(input("New value for the parameter: "))
		Modules_extended[module_index].Parameters[param_index].pa_value = new_value

		print("Do you wish to modify the value of another parameter? (yes/no)")
		answer = input()

	nConnections = 0
	interconnections = []   ##Variable on s'emmagatzemen les connexions de forma més simple per a l'escriptura a HDL
	for module in Modules_extended:
		nConnections += len(module.Connections)
		copy_interconnections(Modules_extended, module, interconnections)

	nConnections /= 2
	delete_doubled_interconnections(interconnections)
	

	for connection in interconnections:
		connection.signal_name = "u_" + connection.from_module  + "_" + str(connection.from_nInstance) + "_" + connection.to_module + "_" + str(connection.to_nInstance) + "_" + connection.from_port + "_sig"
		f.write("wire ")
		if int(connection.nBits) > 1:
			f.write("[%s:0]" %(int(connection.nBits) - 1))
		f.write(" %s;\n" %(connection.signal_name))
		#delete_connection(Modules_extended, module, i)
	
	
	
	####Modules and instances
	for module in Modules_extended:
		written = False #Used to know wether we wrote the header of the IP or not
		if module.Connections:
			f.write("%s "%(module.Name))
			write_param(module, f)
			f.write("	u_%s_%s (\n" %(module.Name, module.nInstance))
			written = True

		for connection in exterior_connection:
			if not module.Connections and Modules_extended[connection.to_module] == module and not written:
				f.write("%s "%(module.Name))
				write_param(module, f)
				f.write("	u_%s_%s (\n" %(module.Name, module.nInstance))
				written = True
			elif Modules_extended[connection.to_module] == module:
				f.write("	.%s( %s ),\n" %(module.Ports[connection.to_port].po_name, connection.in_out_name))
				
		for i in range(len(module.Connections)):
			port_index = int(module.Connections[i].from_port)
			f.write("	.%s(" %(module.Ports[port_index].po_name))
			if (i + 1) == len(module.Connections):
				f.write(" %s )\n"%(find_signal_name(Modules_extended, module, module.Connections[i], interconnections)))
				f.write(");\n\n")
				break
			f.write(" %s ),\n"%(find_signal_name(Modules_extended, module, module.Connections[i], interconnections)))

	f.write("endmodule;")
	f.close()



def crossbar_handler(Modules, Modules_extended):

	print("Possible modules: ") 
	print_modules(Modules)
	print("Enter the number of the module you want to connect to crossbar: ")
	num_module = int(input()) - 1
	copy_module(Modules[num_module], Modules_extended)

	print("How many instances do you wish of this module? ")
	ninstances = int(input())
	if ninstances > 1:
		create_instance(Modules, num_module, ninstances, Modules_extended)

	print("Do you wish to connect another module? (yes/no)")
	answer = input()
	while answer == "yes":
		print("Possible modules: ") 
		print_modules(Modules)
		print("Enter the number of the module you want to connect to crossbar: ")
		num_module = int(input()) - 1
		copy_module(Modules[num_module], Modules_extended)
		print("How many instances do you wish of this module? ")
		ninstances = int(input())
		if ninstances > 1:
			create_instance(Modules, num_module, ninstances, Modules_extended)
		print("Do you wish to connect another module? (yes/no)")
		answer = input()

	print_all(Modules_extended)


def manual_connections_handler(Modules):
	print("Please select one of the options below. ")
	print("1. Connection between inputs/outputs and modules. ")
	print("2. Connection between modules. ")
	option = int(input())
	if option == 1:
		print("")
	elif option == 2:

		generate_component(Modules, 0, 0, 0, 0)

'''
def write_hdl(Modules):
	print("Name for the new module: ")
	new_name = input()

	inputs_names = []
	outputs_names = []

	try:
		if not os.path.exists("IPs"):
			os.mkdir("IPs")
	except:
		print("Failed to create a directory.")
	f = open(os.path.join("IPs", new_name + ".txt"), "w")
	f.write("`timescale 10ns / 10ns\n\n")
	f.write("module %s( \n"%(new_name))

	print("Does the module have any inputs? (yes/no)")
	answer = input()
	while answer == "yes":
		print("Name for the input: ")
		input_name = input()
		inputs_names.append(input_name)
		print("Number of bits? ")
		input_bits = int(input())
		if input_bits>1:
			f.write("input [%s:0] %s"%(input_bits - 1, input_name))
		else:
			f.write("input %s"%(input_name))
		print("Another input? (yes/no)")
		answer = input()
		if answer == "yes":
			f.write(",\n")
		

	print("Does the module have any outputs? (yes/no)")
	answer = input()
	if answer == "yes":
		f.write(",\n")
	else:
		f.write("\n")

	while answer == "yes":
		print("Name for the output: ")
		output_name = input()
		outputs_names.append(output_name)

		print("Number of bits? ")
		input_bits = int(input())

		if input_bits > 1:
			f.write("output [%s:0] %s"%(input_bits - 1, output_name))
		else:
			f.write("output %s"%(output_name))
		print("Another output? (yes/no)")
		answer = input()
		if answer == "yes":
			f.write(",\n")
		
	f.write("\n);\n\n")

	num_module = []
	ninstances = []
	#List that stores the instances as well as the modules
	Modules_extended = []

	#Menu
	print("Menu: ")
	print("1. Connect everything to crossbar, only 1 instance per module.")
	print("2. Make manual connections. ")
	print("3. Select instances/modules to connect to crossbar. ")
	print("4. Quit. ")
	x = int(input())
	while x != 4:
		if x == 1:
			#Connect everything to crossbar.
			f.close()
			connect_to_crossbar(Modules, new_name)
			print("Done.")
			print("")
		elif x == 2:
			#Make a manual connections.
			f.close()
			manual_connections_handler(Modules, inputs_names, outputs_names)
			print("Done.")
			print("")
		elif x == 3: 
			#Selective connection to crossbar.
			f.close()
			i = 0
			for module in Modules:
				if module.Name == "crossbar" or module.Name == "Crossbar":
					copy_module(module, Modules_extended)
					break
			crossbar_handler(Modules, Modules_extended)
			connect_to_crossbar(Modules_extended, new_name)
			print("Done.")
			print("")
		else:
			print("Wrong number. Try again.")



		print("Menu: ")
		print("1. Connect everything to crossbar.")
		print("2. Make manual connections. ")
		print("3. Select instances/modules to connect to crossbar. ")
		print("4. Quit. ")
		x = int(input())





	f.close()

#Creates a component to connect components
def generate_component(Modules, module_index1, module_index2, port_index1, port_index2):
	print("Name for the new module: ")
	new_name = input()

	#if path.exists("connections.txt"):
	#	os.remove("connections.txt")
	try:
		if not os.path.exists("IPs"):
			os.mkdir("IPs")
	except:
		print("Failed to create a directory.")
	f = open(os.path.join("IPs", new_name + ".txt"), "w")
	f.write("`timescale 10ns / 10ns\n\n")
	f.write("module %s;\n"%(new_name))
	f.write("\n")

	for i in range(0, len(module_index1)):
		f.write("wire u_%s_%s_sig;\n" %(Modules[module_index1[i]].Name, Modules[module_index1[i]].Ports[port_index1[i]].po_name))
	f.write("\n")

	f.write("%s u_%s (\n" %(Modules[module_index1[i]].Name, Modules[module_index1[i]].Name))
	for i in range(0, len(module_index1)):
		if (i+1) == len(module_index1):
			f.write("	.%s( u_%s_%s_sig )\n" %(Modules[module_index1[i]].Ports[port_index1[i]].po_name, Modules[module_index1[i]].Name, Modules[module_index1[i]].Ports[port_index1[i]].po_name))
			break
		f.write("	.%s( u_%s_%s_sig ),\n" %(Modules[module_index1[i]].Ports[port_index1[i]].po_name, Modules[module_index1[i]].Name, Modules[module_index1[i]].Ports[port_index1[i]].po_name))
	f.write("	);\n\n")

	f.write("%s u_%s (\n" %(Modules[module_index2[i]].Name, Modules[module_index2[i]].Name))
	for i in range(0, len(module_index1)):
		if (i+1) == len(module_index1):
			f.write("	.%s( u_%s_%s_sig )\n" %(Modules[module_index2[i]].Ports[port_index2[i]].po_name, Modules[module_index1[i]].Name, Modules[module_index2[i]].Ports[port_index2[i]].po_name))
			break
		f.write("	.%s( u_%s_%s_sig ),\n" %(Modules[module_index2[i]].Ports[port_index2[i]].po_name, Modules[module_index1[i]].Name, Modules[module_index2[i]].Ports[port_index2[i]].po_name))
	f.write("	);\n\n")
	f.write("endmodule;")
	f.close()
'''
def save_connection(Modules, module_index1, module_index2, port_index1, port_index2):

	Modules[module_index1].Connections.append(Connections())
	Modules[module_index1].Connections[-1].to_module = module_index2
	Modules[module_index1].Connections[-1].to_port = port_index2
	Modules[module_index1].Connections[-1].from_port = port_index1

	Modules[module_index2].Connections.append(Connections())
	Modules[module_index2].Connections[-1].to_module = module_index1
	Modules[module_index2].Connections[-1].to_port = port_index1
	Modules[module_index2].Connections[-1].from_port = port_index2
'''
#Function that reads from the user what modules and ports he wishes to connect
def connect_modules(Modules, module_index1, module_index2, port_index1, port_index2):
	x = "yes"
	while x == "yes":
		os.system('cls' if os.name == 'nt' else 'clear')

		print("Possible modules: ") 
		print_modules(Modules)

		print("Enter the number of the module you want to connect: ")
		module_index1.append((int(input()) - 1))
		print("Enter the number of the second module you want to connect: ")
		module_index2.append((int(input()) - 1))

		print("Enter the port from %s you want to connect: " % (Modules[module_index1[-1]].Name))
		print("Possible ports(name, direction): ")
		for i in range(0, Modules[module_index1[-1]].nPorts + 1):
			print("%s. %s %s " %((i + 1), Modules[module_index1[-1]].Ports[i].po_name, Modules[module_index1[-1]].Ports[i].po_direction))
		port_index1.append((int(input()) - 1))

		print("Enter the port from %s you want to connect: " % (Modules[module_index2[-1]].Name))
		print("Possible ports(name, direction): ")
		for i in range(0, Modules[module_index2[-1]].nPorts + 1):
			print("%s. %s %s " %((i + 1), Modules[module_index2[-1]].Ports[i].po_name, Modules[module_index2[-1]].Ports[i].po_direction))
		port_index2.append((int(input()) - 1))
		
		try:
			save_connection(Modules, module_index1[-1], module_index2[-1], port_index1[-1], port_index2[-1])
		
		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments:\n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print (message)

		print("Do you wish to make another connection? (yes/no)")
		x = input()


	generate_component(Modules, module_index1, module_index2, port_index1, port_index2)





def connect_module_to_crossbar(module, crossbar, m_portsIndex, c_portsIndex, new_name, first, nMasters, nSlaves):
	i = 0

	#if path.exists("connections.txt"):
	#	os.remove("connections.txt")
	try:
		if not os.path.exists("IPs"):
			os.mkdir("IPs")
	except:
		print("Failed to create a directory.")

	extension = ""
	if module.Master:
		extension = "m_"
	else:
		extension = "s_"

	if first == True:
		f = open(os.path.join("IPs", new_name + ".txt"), "a")

		for i in range(0, len(c_portsIndex)):
			if int(crossbar.Ports[c_portsIndex[i]].po_nbits) > 1:
				f.write("wire [%s:0] %s_sig;\n" %(int(crossbar.Ports[c_portsIndex[i]].po_nbits) - 1, crossbar.Ports[c_portsIndex[i]].po_name))
			else:
				f.write("wire %s_sig;\n" %(crossbar.Ports[c_portsIndex[i]].po_name))
		f.write("\n")
		
		#for i in range(0, len(module_index1)):
		#	f.write("wire u_%s_%s_sig;\n" %(Modules[module_index1[i]].Name, Modules[module_index1[i]].Ports[port_index1[i]].po_name))
		#f.write("\n")
		
		f.write("%s " %(crossbar.Name))
		write_param(crossbar, f)
		f.write("	u_%s (\n" %(crossbar.Name))
		for i in range(0, len(c_portsIndex)):							#for each port found in connect_to_crossbar write the VHDL code
			if (i+1) == len(c_portsIndex):
				f.write("	.%s( %s_sig )\n" %(crossbar.Ports[c_portsIndex[i]].po_name, crossbar.Ports[c_portsIndex[i]].po_name ))
				break
			f.write("	.%s( %s_sig ),\n" %(crossbar.Ports[c_portsIndex[i]].po_name, crossbar.Ports[c_portsIndex[i]].po_name))
		f.write("	);\n\n")
		
		f.write("%s "%(module.Name))
		write_param(module, f)
		f.write("	u_%s_%s (\n" %(module.Name, module.nInstance))
		for i in range(0, len(m_portsIndex)):
			if (i+1) == len(m_portsIndex):
				f.write("	.%s( %s_sig )\n" %(module.Ports[m_portsIndex[i]].po_name, crossbar.Ports[c_portsIndex[i]].po_name))
				break
			f.write("	.%s( %s_sig ),\n" %(module.Ports[m_portsIndex[i]].po_name, crossbar.Ports[c_portsIndex[i]].po_name))


	else:
		f = open(os.path.join("IPs", new_name + ".txt"), "r")
		lines = f.readlines()
		f.close()

		j = 0
		found = False
		while j < len(lines) and found == False:
			j+=1
			line = lines[j]
			if "wire" in line:
				found = True

		for i in range(0, len(c_portsIndex)):
			if int(crossbar.Ports[c_portsIndex[i]].po_nbits) > 1:
				lines.insert(j,"wire [%s:0] %s_sig;\n" %(int(crossbar.Ports[c_portsIndex[i]].po_nbits) - 1,crossbar.Ports[c_portsIndex[i]].po_name))
			else:
				lines.insert(j,"wire %s_sig;\n" %(crossbar.Ports[c_portsIndex[i]].po_name))
		
		# Need to find the line to append to in module crossbar
		j = 0
		found=False
		secondfound = False
		while j < len(lines) and secondfound == False:
			j+=1
			line = lines[j]
			if ");" in line and found == True:
				secondfound = True
			if ");" in line:
				found = True
			


		for i in range(0, len(c_portsIndex)):							#for each port found in connect_to_crossbar write the VHDL code
			#if (i+1) == len(c_portsIndex):
			#	lines.insert(j, "	.%s( %s_sig )\n" %(crossbar.Ports[c_portsIndex[i]].po_name, crossbar.Ports[c_portsIndex[i]].po_name ))
			#	j+=1
			#	break
			lines.insert(j, "	.%s( %s_sig ),\n" %(crossbar.Ports[c_portsIndex[i]].po_name, crossbar.Ports[c_portsIndex[i]].po_name))
			j+=1

		
		f = open(os.path.join("IPs", new_name + ".txt"), "w")
		lines = "".join(lines)
		f.write(lines)
		f.close()
		
		f = open(os.path.join("IPs", new_name + ".txt"), "a")
		f.write("%s "%(module.Name))
		write_param(module, f)
		f.write("	u_%s_%s (\n" %(module.Name, module.nInstance))
		for i in range(0, len(m_portsIndex)):
			if (i+1) == len(m_portsIndex):
				f.write("	.%s( %s_sig )\n" %(module.Ports[m_portsIndex[i]].po_name, crossbar.Ports[c_portsIndex[i]].po_name))
				break
			f.write("	.%s( %s_sig ),\n" %(module.Ports[m_portsIndex[i]].po_name, crossbar.Ports[c_portsIndex[i]].po_name))
	f.write("	);\n\n")
	f.close()

def connect_to_crossbar(Modules, new_name):
	found = False
	first = True
	nMasters = 0
	nSlaves = 0
	
	for module in Modules:
		if module.Name == "Crossbar" or module.Name == "crossbar":
			found = True
			crossbar = module


	if found:
		for module in Modules:
			if module.Master is not None: 			#Modules that shouldn't connect to crossbar are None, like crossbar itself
				i = 0
				m_portsIndex = []
				c_portsIndex = []
				for port in module.Ports:
					j = 0

					if module.Master == True:
						nMasters += 1
						master_name = port.po_name + "_m_"
						for c_port in crossbar.Ports:
							if master_name in c_port.po_name:
								m_portsIndex.append(i)
								c_portsIndex.append(j)
							j += 1
						
					else:
						nSlaves += 1
						slave_name = port.po_name + "_s_"
						for c_port in crossbar.Ports:
							if slave_name in c_port.po_name:
								m_portsIndex.append(i)
								c_portsIndex.append(j)
							j += 1
					i += 1
				
				connect_module_to_crossbar(module, crossbar, m_portsIndex, c_portsIndex, new_name, first, nMasters, nSlaves)
				first = False

		f = open(os.path.join("IPs", new_name + ".txt"), "a")
		f.write("endmodule;")
		f.close()

	else:
		print("Crossbar not found. Try naming it 'crossbar'.")

def edit_module(Modules):
	os.system('cls' if os.name == 'nt' else 'clear')
	print("What do you wish to edit?")
	print("1. Parameters values.")
	print("2. Add ports in a module.")
	print("3. Delete ports from a module.")
	x = input()

	print("Possible modules: ") 
	print_modules(Modules)

	module_index = int(input("Enter the number of the module you want to edit: ")) - 1
	os.system('cls' if os.name == 'nt' else 'clear')
	if x == "1":
		print("Enter the number of the parameter you wish to modify:")
		print()
		print("n.  Name   Value")
		i = 0
		for param in Modules[module_index].Parameters:
			i += 1
			print("%s.  %s  %s" %(i, param.pa_name, param.pa_value))
		param_index = int(input()) - 1
		new_value = int(input("New value for the parameter: "))
		Modules[module_index].Parameters[param_index].pa_value = new_value

	if x == "2":
		new_name = input("Enter the name of the new port: ")
		new_direction = input("Enter the direction of the port: ")
		Modules[module_index].Ports.append(Ports())
		Modules[module_index].Ports[-1].po_name = new_name
		Modules[module_index].Ports[-1].po_direction = new_direction

	if x == "3":
		i = 0
		print("n.   Name    Direction")
		for port in Modules[module_index].Ports:
			i += 1
			print("%s.  %s  %s" %(i, port.po_name, port.po_direction))
		port_index = int(input("Enter the number of the port you wish to delete: ")) - 1
		del Modules[module_index].Ports[port_index]

<?xml version="1.0" encoding="UTF-8"?>
<ipxact:design xmlns:ipxact="http://www.accellera.org/XMLSchema/IPXACT/1685-2014" xmlns:xsi="http://
www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.accellera.org/XMLSchema/
IPXACT/1685-2014 http://www.accellera.org/XMLSchema/IPXACT/1685-2014/index.xsd">
 <ipxact:vendor>accellera.org</ipxact:vendor>
 <ipxact:library>i2s</ipxact:library>
 <ipxact:name>transmitter_is_master_rtl</ipxact:name>
 <ipxact:version>1.0</ipxact:version>
 <ipxact:componentInstances>
 <ipxact:componentInstance>
 <ipxact:instanceName>u_master_transmitter</ipxact:instanceName>
 <ipxact:componentRef vendor="accellera.org" library="i2s" name="master_transmitter"
 version="1.0"/>
 </ipxact:componentInstance>
 <ipxact:componentInstance>
 <ipxact:instanceName>u_slave_receiver</ipxact:instanceName>
 <ipxact:componentRef vendor="accellera.org" library="i2s" name="slave_receiver" version="1.0"/>
 </ipxact:componentInstance>
 </ipxact:componentInstances>
 <ipxact:adHocConnections>
 <ipxact:adHocConnection>
 <ipxact:name>u_master_transmitter_sck_u_slave_receiver_sck</ipxact:name>
 <ipxact:portReferences>
 <ipxact:internalPortReference componentRef="u_master_transmitter" portRef="sck"/>
 <ipxact:internalPortReference componentRef="u_slave_receiver" portRef="sck"/>
 </ipxact:portReferences>
 </ipxact:adHocConnection>
 <ipxact:adHocConnection>
 <ipxact:name>u_master_transmitter_ws_u_slave_receiver_ws</ipxact:name>
 <ipxact:portReferences>
 <ipxact:internalPortReference componentRef="u_master_transmitter" portRef="ws"/>
 <ipxact:internalPortReference componentRef="u_slave_receiver" portRef="ws"/>
 </ipxact:portReferences>
 </ipxact:adHocConnection>
 <ipxact:adHocConnection>
 <ipxact:name>u_master_transmitter_sd_u_slave_receiver_sd</ipxact:name>
 <ipxact:portReferences>
 <ipxact:internalPortReference componentRef="u_master_transmitter" portRef="sd"/>
 <ipxact:internalPortReference componentRef="u_slave_receiver" portRef="sd"/>
 </ipxact:portReferences>
 </ipxact:adHocConnection>
 </ipxact:adHocConnections>
</ipxact:design>
'''

def save(Modules):
	try:
		if not os.path.exists("Connections"):
			os.mkdir("Connections")
	except:
		print("Failed to create a directory.")

	module_index1 = []
	module_index2 = []
	port_index1 = []
	port_index2 = []
	i = 0
	j = 0
	
	print("Give a name to the XML file to save. ")
	new_name = input()

	if not os.path.isfile(os.path.join("Connections", new_name + ".txt")):
		f = open(os.path.join("Connections", new_name + ".txt"), "w")
		f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		f.write('<ipxact:design xmlns:ipxact="http://www.accellera.org/XMLSchema/IPXACT/1685-2014" xmlns:xsi="http://\n')
		f.write('www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.accellera.org/XMLSchema/\n')
		f.write('IPXACT/1685-2014 http://www.accellera.org/XMLSchema/IPXACT/1685-2014/index.xsd">\n')
		f.write(' <ipxact:vendor>accellera.org</ipxact:vendor>\n')
		f.write(' <ipxact:library>i2s</ipxact:library>\n')
		f.write(' <ipxact:name>transmitter_is_master_rtl</ipxact:name>\n')
		f.write(' <ipxact:name>transmitter_is_master_rtl</ipxact:name>\n')
		f.write(' <ipxact:version>1.0</ipxact:version>\n')
		f.write(' <ipxact:componentInstances>\n')
		
		for module in Modules:
			if module.Connections:    ##List not empty
				f.write(' <ipxact:componentInstance>\n')
				f.write(' <ipxact:instanceName>u_'+module.Name+'</ipxact:instanceName>\n')
				f.write(' <ipxact:componentRef vendor="accellera.org" library="i2s" name="master_transmitter"\n')
				f.write(' version="1.0"/>\n')
				f.write(' </ipxact:componentInstance>\n')
		
		f.write(' </ipxact:componentInstances>\n')
		f.write(' <ipxact:adHocConnections>\n')
		for module in Modules:
			if module.Connections:
				module_index1.append(i)
				i += 1
				for connection in module.Connections:
					if not (connection.to_module < module_index1[-1]):
						f.write(' <ipxact:adHocConnection>\n')
						f.write(' <ipxact:name>u_'+module.Name+'_'+module.Ports[connection.from_port].po_name+'_u_'+Modules[connection.to_module].Name+'_'+Modules[connection.to_module].Ports[connection.to_port].po_name+'</ipxact:name>\n')
						f.write(' <ipxact:portReferences>\n')
						f.write(' <ipxact:internalPortReference componentRef="u_'+module.Name+'" portRef="'+module.Ports[connection.from_port].po_name+'"/>\n')
						f.write(' <ipxact:internalPortReference componentRef="u_'+Modules[connection.to_module].Name+'" portRef="'+Modules[connection.to_module].Ports[connection.to_port].po_name+'"/>\n')
						f.write(' </ipxact:portReferences>\n')
						f.write(' </ipxact:adHocConnection>\n')
		f.write(' </ipxact:adHocConnections>\n')



		

##   Main   ##

Modules = [] #List where the modules will be stored
Modules_extended = [] #For programming purposes
while(True):
	os.system('cls' if os.name == 'nt' else 'clear')
	print("Menu: ")
	print("1. Read all modules in directory XML.")
	print("2. Write Verilog")
	print("3. Read connections.")
	print("4. Print Connections. ")
	print("5. Save connections made. ")
	print("6. Print all modules. ")
	print("7. Connect to crossbar. ")
	print("8. Make manual connection. ")
	print("9. Create instance. ")
	print()
	print("Choose the number of the option you want to do.")
	x = input()

	if x == "1":
		try:
			read(Modules)
			print("Done. ")

			print()
			print_all(Modules)
			print()
		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments:\n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print (message)



	elif x == "2":
		if Modules:
			try:
				write_Verilog(Modules, Modules_extended)
			except Exception as ex:
				template = "An exception of type {0} occurred. Arguments:\n{1!r}"
				message = template.format(type(ex).__name__, ex.args)
				print (message)
		else:
			print("No modules to write.")

	elif x == "3":
		print("What's the name of the file you want to read from? (Without the extension (example: my_file))")
		file_name = input()
		try:
			read_connections(file_name, Modules)
			#for module in Modules:
			#	for connection in Connections:
			#		print(connection.from_port)
			#		print(connection.to_port)
			#		print(connection.to_module)
		except Exception as ex:
			print("Error. ")
			template = "An exception of type {0} occurred. Arguments:\n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print (message)
		except:
			print("Error!!!")

	elif x == "4":
		try:
			if Modules_extended:
				print_connections(Modules_extended)
			else:
				print_connections(Modules)
			
		except Exception as ex:
			print("Error. ")
			template = "An exception of type {0} occurred. Arguments:\n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print (message)
		except:
			print("Error!!!")
	
	elif x == "5":
		try:
			save(Modules)
		
		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments:\n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print (message)

	elif x == "6":
		print()
		if Modules_extended:
			print_all(Modules_extended)
		else:
				print_all(Modules)
		print()

	elif x == "7":
		try:
			if Modules_extended:
				connect_toto_crossbar(Modules_extended)
			else:
				connect_toto_crossbar(Modules)

		except Exception as ex:
			print("Error. ")
			template = "An exception of type {0} occurred. Arguments:\n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print (message)
		except:
			print("Error!!!")

	elif x == "8":
		try:
			if Modules_extended:
				make_manual_connection(Modules_extended)
			else:
				make_manual_connection(Modules)
		except Exception as ex:
			print("Error. ")
			template = "An exception of type {0} occurred. Arguments:\n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print (message)
		except:
			print("Error!!!")

	elif x == "9":
		try:
			answer = "yes"
			for module in Modules:
				copy_module(module, Modules_extended)
			print_all(Modules_extended)

			while answer == "yes":
				print("Possible modules: ") 
				print_modules(Modules)

				module_index = int(input("Enter the number of the module you want to create an instance: ")) - 1
				ninstances = int(input("How many instances? "))
				create_instance(Modules, module_index, ninstances, Modules_extended)

				print("Do you wish to create another instance? (yes/no)")
				answer = input()
			os.system('cls' if os.name == 'nt' else 'clear')
			print_all(Modules_extended)
			
		except Exception as ex:
			print("Error. ")
			template = "An exception of type {0} occurred. Arguments:\n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print (message)
		except:
			print("Error!!!")
	else:
		break

	print()
	print("Done.")
	print()
	print("Press any key to continue.")
	msvcrt.getch()
