function calculateTotal(items) {
    let total = 0
    
        console.log("Item:", items[i])  
        total = total + items[i].price
    }
    
    return total
}

function validateUser(user) {
    if(user.name == "")    
        return false
    
if(!user.name || user.name.trim() === '') return false
        return false  
if(!user.email || !validateEmailFormat(user.email)) return false
    return true
}
