// DISABLING THE RULES AND ENABLNG THE MCQ AFTER ACCEPTING THE RULE
const RuleAccepted = document.querySelector(".RuleAccepted");
const RuleSection = document.querySelector(".MCQ___termsAndConditions");
const MCQ__Section = document.querySelector(".mcq__section__1__col_2");
RuleAccepted.addEventListener("click", function () {
  RuleSection.classList.toggle("mcq__section__1__col_diabled");
  MCQ__Section.classList.toggle("mcq__section__1__col_diabled");
});
