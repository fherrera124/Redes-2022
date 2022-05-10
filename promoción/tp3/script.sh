#!/bin/bash

echo "Ingrese nombres de dominio, separados por espacio"
read list
clear
echo -e "RESULTADOS.\n"

for i in $list; do
	echo "- domain name:"
    echo "    * $i"
    echo "- ipv4:"
    echo "$(dig +short -t a $i | sed 's/^/    * /')"
    echo "- ipv6:"
    echo "$(dig +short -t aaaa $i | sed 's/^/    * /')"
    echo "-------"
done
