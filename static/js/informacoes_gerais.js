const FORWARD_URL = '/operacoes/cadastro/informacoes/operacionais/parte-1/';
const API_URL = '/v1/operacoes/cria-informacoes-gerais/';
const FORM_VAR_LIST = {
    "data": "#data_operacao",
    "hora": "#hora_operacao",
    "municipio": "#municipio_operacao",
    "bairro": "#bairro_operacao",
    "localidade": "#localidade_operacao",
    "endereco_referencia": "#endereco_referencia",
    "batalhao_responsavel": "#batalhao_operacao"
};


function getBairros(object) {
  const bairroUrl = `/v1/dados/bairros-rj/${object.value}`;
  fetch(bairroUrl, { method: "GET" })
    .then((response) => response.json())
    .then((data) => {
      let bairroSelector = document.querySelector("#bairro_operacao");
      bairroSelector.innerHTML = "";
      let option = document.createElement("option");
      option.text = "-";
      option.value = "";
      bairroSelector.add(option);
      data.forEach((bairro) => {
        option = document.createElement("option");
        option.text = bairro.bairro;
        option.value = bairro.bairro;
        bairroSelector.add(option);
      });
    })
    .catch((error) => {});
}

function getBatalhoes(object) {
  const batalhaoUrl = `/v1/dados/batalhoes-rj/${object.value}`;
  fetch(batalhaoUrl, { method: "GET" })
    .then((response) => response.json())
    .then((data) => {
      let batalhaoSelector = document.querySelector("#batalhao_operacao");
      batalhaoSelector.innerHTML = "";
      let option = document.createElement("option");
      option.text = "-";
      option.value = "";
      batalhaoSelector.add(option);
      data.forEach((batalhao) => {
        option = document.createElement("option");
        option.text = batalhao.bpm;
        option.value = batalhao.bpm;
        batalhaoSelector.add(option);
      });
    })
    .catch((error) => {});
}
