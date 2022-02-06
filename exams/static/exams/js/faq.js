//////////////////////////////
// ACCORDION FUNCTIONALITY //
////////////////////////////
const FAQBtnsDOWN = document.querySelectorAll(".DOWN___IONICON");
const NameValueChanger = (element) => {
  let value__name = element.getAttribute("name");
  if (value__name === "chevron-down-outline") {
    element.setAttribute("name", "remove-outline");
  }
  if (value__name === "remove-outline") {
    element.setAttribute("name", "chevron-down-outline");
  }
};

const ParagraphDisplayToggler = (element) => {
  element.classList.toggle("faq__para__active");
};

FAQBtnsDOWN.forEach((element) => {
  element.addEventListener("click", function () {
    NameValueChanger(element);
    ParagraphDisplayToggler(element.parentElement.parentElement);
  });
});
