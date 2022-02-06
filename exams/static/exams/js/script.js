// This script.js contains the functions that can be applied to each and every page //
/////////////////////////////////
// NAVBAR CLICK FUNCTIONALITY //
////////////////////////////////
// const burger = document.querySelector(".burger");
// const nav = document.querySelector(".nav");
// burger.addEventListener("click", function () {
//   nav.classList.toggle("nav-active");
//   burger.classList.toggle("toggle");
// });
$(document).ready(function() {
    // clicking the sing up button
    $("#signup_btn").click(function(e) {
        e.preventDefault();

        let first_name = $("input[name=first_name]").val()
        let second_name = $("input[name=second_name]").val()
        let email = $("input[name=eamil]").val()
        let password = $("input[name=password]").val()
        let confirm_password = $("input[name=confirm_password]").val()

        if (first_name === "" || second_name === "" || email === "" || password === "" || confirm_password === "") {
            $("p.error_msg")[0].style.display = "block"
            return
        }

        if (password !== confirm_password) {
            $("p.error_msg")[0].innerHTML = "Please confirm password!"
            $("p.error_msg")[0].style.display = "block"
            return
        }

        $("#signup_form").submit()
    })

    // clicking the login button
    $("#login_btn").click(function(e) {
        e.preventDefault();

        let email = $("input[name=login_eamil]").val()
        let password = $("input[name=login_password]").val()

        if (email === "" || password === "") {
            $("p.error_msg")[1].style.display = "block"
            return
        }

        $("#login_form").submit()
    })
    
    $('#loginModal').on('hidden.bs.modal', function () {
        $("p.error_msg")[1].style.display = "none"
    })

    $('#registerModal').on('hidden.bs.modal', function () {
        $("p.error_msg")[0].style.display = "none"
    })

})