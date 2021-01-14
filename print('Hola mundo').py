import re
import os
from os import path
import msvcrt
import glob

class Ports:
	def __init__(self):
		self.po_name = ""
		self.po_direction = ""
		self.po_nbits = ""

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
		self.Master = None
		self.Ports = []
		self.Parameters = []
		self.Connections = []


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
									Modules[-1].Parameters[Modules[-1].nParameters].pa_value = param_values[-1].group(1)
						if "<ipxact:classType>" in line:     														#Invented parameter from the IP-XACT protocol
							p = re.compile("<ipxact:classType>(.*)</ipxact:classType>")
							classType = p.search(line)
							if classType.group(1) == "Master" or classType.group(1) == "master":
								Modules[-1].Master = True
							else:
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
		print (module.Name)
		print (module.Master)
		for param in module.Parameters:
			print(param.pa_name)
			print(param.pa_value)
		for port in module.Ports:
			print(port.po_name)
			print(port.po_direction)
		print()

def print_modules(Modules):
	i = 0
	for module in Modules:
		i += 1
		print("%s. %s" % (i, module.Name))

def print_connections(Modules):
	for module in Modules:
		print ("From module: "+module.Name)
		for connection in module.Connections:
			print("		With port: "+module.Ports[connection.from_port].po_name)
			print("		To module: "+Modules[connection.to_module].Name)
			print("		With port: "+Modules[connection.to_module].Ports[connection.to_port].po_name)
		print()

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

def save_connection(Modules, module_index1, module_index2, port_index1, port_index2):

	Modules[module_index1].Connections.append(Connections())
	Modules[module_index1].Connections[-1].to_module = module_index2
	Modules[module_index1].Connections[-1].to_port = port_index2
	Modules[module_index1].Connections[-1].from_port = port_index1

	Modules[module_index2].Connections.append(Connections())
	Modules[module_index2].Connections[-1].to_module = module_index1
	Modules[module_index2].Connections[-1].to_port = port_index1
	Modules[module_index2].Connections[-1].from_port = port_index2

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


def write_param(module, f):
	i = 0
	if module.nParameters > -1:   #If there is some parameter to write
		f.write("#(\n")
		for param in module.Parameters:
			if i+1 == len (module.Parameters):
				f.write("	.%s (%s)\n" %(param.pa_name, param.pa_value))
				break
			f.write("	.%s (%s),\n" %(param.pa_name, param.pa_value))
			i+=1
		f.write("	)\n")


def connect_module_to_crossbar(module, crossbar, m_portsIndex, c_portsIndex, new_name):
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

	if not os.path.isfile(os.path.join("IPs", new_name + ".txt")):
		f = open(os.path.join("IPs", new_name + ".txt"), "w")
		f.write("`timescale 10ns / 10ns\n\n")
		f.write("module %s;\n"%(new_name))
		f.write("\n")


		#for i in range(0, len(portsIndex)):
		#	f.write("wire %s_sig;\n" %(module.Ports[m_portsIndex[i]].po_name))
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
		f.write("	u_%s (\n" %(module.Name))
		for i in range(0, len(m_portsIndex)):
			if (i+1) == len(m_portsIndex):
				f.write("	.%s( %s_sig )\n" %(module.Ports[m_portsIndex[i]].po_name, crossbar.Ports[c_portsIndex[i]].po_name))
				break
			f.write("	.%s( %s_sig ),\n" %(module.Ports[m_portsIndex[i]].po_name, crossbar.Ports[c_portsIndex[i]].po_name))


	else:
		f = open(os.path.join("IPs", new_name + ".txt"), "r")
		lines = f.readlines()
		f.close()
		
		# Need to find the line to append to in module crossbar
		j = 0
		found=False
		while j < len(lines) and found == False:
			j+=1
			line = lines[j]
			if ");" in line:
				found = True


		for i in range(0, len(c_portsIndex)):							#for each port found in connect_to_crossbar write the VHDL code
			#if (i+1) == len(c_portsIndex):
			#	lines.insert(j, "	.%s( %s_sig )\n" %(crossbar.Ports[c_portsIndex[i]].po_name, crossbar.Ports[c_portsIndex[i]].po_name ))
			#	j+=1
			#	break
			lines.insert(j-1, "	.%s( %s_sig ),\n" %(crossbar.Ports[c_portsIndex[i]].po_name, crossbar.Ports[c_portsIndex[i]].po_name))
			j+=1

		
		f = open(os.path.join("IPs", new_name + ".txt"), "w")
		lines = "".join(lines)
		f.write(lines)
		f.close()
		
		f = open(os.path.join("IPs", new_name + ".txt"), "a")
		f.write("%s "%(module.Name))
		write_param(module, f)
		f.write("	u_%s (\n" %(module.Name))
		for i in range(0, len(m_portsIndex)):
			if (i+1) == len(m_portsIndex):
				f.write("	.%s( %s_sig )\n" %(module.Ports[m_portsIndex[i]].po_name, crossbar.Ports[c_portsIndex[i]].po_name))
				break
			f.write("	.%s( %s_sig ),\n" %(module.Ports[m_portsIndex[i]].po_name, crossbar.Ports[c_portsIndex[i]].po_name))
	f.write("	);\n\n")
	f.close()

def connect_to_crossbar(Modules):
	found = False
	
	for module in Modules:
		if module.Name == "Crossbar" or module.Name == "crossbar":
			found = True
			crossbar = module


	if found:
		print("Do you wish to connect all modules to crossbar? (yes/no)")
		x = input()
		if x == "yes":
			print("Name for the new module: ")
			new_name = input()
			for module in Modules:
				if module.Master is not None: 			#Modules that shouldn't connect are None, like crossbar
					i = 0
					m_portsIndex = []
					c_portsIndex = []
					for port in module.Ports:
						j = 0

						if module.Master == True:
							master_name = port.po_name + "_m_"
							for c_port in crossbar.Ports:
								if master_name in c_port.po_name:
									m_portsIndex.append(i)
									c_portsIndex.append(j)
								j += 1
						
						else:
							slave_name = port.po_name + "_s_"
							for c_port in crossbar.Ports:
								if slave_name in c_port.po_name:
									m_portsIndex.append(i)
									c_portsIndex.append(j)
								j += 1
						i += 1
					
					connect_module_to_crossbar(module, crossbar, m_portsIndex, c_portsIndex, new_name) 

			f = open(os.path.join("IPs", new_name + ".txt"), "a")
			f.write("endmodule;")
			f.close()

		else: 
			print("Which modules do you want to connect? ")
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
'''
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
	

	if not os.path.isfile(os.path.join("Connections", "save" + ".txt")):
		f = open(os.path.join("Connections", "save" + ".txt"), "w")
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
while(True):
	os.system('cls' if os.name == 'nt' else 'clear')
	print("Menu: ")
	print("1. Read all modules in directory XML.")
	print("2. Connect modules.")
	print("3. Edit a module.")
	print("4. Read connections.")
	print("5. Connect modules to crossbar.")
	print("6. Print Connections. ")
	print("7. Save connections made. ")
	print("8. Print all modules. ")
	print("9. Exit. ")
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
		except:
			print("Couldn't read the file.")


	elif x == "2":
		if Modules:
			connect_modules(Modules, [], [], [], [])
		else:
			print("No modules to connect.")

	elif x == "3":
		if Modules:
			edit_module(Modules)
		else:
			print("No modules to edit.")

	elif x == "4":
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

	elif x == "5":
		try:	
			connect_to_crossbar(Modules)
		except:
			print("Failed to connect to crossbar. ")

	elif x == "6":
		print_connections(Modules)
	
	elif x == "7":
		try:
			save(Modules)
		
		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments:\n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print (message)
	elif x == "8":
		print()
		print_all(Modules)
		print()

	else:
		break

	print("Press any key to continue.")
	msvcrt.getch()


'''
	print()
	print_all(Modules)
	print()
'''


#		for module in Modules:
#			print(module.Name)
#			for i in range(0, module.nParameters + 1):
#				print(module.Parameters[i].pa_name)
#				print(module.Parameters[i].pa_value)
#			for i in range(0, module.nPorts + 1):
#				print(module.Ports[i].po_name)
#				print(module.Ports[i].po_direction)