let timer = null;
let currentAction = null;

function setDisplay(name, timestamp, action) {
  document.getElementById("name").textContent = name;
  document.getElementById("timestamp").textContent = timestamp;
  document.getElementById("action").textContent = action;
  clearTimeout(timer);
  timer = setTimeout(() => {
    document.getElementById("name").textContent = "";
    document.getElementById("timestamp").textContent = "";
    document.getElementById("action").textContent = "";
    currentAction = null;
  }, 5000);
}

function punch(card_id, action) {
  fetch("/api/punch", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({card_id: card_id, action: action})
  })
    .then(res => res.json())
    .then(data => setDisplay(data.name, data.timestamp, action));
}

function determineAction() {
  let now = new Date();
  return (now.getHours() < 12) ? "出勤" : "退勤";
}

document.getElementById("in-btn").onclick = () => {
  currentAction = "出勤";
  setDisplay("手動設定", new Date().toLocaleString(), "出勤");
  setTimeout(() => {
    if (currentAction === "出勤") {
      currentAction = null;
      setDisplay("", "", "");
    }
  }, 10000);
};

document.getElementById("out-btn").onclick = () => {
  currentAction = "退勤";
  setDisplay("手動設定", new Date().toLocaleString(), "退勤");
  setTimeout(() => {
    if (currentAction === "退勤") {
      currentAction = null;
      setDisplay("", "", "");
    }
  }, 10000);
};

window.onload = () => {
  fetch("/api/device_id")
    .then(res => res.json())
    .then(data => {
      document.getElementById("device-id").textContent = `装置ID: ${data.device_id}`;
    });
  // 実際はWebSocket等でカードID受信を実装
};