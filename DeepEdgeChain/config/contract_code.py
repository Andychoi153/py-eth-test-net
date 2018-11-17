contract_code = """pragma solidity ^0.4.12;
contract DataStruct {
    string hashData;
    string name;
    string age;
    string time;
    
    function writeResult(string _hashData, string _name, string _age, string _time) {
        hashData = _hashData;
        name = _name;
        age = _age;
        time = _time;
    }
    
    function getHashData() constant public returns (string) {
        return hashData;
    }
    
    function getName() constant public returns (string) {
        return name;
    }
    
    function getAge() constant public returns (string) {
        return age;
    }
    
    function getTime() constant public returns (string) {
        return time;
    }
    
}"""