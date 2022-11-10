# Presentation-Blockchain

Presentation on how blockchains can be used for cryptography

To run the code :  
-Create a .env file at the root of the project folder (the .env file should NEVER be shared)  
-Add the following lines  
export PRIVATE_KEY=0xXXXXXXXXXXXXXXXXXXXXXX  
export PRIVATE_KEY_2=0xXXXXXXXXXXXXXXXXXXXXXX  
export WEB3_INFURA_PROJECT_ID=XXXXXXXXXXXXXXX  

PRIVATE_KEY (Alice's private Key): In Metamask, create an account on the Goerli network, export the private key and add funds by using a Goerli faucet.  
PRIVATE_KEY_2 (Bob's private key) : Create a second account on Metamask and follow the same steps  
WEB3_INFURA_PROJECT_ID : the API KEY can be found in the Infura dashboard (create an account + a project first)  

![image](https://user-images.githubusercontent.com/65608974/200974628-1347bbfb-740f-437a-a228-a42718917985.png)  

To execute the script on a Ganache local blockchain :   
brownie run scripts/deploy.py  

To execute the script on the Goerli testnet :   
brownie run scripts/deploy.py --network goerli  
