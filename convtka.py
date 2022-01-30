import xml.etree.ElementTree as ET
import pandas as pd
import argparse
import sys




parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="Muestra información del script", action="store_true")
parser.add_argument("-input","--fichero_input", help="nombre del fichero de entrada")
parser.add_argument("-output", "--fichero_output", help="nombre del fichero de salida")
args = parser.parse_args()
if args.verbose:
    print ("Este script convierte espectros LYNX a TKA")
if args.fichero_input:
    print ("Fichero de entrada:"+args.fichero_input)   
if args.fichero_output:
    print ("Fichero de salida:"+args.fichero_output)

if ( not args.fichero_input and not args.fichero_output):
    print("Debe definir el fichero de entrada y salida")
    sys.exit()

mytree = ET.parse(args.fichero_input)
myroot = mytree.getroot()

data=[]

espectro_atributos = str(myroot[220].attrib)

ilive = espectro_atributos.find("elapsed_live")
ireal = espectro_atributos.find("elapsed_real")
icomp = espectro_atributos.find("elapsed_comp_cnts")
live_time = espectro_atributos[ireal+16:ilive-4]
real_time = espectro_atributos[ilive+16:icomp-4]
channels_atributos = str(myroot[74].attrib)
ichannels = channels_atributos.find("value")
channels = (channels_atributos[ichannels+9:ichannels+13])

x = myroot[220].text
data.append(x.split(","))
df = pd.DataFrame(data).T  # Create DataFrame and transpose it

for row in df:
    df[row] = df[row].astype(int)

my_file = open(args.fichero_output, "w")
my_file.write(real_time+"\n")
my_file.write(live_time+"\n")


c = 0
while c < int(channels):
    my_file.write(str(df[0][c])+"\n")
    c+=1

print("Conversión realizada")
my_file.close()

#print (df.dtypes)
#df.plot(kind='bar');
#df.to_csv(r'C:/pyconv/coreoutput.csv', index = False)
#plt.show()
