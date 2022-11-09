// SPDX-Licence-Identifier: UNLICENSED
pragma solidity ^0.8.17; //Latest version as of November 2022

contract SimpleStorage {
    uint256 publicKey;
    string encryptedMessage;
    uint256 primeNumber = 13; //p
    uint256 generator = 6; //g
    struct People {
        uint256 publicKey;
        string name;
    }
    People[] public people;
    mapping(string => uint256) public nameToPublicKey;

    function getPrimeNumber() public view returns (uint256) {
        return primeNumber;
    }

    function getGenerator() public view returns (uint256) {
        return generator;
    }

    function addPersonAndKey(string memory _name, uint256 _publicKey) public {
        people.push(People(_publicKey, _name));

        nameToPublicKey[_name] = _publicKey;
    }

    function getKeyFromPerson(string memory _name) public view returns (uint256) {
        return nameToPublicKey[_name];
    }

    function storeEncryptedMessage(string memory _encryptedMessage) public {
        encryptedMessage = _encryptedMessage;
    }

    function getEncryptedMessage() public view returns (string memory) {
        return encryptedMessage;
    }
}
