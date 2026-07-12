// ==========================================
// Vehicle Rental Booking System
// Professional JavaScript
// ==========================================

// Welcome Message
window.onload = function () {

    console.log("Vehicle Rental Booking System Loaded Successfully");

};


// Vehicle Details Popup

const buttons = document.querySelectorAll(".card button");

if (buttons.length >= 3) {

    buttons[0].addEventListener("click", function () {

        alert(
`🚗 Luxury Car

Price : ₹2000 / Day

Seats : 5

Fuel : Petrol

Mileage : 18 km/l

Air Conditioner : Yes

Available : Yes`
        );

    });


    buttons[1].addEventListener("click", function () {

        alert(
`🏍 Sports Bike

Price : ₹800 / Day

Engine : 220 CC

Mileage : 40 km/l

Fuel : Petrol

Helmet : Included

Available : Yes`
        );

    });


    buttons[2].addEventListener("click", function () {

        alert(
`🛵 City Scooter

Price : ₹500 / Day

Mileage : 45 km/l

Fuel : Petrol

Storage : Large

Available : Yes`
        );

    });

}


// Booking Form Validation

const bookingForm = document.querySelector(".booking-form");

if (bookingForm) {

    bookingForm.addEventListener("submit", function (event) {

        const fullname = document.querySelector("input[name='fullname']").value.trim();

        const mobile = document.querySelector("input[name='mobile']").value.trim();

        const bookingDate = document.querySelector("input[name='booking_date']").value;

        const vehicle = document.querySelector("select[name='vehicle']").value;

        if (fullname.length < 3) {

            alert("Please enter a valid full name.");

            event.preventDefault();

            return;

        }

        if (!/^[0-9]{10}$/.test(mobile)) {

            alert("Please enter a valid 10-digit mobile number.");

            event.preventDefault();

            return;

        }

        if (bookingDate === "") {

            alert("Please select a booking date.");

            event.preventDefault();

            return;

        }

        if (vehicle === "") {

            alert("Please select a vehicle.");

            event.preventDefault();

            return;

        }

    });

}


// Navbar Hover Effect

const navLinks = document.querySelectorAll("nav a");

navLinks.forEach(function(link){

    link.addEventListener("mouseover", function(){

        this.style.color = "#ffdd00";

    });

    link.addEventListener("mouseout", function(){

        this.style.color = "white";

    });

});


// Print Receipt

function printReceipt(){

    window.print();

}


// Smooth Scroll

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function(e){

        e.preventDefault();

        document.querySelector(this.getAttribute("href")).scrollIntoView({

            behavior:"smooth"

        });

    });

});


// Success Message

console.log("Professional Vehicle Rental Booking System Loaded Successfully.");