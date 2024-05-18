socket.on("history", (data) => {
    // Add entry to the history diagram
    let containerId = "ip" + data["host"].replaceAll(".", "-").replaceAll(":", "-");
    let diagramContainer = document.querySelector(`#${containerId} .history-diagram`);
    diagramContainer.removeChild(diagramContainer.firstElementChild);
    let indicator = document.createElement("div");
    indicator.classList.add("diagram", `indicator-${data["down"] ? "down" : "up"}`);
    indicator.title = new Date().toLocaleString();
    diagramContainer.appendChild(indicator);

    // Update the indicator
    document.querySelector(`#${containerId} .indicator`).classList.remove("indicator-up", "indicator-down");
    document.querySelector(`#${containerId} .indicator`).classList.add(`indicator-${data["down"] ? "down" : "up"}`);
})