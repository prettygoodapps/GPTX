pragma solidity ^0.8.4;

contract GreenLedgerToken {
    // ...
    
    /**
     * @dev Mints new tokens for the owner.
     */
    function mint(address to, uint256 amount) public onlyOwner {
        require(amount <= 100000); // Limit initial supply (1% of total maxSupply)
        
        _mint(to, amount);
        emit Transfer(msg.sender, address(this), amount);
    }
    
    /**
     * @dev Pauses token transfers when necessary.
     */
    function pause() public onlyOwner {
        paused = true;
        emit Pause(address(this));
    }
    
    // ...
}
