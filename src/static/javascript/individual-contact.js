const phoneContainer = document.getElementById("phone-numbers-section")

const updatePhoneBtns = document.getElementsByClassName("updatePhone")
const updateEmailBtns = document.getElementsByClassName("updateEmail")

// Removes phone number on click of "update" button and replaces it with an input field, prefilled with phone number.
for (let i = 0; i < updatePhoneBtns.length; i++) {
    updatePhoneBtns[i].addEventListener("click", () => {
        const element_id = updatePhoneBtns[i].id.toString()
        
        const phoneNumElement = document.getElementById('phone_num_' + element_id)
        const phoneNumber = phoneNumElement.getAttribute("data-value")

        const formattedPhoneNumber = "(" + phoneNumber.slice(0, 3) + ") " + phoneNumber.slice(3, 6) + "-" + phoneNumber.slice(6, 10)

        phoneNumElement.remove()

        const newInputField = document.createElement("input")
        const newUpdateBtn = document.createElement("button")
        newInputField.setAttribute("type", "text")
        newInputField.setAttribute("value", formattedPhoneNumber)
        
        newUpdateBtn.innerHTML = "Confirm Update"
        newUpdateBtn.setAttribute("class", "main-button")
        newUpdateBtn.addEventListener("click", () => {
            console.log("Attempting fetch request.")
            fetch("http://localhost:5000/update-contact-phone", {method:"POST", body:JSON.stringify({phone_id: "value"})}).then(() => {console.log("testing")})
        })

        phoneContainer.appendChild(newInputField)
        phoneContainer.appendChild(newUpdateBtn)
    })

}

