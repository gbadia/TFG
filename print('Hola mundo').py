import re
import os
from os import path
import msvcrt



class Ports:
	def __init__(self):
		self.po_name = ""
		self.po_direction = ""

class Parameters:
	def __init__ (self):
		self.pa_name = ""
		self.pa_value = 0


class Module:
	
	Parameters = []
	def __init__(self):
		self.Name = ""
		self.nParameters = -1  #For programming purposes
		self.nPorts = -1
		self.Ports = []
		self.Parameters = []

#Reads a file and stores the relevant data in Modules
def read(file_name):
	f = open(file_name, "r")
	lines = f.readlines()

	#Temporary data storage
	Modules = []
	nModules = -1
	port_names = []
	port_directions = []
	param_names = []
	param_values = []
	i = 0
	prova = False
	#Data acquisition
	while i < len(lines):
		line = lines[i]
		if "<ipxact:moduleName>" in line:
			Modules.append(Module())
			nModules += 1
			p = re.compile("<ipxact:moduleName>(.*)</ipxact:moduleName>")
			name = p.search(line)
			Modules[nModules].Name = name.group(1)

			while "</ipxact:componentInstantiation>" not in line:
				
				if "<ipxact:moduleParameter " in line:
					Modules[nModules].nParameters += 1
					Modules[nModules].Parameters.append(Parameters())
					while "</ipxact:moduleParameter>" not in line:
						i += 1
						line = lines[i]
						if "<ipxact:moduleParameter " in line:
							Modules[nModules].nParameters += 1
							Modules[nModules].Parameters.append(Parameters())
						if "<ipxact:name>" in line:
							p = re.compile("<ipxact:name>(.*)</ipxact:name>")
							param_names.append(p.search(line))
							Modules[nModules].Parameters[Modules[nModules].nParameters].pa_name = param_names[-1].group(1)						
						if "<ipxact:value>" in line:
							p = re.compile("<ipxact:value>(.*)</ipxact:value>")
							param_values.append(p.search(line))
							Modules[nModules].Parameters[Modules[nModules].nParameters].pa_value = param_values[-1].group(1)
							
				i += 1
				line = lines[i]

						
		if "<ipxact:port>" in line:
			Modules[nModules].nPorts += 1
			Modules[nModules].Ports.append(Ports())

			while "</ipxact:ports>" not in line:
				i += 1
				line = lines[i]

				if "<ipxact:port>" in line:
					Modules[nModules].nPorts += 1
					Modules[nModules].Ports.append(Ports())
				if "<ipxact:name>" in line:
					p = re.compile("<ipxact:name>(.*)</ipxact:name>")
					port_names.append(p.search(line))
					Modules[nModules].Ports[Modules[nModules].nPorts].po_name = port_names[-1].group(1)

				if "<ipxact:direction>" in line:
					p = re.compile("<ipxact:direction>(.*)</ipxact:direction>")
					port_directions.append(p.search(line))
					Modules[nModules].Ports[Modules[nModules].nPorts].po_direction = port_directions[-1].group(1)
					
		i += 1	
	f.close()
	return Modules

#Creates a component to connect components
def generate_component(Modules, module_index1, module_index2, port_index1, port_index2):
	print("Name for the new component: ")
	new_name = input()
	#if path.exists("connections.txt"):
	#	os.remove("connections.txt")
	f = open("connections.txt", "w")
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
			f.write("	.%s( u_%s_%s_sig )\n" %(Modules[module_index2[i]].Ports[port_index2[i]].po_name, Modules[module_index2[i]].Name, Modules[module_index2[i]].Ports[port_index2[i]].po_name))
			break
		f.write("	.%s( u_%s_%s_sig ),\n" %(Modules[module_index2[i]].Ports[port_index2[i]].po_name, Modules[module_index2[i]].Name, Modules[module_index2[i]].Ports[port_index2[i]].po_name))
	f.write("	);\n\n")
	f.close()



#Function that reads from the user what modules and ports he wishes to connect
def connect_modules(Modules, module_index1, module_index2, port_index1, port_index2):
	x = "yes"
	while x == "yes":
		os.system('cls' if os.name == 'nt' else 'clear')

		print("Possible modules: ") 
		i = 0
		for module in Modules:
			i += 1
			print("%s. %s" % (i, module.Name))

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

		print("Do you wish to make another connection? (yes/no)")
		x = input()


	generate_component(Modules, module_index1, module_index2, port_index1, port_index2)






Modules = [] #List where the modules will be stored
while(True):
	os.system('cls' if os.name == 'nt' else 'clear')
	print("Menu: ")
	print("1. Read modules")
	print("2. Connect modules.")
	print("3. Exit. ")
	print()
	print("Choose the number of the option you want to do.")
	x = input()
	if x == "1":
		Modules = read("XML_exemple1.txt")
		print("Done. ")
		#Imprimir por pantalla
		for module in Modules:
			print (module.Name)
			for param in module.Parameters:
				print(param.pa_name)
				print(param.pa_value)
			for port in module.Ports:
				print(port.po_name)
				print(port.po_direction)
		print()
		print("Press any key to continue.")
		msvcrt.getch()
	elif x == "2":
		if Modules:
			connect_modules(Modules, [], [], [], [])
	elif x == "3":
		break



#		for module in Modules:
#			print(module.Name)
#			for i in range(0, module.nParameters + 1):
#				print(module.Parameters[i].pa_name)
#				print(module.Parameters[i].pa_value)
#			for i in range(0, module.nPorts + 1):
#				print(module.Ports[i].po_name)
#				print(module.Ports[i].po_direction)