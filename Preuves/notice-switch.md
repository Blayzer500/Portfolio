# SAE 12 – Configuration d’un Switch Cisco

## 1. Initialisation du switch

Ces commandes permettent de remettre le switch à l’état initial.

flash_init  
delete flash:config.text  
delete flash:vlan.dat  
boot

---

## 2. Commandes de base obligatoires

Commandes essentielles pour la gestion et la sauvegarde de la configuration.

reload  
show running-config  
hostname SW1  
copy running-config startup-config

---

## 3. Création des VLAN

Création d’un VLAN avec un nom et une interface VLAN (SVI).

vlan 200  
name Vente  
exit

interface vlan 200  
ip address 192.168.20.1 255.255.255.0  
no shutdown  
exit

---

## 4. Attribution des ports à un VLAN

Affectation de plusieurs ports à un VLAN donné.

interface range fastEthernet 0/12-15  
switchport mode access  
switchport access vlan 220  
exit

---

## 5. Agrégation de ports (EtherChannel – LACP)

Création d’un lien agrégé entre plusieurs interfaces physiques.

interface range fastEthernet 0/12-25  
channel-group 2 mode active  
exit

---

## 6. Configuration du Port-Channel en Trunk

Configuration du port agrégé pour le transport de plusieurs VLANs.

interface port-channel 1  
switchport mode trunk  
switchport trunk allowed vlan 210,220,230,240  
switchport trunk native vlan 696  
exit

---

## 7. Suppression de la configuration

Effacement de la configuration et vérification de l’état des interfaces.

erase startup-config  
show interface status

---

## 8. Modification de l’adresse IP d’un VLAN

Suppression puis ajout d’une nouvelle adresse IP sur un VLAN.

interface vlan 200  
no ip address  
ip address 192.168.21.25 255.255.255.0  
exit

---

## 9. Configuration de l’accès SSH

Configuration complète de l’accès distant sécurisé via SSH.

enable  
configure terminal

hostname SW1  
ip domain-name cisco.com

crypto key generate rsa  
(2048 bits recommandés)

username cisco privilege 15 secret MotDePasse  
ip ssh version 2

line vty 0 4  
login local  
transport input ssh  
exit

---

## 10. Commandes de vérification

Vérification de l’état du SSH et des lignes VTY.

show ip ssh  
show running-config | section vty

---

## 11. Sauvegarde finale

Sauvegarde de la configuration active.

copy running-config startup-config
