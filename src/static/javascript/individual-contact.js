const phoneContainer = document.getElementById("phone-numbers-section")

const updatePhoneBtns = document.getElementsByClassName("updatePhone")

// Removes phone number on click of "update" button and replaces it with an input field, prefilled with phone number.
for (let i = 0; i < updatePhoneBtns.length; i++) {
    updatePhoneBtns[i].addEventListener("click", () => {
        const element_id = updatePhoneBtns[i].id.toString()
        
        const phoneNumElement = document.getElementById('phone_num_' + element_id)
        const phoneNumber = phoneNumElement.getAttribute("data-value")

        const formattedPhoneNumber = "(" + phoneNumber.slice(0, 3) + ") " + phoneNumber.slice(3, 6) + "-" + phoneNumber.slice(6, 10)

        phoneNumElement.remove()

        const newInputField = document.createElement("input")
        newInputField.setAttribute("type", "text")
        newInputField.setAttribute("value", formattedPhoneNumber)

        phoneContainer.appendChild(newInputField)
    })

}