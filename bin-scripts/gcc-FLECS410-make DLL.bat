# This script compiles the flecs library into a DLL using GCC.
# à exécuter dans le dossier racine du projet flecs
# Après modification du fichier distr/flecs.h 
# pour commenter la ligne 02 qui définit STATIC,
# Afin de créer la librairie dynamique flecs.dll.

gcc -std=gnu99 -O2 -Wall -Dflecs_EXPORTS -shared -o flecs.dll distr/flecs.c -Idistr -lWs2_32
