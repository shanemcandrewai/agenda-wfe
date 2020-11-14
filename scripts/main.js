function fetchMD() {
  let myHeaders = new Headers({'cache-control': 'no-cache'});

  fetch('README.md', {headers: myHeaders})
    .then(response => response.text())
    .then(data => getMD(data));
}

function getMD(md) {
  let converter = new showdown.Converter();
  document.body.innerHTML = converter.makeHtml(md);
}

let intervalID = window.setInterval(fetchMD, 1000);
