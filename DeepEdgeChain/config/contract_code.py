contract_code = """pragma solidity ^0.4.0;

contract DataStruct {

    struct ResultForm{
        string id;
        uint hashData;
        string name;
        uint age;
        string time;
    }
        
    address MES;
    ResultForm Result;

    function setMESAddress(address _MES){
        MES = _MES;
    }
    
    function writeResult(uint _hashData, string _name, uint _age, string _time) public{
        Result.hashData = _hashData;
        Result.name = _name;
        Result.age = _age;
        Result.time = _time;
    }
    
    function getMESAddress() constant public returns(address){
        return MES;
    }
    
    
    function getHashData() constant public returns(uint){
        return Result.hashData;
    }
    
    function getName() constant public returns(string){
        return Result.name;
    }
    
    function getAge() constant public returns(uint){
        return Result.age;
    }
    
    function getTime() constant public returns(string){
        return Result.time;
    }
    
    function confirmResult() public payable{
        MES.transfer(msg.value);
    }
    
}"""