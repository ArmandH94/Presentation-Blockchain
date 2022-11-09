from brownie import accounts,config, SimpleStorage, network

alice_secret_key = 5 # Alice's private key for DH key exchange
bob_secret_key = 4 # Bob's private key for DH key exchange
alice_message = "Bonjour"

def increment_number_of_executions():
    reader = open("number_of_executions.txt", "r")
    number_of_executions = reader.readline()
    reader.close()

    new_number_of_executions = int(number_of_executions) + 1
    print("Number of execution(s) for this script : ", new_number_of_executions)

    reader = open("number_of_executions.txt", "w")
    reader.writelines(str(new_number_of_executions))
    reader.close()


#Use a local ganache account by default for development if the network is not mentioned in the command line
#Else use the account in brownie-config.yaml file and the private key in the env variables
def get_account_alice():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def get_account_bob():
    if network.show_active() == "development":
        return accounts[1]
    else:
        return accounts.add(config["wallets"]["from_key_2"])

#Deploying the contract with Alice's account
def deploy_simple_storage():
    alice_account = get_account_alice()
    simple_storage = SimpleStorage.deploy({"from": alice_account})
    return simple_storage

def get_prime_num(simple_storage):
    return simple_storage.getPrimeNumber()

def get_generator(simple_storage):
    return simple_storage.getGenerator()
     
def calculate_public_key(secret_key, generator, primeNumber):
    return (generator**secret_key) % primeNumber

def calculate_shared_secret(public_key, secret_key, primeNumber):
    return (public_key**secret_key) % primeNumber

def store_public_key(simple_storage, name, public_key, account):
    transaction = simple_storage.addPersonAndKey(name, public_key, account)
    transaction.wait(1) #Wait for the transaction to be mined

def cesar_cipher(text,key):
    result = ""
 
    for i in range(len(text)):
        char = text[i]
 
        # Encrypt uppercase characters
        if (char.isupper()):
            result += chr((ord(char) + key-65) % 26 + 65)
 
        # Encrypt lowercase characters
        else:
            result += chr((ord(char) + key - 97) % 26 + 97)
 
    return result    

def store_encrypted_message(simple_storage, encrypted_message, account):
    transaction = simple_storage.storeEncryptedMessage(encrypted_message, account)
    transaction.wait(1) #Wait for the transaction to be mined

#To execute the script : brownie run scripts/deploy.py
#To execute the script on the goerli network : brownie run scripts/deploy.py --network goerli
def main():
    #Counts the number of times the script has been executed
    increment_number_of_executions()

    #######################################Deploying the contract########################################
    simple_storage = deploy_simple_storage()

    print("Alice secret key : ", alice_secret_key)
    print("Bob secret key : ", bob_secret_key)

    #######################################Getting the prime number and generator from the contract########################################
    print("Getting the prime number and generator from the contract...")
    primeNumber = get_prime_num(simple_storage)
    generator = get_generator(simple_storage)
    print("Prime number: ", primeNumber)
    print("Generator: ", generator)

    #######################################Calculating the public keys########################################
    alice_public_key = calculate_public_key(alice_secret_key, generator, primeNumber)
    print("Alice's public key: ", alice_public_key)
    
    bob_public_key = calculate_public_key(bob_secret_key, generator, primeNumber)
    print("Bob's public key: ", bob_public_key)

    #######################################Storing Alice and Bob's public keys in the contract########################################
    print("Storing Alice's public key in the contract...")
    store_public_key(simple_storage, "Alice", alice_public_key, {"from": get_account_alice()})

    print("Storing Bob's public key in the contract...")
    store_public_key(simple_storage, "Bob", bob_public_key, {"from": get_account_bob()})

    #######################################Getting the public keys from the contract########################################
    print("Alice gets Bob’s public key from the contract...")
    bob_pk_from_contract = simple_storage.getKeyFromPerson("Bob")
    print("bob_pk_from_contract: ", bob_pk_from_contract) 

    print("Bob gets Alice’s public key from the contract...")
    alice_pk_from_contract = simple_storage.getKeyFromPerson("Alice")
    print("alice_pk_from_contract: ", alice_pk_from_contract) 

    #######################################Calculating the shared secret########################################
    #Alice calculates the shared secret
    shared_secret_alice = calculate_shared_secret(bob_pk_from_contract, alice_secret_key, primeNumber)
    print("Shared secret calculated by Alice: ", shared_secret_alice) 

    #Bob calculates the shared secret    
    shared_secret_bob = calculate_shared_secret(alice_pk_from_contract, bob_secret_key, primeNumber)
    print("Shared secret calculated by Bob: ", shared_secret_bob) 

    #######################################Encryption of the message########################################
    print("Message to encrypt: ", alice_message)

    print("Alice encrypts the message with the shared secret...")
    alice_secret_message = cesar_cipher(alice_message, shared_secret_alice)
    print("Encrypted message: ", alice_secret_message)

    #######################################Sending the encrypted message to the contract########################################
    print("Alice sends the encrypted message to the contract...")
    store_encrypted_message(simple_storage, alice_secret_message, {"from": get_account_alice()})
    
    #######################################Getting the encrypted message from the contract########################################
    print("Bob gets the encrypted message from the contract...")
    encrypted_message_from_contract = simple_storage.getEncryptedMessage()
 
    #######################################Decryption of the message########################################
    print("Bob decrypts the message with his shared secret...")
    decrypted_message = cesar_cipher(encrypted_message_from_contract, -shared_secret_bob)
    print("Decrypted message: ", decrypted_message)

