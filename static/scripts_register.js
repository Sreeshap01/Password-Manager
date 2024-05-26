 // regex function to check if the password contains a letter
 function containsLetter(str) {
     return /[a-zA-Z]/.test(str);
 }

 // regex function to check if the password contains a digit
 function containsDigit(str) {
     return /\d/.test(str);
 }

 // function to count the number of characters
 function countCharacters(str) {
     return str.length;
 }

 document.addEventListener('DOMContentLoaded', function() {
     const inputField = document.getElementById('password');
     const letter = document.getElementById('letter');
     const number = document.getElementById('number');
     const characters = document.getElementById('characters');
     const popup = document.getElementById("myPopup");

     inputField.addEventListener('keyup', function() {
         if (inputField.value.trim() !== '') {
             popup.style.visibility = 'visible';
         } else {
             popup.style.display = 'hidden';
         }
     })

     inputField.addEventListener('keyup', function() {
         if (containsLetter(inputField.value)) {
             // make the letter ID in color green
             letter.style.color = 'darkgreen';
             letter.style.fontWeight = 'bold';
         } else {
             letter.style.color = '#333';
             letter.style.fontWeight = 'normal';
         }
         //if value contains a digit
         if (containsDigit(inputField.value)) {
             // make the number ID in color green
             number.style.color = 'darkgreen';
             number.style.fontWeight = 'bold';
         } else {
             number.style.color = '#333';
             number.style.fontWeight = 'normal';
         }
         //if value contains 8 characters
         if (countCharacters(inputField.value) >= 8) {
             // make the characters ID in color green
             characters.style.color = 'darkgreen';
             characters.style.fontWeight = 'bold';
         } else {
             characters.style.color = '#333';
             characters.style.fontWeight = 'normal';
         }
     })

 })
