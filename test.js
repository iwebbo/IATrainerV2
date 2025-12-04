function calculateTotal(items) {
    console.log("Debug: calculating total")
    let total = 0
    
    for(let i = 0; i < items.length; i++) {
        console.log("Item:", items[i])  
        total = total + items[i].price
    }
    
    return total
}

function validateUser(user) {
    if(user.name == "")    
        return false
    
    if(user.email == "")
        return false  
        
    return true
}
