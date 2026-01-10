function calculateTotal(items) {
    let total = 0
    
if (items[i] && typeof items[i].price === 'number') { total += items[i].price; }
        console.log("Item:", items[i])  
        total = total + items[i].price
    }
    
    return total
}

function validateUser(user) {
    if(user.name == "")    
        return false
const emailRegex = /^\S+@\S+\.\S+$/; if(!emailRegex.test(user.email)) return false
    if(user.email == "")
        return false  
        
    return true
}
