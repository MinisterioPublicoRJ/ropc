function getCookie(name) {
  if (!document.cookie) {
    return null;
  }

  const xsrfCookies = document.cookie
    .split(";")
    .map((c) => c.trim())
    .filter((c) => c.startsWith(name + "="));

  if (xsrfCookies.length === 0) {
    return null;
  }
  return decodeURIComponent(xsrfCookies[0].split("=")[1]);
}

function checkRadioFilled(inputs){
    let no_errors = false;
    for (k = 0; k < inputs.length; k++){
        if (inputs[k].checked){
            no_errors = true;
        }
    }

    return no_errors;
}

function getRadioData(inputs){
    for (ii = 0; ii < inputs.length; ii++){
        if(inputs[ii].checked){
            return inputs[ii].value;
        }
    }
    return null;

}

function validateFields(formObj) {
  const fields = formObj.querySelectorAll("[required]");

  let no_errors = true;
  let no_radio_errors = true;
  for (i = 0; i < fields.length; i++) {
      let inputs = fields[i].getElementsByTagName("input");

      if(inputs.length == 0){ // check wether is a radion button
            if (!fields[i].value) {
              fields[i].style.borderColor = "#ED0606";
              no_errors = false;
            } else {
              fields[i].style.borderColor = "#0676ED";
            }
        }
      else {
          no_radio_errors = checkRadioFilled(inputs);
      }
  }
  return no_errors && no_radio_errors;
}

function buildFormData(fields){
    let formData = {};
    Object.entries(fields).forEach(field => {
        let fieldObj = document.querySelector(field[1]);
        let inputs = fieldObj.getElementsByTagName("input");
        if(inputs.length == 0){
            formData[field[0]] = fieldObj.value;
        }else {
            formData[field[0]] = getRadioData(inputs);
        }
    });
    return JSON.stringify(formData);
}

function showValidationErros(errors){
    document.querySelectorAll(".error-message").forEach(elem => elem.remove());
    Object.entries(errors).forEach(error => {
        let fieldObj = document.getElementById(error[0]);
        let pObj = document.createElement("p");
        pObj.classList.add("error-message");
        pObj.innerHTML = error[1];
        fieldObj.after(pObj);
    })
}

function submitFormInfo(event) {
  event.preventDefault();
  let is_valid = validateFields(document.querySelector("#main-form"));

  if (is_valid) {
    const formUUID = document.querySelector("#form_uuid").value;

    const apiFullURL = API_URL + formUUID;
    const forwardFullURL = FORWARD_URL + formUUID;
    const formData = buildFormData(FORM_VAR_LIST);
    fetch(apiFullURL, {
      method: "PUT",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: formData,
    })
      .then(response => {
        let error = false;
        if(response.status >= 400){
            response.json().then(data => {
                showValidationErros(data);
            })
        }else{
            window.location = forwardFullURL;
        }
      })
  }
}

var firstTarget = document.getElementById("first-li");
var secondTarget = document.getElementById("second-li");
var thirdTarget = document.getElementById("third-li");
var fourthTarget = document.getElementById("fourth-li");


// Mudar cor e imagem da primeira li

var mouseOverFunctionFirtsLi = function () {
  document.getElementById("target-image-first-li").setAttribute("src", `${STATIC_PREFIX}img/home-amarela.png`);
};
firstTarget.onmouseover = mouseOverFunctionFirtsLi;

var mouseLeaveFunctionFirtsLi = function () {
  document.getElementById("target-image-first-li").setAttribute("src",  `${STATIC_PREFIX}img/home.png`);
};
firstTarget.onmouseleave = mouseLeaveFunctionFirtsLi;

// Mudar cor e imagem da segunda li
var mouseOverFunctionSecondLi = function () {
  document.getElementById("target-image-second-li").setAttribute("src", `${STATIC_PREFIX}img/align-left-amarela.png`);
};
secondTarget.onmouseover = mouseOverFunctionSecondLi;

var mouseLeaveFunctionSecondLi = function () {
  document.getElementById("target-image-second-li").setAttribute("src",  `${STATIC_PREFIX}img/align-left.png`);
};
secondTarget.onmouseleave = mouseLeaveFunctionSecondLi;

// Mudar cor e imagem da terceira li
var mouseOverFunctionThirdLi = function () {
  document.getElementById("target-image-third-li").setAttribute("src", `${STATIC_PREFIX}img/file-plus-amarela.png`);
};
thirdTarget.onmouseover = mouseOverFunctionThirdLi;

var mouseLeaveFunctionThirdLi = function () {
  document.getElementById("target-image-third-li").setAttribute("src",  `${STATIC_PREFIX}img/file-plus.png`);
};
thirdTarget.onmouseleave = mouseLeaveFunctionThirdLi;

// Mudar cor e imagem da quarta li
var mouseOverFunctionFourthdLi = function () {
  document.getElementById("target-image-fourth-li").setAttribute("src", `${STATIC_PREFIX}img/chart-amarelo.png`);
};
fourthTarget.onmouseover = mouseOverFunctionFourthdLi;

var mouseLeaveFunctionFourthdLi = function () {
  document.getElementById("target-image-fourth-li").setAttribute("src",  `${STATIC_PREFIX}img/chart.png`);
};
fourthTarget.onmouseleave = mouseLeaveFunctionFourthdLi;