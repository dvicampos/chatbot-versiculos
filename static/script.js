let userName = localStorage.getItem('user_name') || "";

// Función para agregar mensajes al chat
function addMessage(message, sender = "bot") {
    const chatBox = document.getElementById("chat-box");

    // Crear el contenedor para el mensaje
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);
    
    // Crear el contenedor para el nombre
    const nameDiv = document.createElement("div");
    nameDiv.classList.add("message-sender", sender);
    nameDiv.innerText = sender === "user" ? userName : "Asistente Bíblico"; // Agregar el nombre del usuario o chatbot
    
    // Crear el contenedor para el texto del mensaje
    const textDiv = document.createElement("div");
    textDiv.classList.add("message-text");
    textDiv.innerHTML = message;
    
    // Agregar el nombre y el mensaje al contenedor
    messageDiv.appendChild(nameDiv);
    messageDiv.appendChild(textDiv);
    
    // Añadir el mensaje al chat
    chatBox.appendChild(messageDiv);

    // Desplazar el chat hacia abajo
    chatBox.scrollTop = chatBox.scrollHeight;
}


function createButtons(options, category, index) {
    const buttonContainer = document.querySelector(".button-container");
    buttonContainer.innerHTML = "";

    options.forEach((option) => {
        const button = document.createElement("button");
        button.innerText = option;
        button.classList.add("option-button");
        button.onclick = () => handleUserInput(option, category, index);
        buttonContainer.appendChild(button);
    });

    const exitButton = document.createElement("button");
    exitButton.innerText = "Salir";
    exitButton.classList.add("exit-button");
    exitButton.onclick = () => handleExit();
    buttonContainer.appendChild(exitButton);
}

function handleExit() {
    localStorage.removeItem('user_name');
    
    addMessage("¡Hasta pronto! Vuelve cuando quieras.", "bot");

    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML = "";

    const buttonContainer = document.querySelector(".button-container");
    buttonContainer.innerHTML = "";

    document.getElementById("name-form-container").style.display = "block";
    document.getElementById("name-input").value = "";
    document.getElementById("name-form").style.display = "block";

    userName = "";

    setTimeout(() => {
        window.location.reload(); 
    }, 2000);
}

function handleUserInput(userInput, category, index) {
    const categoryName = category || "✝️";
    addMessage(`${userInput} (${categoryName})`, "user");

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            message: userInput,
            category: category,
            index: index,
            user_name: userName 
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            addMessage(data.message);
            if (data.options) {
                createButtons(data.options, data.category, data.index);
            }
        });
}

function handleNameInput(event) {
    event.preventDefault();
    const nameInput = document.getElementById("name-input");
    userName = nameInput.value.trim();
    if (userName) {
        localStorage.setItem('user_name', userName);

        document.getElementById("name-form").style.display = "none";
        addMessage(`¡Hola, ${userName}! ¿Cómo te sientes hoy?`);

        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                message: "Selecciona una opción:",
                user_name: userName,
            }),
        })
            .then((response) => response.json())
            .then((data) => {
                addMessage(data.message);
                createButtons(data.options);
            });
    }
}

function checkForStoredName() {
    const storedName = localStorage.getItem('user_name');
    if (storedName) {
        userName = storedName;
        document.getElementById("name-form").style.display = "none";
        addMessage(`¡Hola, ${userName}! ¿Cómo te sientes hoy?`);
        
        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                message: "Selecciona una opción:",
                user_name: userName,
            }),
        })
            .then((response) => response.json())
            .then((data) => {
                addMessage(data.message);
                createButtons(data.options);
            });
    } else {
        document.getElementById("name-form").style.display = "block";
    }
}

document.addEventListener("DOMContentLoaded", function () {
    checkForStoredName();

    const form = document.getElementById("name-form");
    form.addEventListener("submit", handleNameInput);
});
