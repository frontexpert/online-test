/////////////////////////////////////////
// NAVBAR SCROLL STCIKY FUNCTIONALITY //
///////////////////////////////////////
const header = document.querySelector(".header");
const section__1 = document.querySelector(".section__1");
const section__2 = document.querySelector(".section__2");

const stickyNav = function (entries) {
  const [entry] = entries;

  if (!entry.isIntersecting) {
    header.classList.add("nav_sticky");
  } else {
    header.classList.remove("nav_sticky");
  }
};

const navOptions = {
  root: null,
  threshold: 0,
};

const headerObserver = new IntersectionObserver(stickyNav, navOptions);
if (section__1 !== null)
  headerObserver.observe(section__1);

////////////////////////////////////
//TABBED COMPONENT FUNCTIONALITY //
//////////////////////////////////

const Tab__BTN = document.querySelectorAll(".CTA___btn");
const Tabbed__component_Text__Box = document.querySelectorAll(
  ".third__sec__content__Box"
);

// FUNCTION TO REMOVE THE ACTIVATED CLASSES
const removeBtnActived = (allSelected, removingClass) => {
  allSelected.forEach((element) => {
    element.classList.remove(removingClass);
  });
};

// ADDING EVENT LISTENERS TO THE BUTTONS
Tab__BTN.forEach((element) => {
  element.addEventListener("click", () => {
    // REMOVING THE CLASSES USING FUNCTION
    removeBtnActived(Tab__BTN, "activedBTN");
    removeBtnActived(
      Tabbed__component_Text__Box,
      "third__sec__content__Box__activated"
    );

    // SELECTIG THE DATA VALUE OF CLICKED
    const btnNum = element.dataset.box;
    element.classList.add("activedBTN");

    document
      .querySelector(`.content__Box__${btnNum}`)
      .classList.add("third__sec__content__Box__activated");
  });
});
